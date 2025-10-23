#!/usr/bin/env python3
"""
Document to PDF Converter with OCR
Converts various document formats (PPTX, DOCX, images) to searchable PDFs.
Perfect for preparing educational materials for AI analysis.
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Tuple


class DocumentConverter:
    """Main converter class for handling various document formats."""
    
    # Supported file extensions
    OFFICE_FORMATS = {'.pptx', '.docx', '.doc', '.ppt', '.xlsx', '.xls', '.odt', '.odp', '.ods', '.rtf'}
    IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.heic'}
    PDF_FORMATS = {'.pdf'}
    TEXT_FORMATS = {'.txt', '.md', '.csv', '.tsv', '.log', '.json', '.xml', '.html', '.htm'}
    
    def __init__(self, source_folder: Path, output_folder: Path = None, use_ocr: bool = True, merge_output: bool = False):
        """
        Initialize the converter.
        
        Args:
            source_folder: Path to source folder containing documents
            output_folder: Path to output folder (default: source_folder/converted_pdfs)
            use_ocr: Whether to apply OCR to documents (default: True)
            merge_output: Whether to merge all PDFs into a single file (default: False)
        """
        self.source_folder = Path(source_folder).resolve()
        self.output_folder = output_folder or (self.source_folder / "converted_pdfs")
        self.use_ocr = use_ocr
        self.merge_output = merge_output
        
        self.stats = {
            'total': 0,
            'converted': 0,
            'failed': 0,
            'skipped': 0
        }
        
        self.converted_pdfs = []
        
        # Check dependencies
        self.deps = self._check_dependencies()
        
    def _check_dependencies(self) -> Dict[str, bool]:
        """Check if required tools are installed."""
        tools = {
            'libreoffice': ['libreoffice', '--version'],
            'tesseract': ['tesseract', '--version'],
            'pdftoppm': ['pdftoppm', '-v'],
            'convert': ['convert', '--version']  # ImageMagick
        }
        
        available = {}
        for tool, cmd in tools.items():
            try:
                subprocess.run(cmd, capture_output=True, check=True, timeout=5)
                available[tool] = True
            except:
                available[tool] = False
        
        return available
    
    def print_dependencies(self):
        """Print dependency status."""
        print("Dependency Check:")
        print(f"  LibreOffice:     {'✓' if self.deps['libreoffice'] else '✗ (required for Office docs)'}")
        print(f"  Tesseract OCR:   {'✓' if self.deps['tesseract'] else '✗ (optional, for OCR)'}")
        print(f"  Poppler:         {'✓' if self.deps['pdftoppm'] else '✗ (optional, for OCR)'}")
        print(f"  ImageMagick:     {'✓' if self.deps['convert'] else '✗ (optional, for images)'}")
        print()
    
    def collect_files(self) -> List[Path]:
        """Collect all convertible files from source folder and subfolders."""
        files = []
        all_formats = self.OFFICE_FORMATS | self.IMAGE_FORMATS | self.PDF_FORMATS | self.TEXT_FORMATS
        
        for root, dirs, filenames in os.walk(self.source_folder):
            for filename in filenames:
                file_path = Path(root) / filename
                if file_path.suffix.lower() in all_formats:
                    files.append(file_path)
        
        return sorted(files)
    
    def convert_office_to_pdf(self, file_path: Path, output_path: Path) -> bool:
        """
        Convert Office documents (PPTX, DOCX, etc.) to PDF using LibreOffice.
        
        Args:
            file_path: Path to source document
            output_path: Path to output PDF
            
        Returns:
            True if successful, False otherwise
        """
        if not self.deps['libreoffice']:
            print(f"  ✗ LibreOffice not installed, cannot convert {file_path.name}")
            return False
        
        # LibreOffice outputs to the specified directory with the same name
        temp_dir = output_path.parent
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(temp_dir),
            str(file_path)
        ]
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                timeout=180,
                text=True
            )
            
            # LibreOffice creates file with same base name
            expected_pdf = temp_dir / (file_path.stem + '.pdf')
            
            if expected_pdf.exists():
                # Rename to desired output name if different
                if expected_pdf != output_path:
                    # Handle name conflicts
                    if output_path.exists():
                        counter = 1
                        while output_path.exists():
                            output_path = temp_dir / f"{output_path.stem}_{counter}.pdf"
                            counter += 1
                    expected_pdf.rename(output_path)
                return True
            else:
                print(f"  ✗ LibreOffice failed to create PDF for {file_path.name}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"  ✗ Timeout converting {file_path.name}")
            return False
        except Exception as e:
            print(f"  ✗ Error converting {file_path.name}: {e}")
            return False
    
    def convert_image_to_pdf(self, image_path: Path, output_path: Path) -> bool:
        """
        Convert image to PDF, optionally with OCR.
        
        Args:
            image_path: Path to source image
            output_path: Path to output PDF
            
        Returns:
            True if successful, False otherwise
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Method 1: Use ImageMagick (simple, no OCR)
        if not self.use_ocr or not self.deps['tesseract']:
            if self.deps['convert']:
                cmd = ['convert', str(image_path), str(output_path)]
                try:
                    subprocess.run(cmd, check=True, capture_output=True, timeout=60)
                    return True
                except Exception as e:
                    print(f"  ✗ ImageMagick conversion failed for {image_path.name}: {e}")
                    return False
            else:
                print(f"  ✗ ImageMagick not installed, cannot convert {image_path.name}")
                return False
        
        # Method 2: Use OCR (requires tesseract and additional Python libraries)
        try:
            from PIL import Image
            import pytesseract
            import fitz  # PyMuPDF
            
            # Open image
            img = Image.open(image_path)
            
            # Perform OCR
            ocr_text = pytesseract.image_to_string(img, lang='deu+eng')
            
            # Create PDF with image and invisible text
            pdf_document = fitz.open()
            
            # Convert image to PDF page
            import io
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PDF')
            img_buffer.seek(0)
            
            # Add page to PDF
            img_pdf = fitz.open("pdf", img_buffer.read())
            pdf_document.insert_pdf(img_pdf)
            
            # Add OCR text as invisible layer
            if ocr_text.strip():
                page = pdf_document[0]
                page.insert_text((10, 10), ocr_text, fontsize=0.1, color=(1, 1, 1))
            
            # Save the final PDF
            pdf_document.save(str(output_path))
            pdf_document.close()
            
            return True
            
        except ImportError:
            # Fallback to ImageMagick if Python libraries not available
            if self.deps['convert']:
                cmd = ['convert', str(image_path), str(output_path)]
                try:
                    subprocess.run(cmd, check=True, capture_output=True, timeout=60)
                    return True
                except Exception as e:
                    print(f"  ✗ Conversion failed for {image_path.name}: {e}")
                    return False
            else:
                print(f"  ✗ Cannot convert {image_path.name} (missing dependencies)")
                return False
                
        except Exception as e:
            print(f"  ✗ OCR failed for {image_path.name}: {e}")
            return False
    
    def convert_text_to_pdf(self, text_path: Path, output_path: Path) -> bool:
        """
        Convert text file to PDF.
        
        Args:
            text_path: Path to source text file
            output_path: Path to output PDF
            
        Returns:
            True if successful, False otherwise
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            import fitz  # PyMuPDF
            
            # Read text file
            with open(text_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            # Create PDF
            pdf_document = fitz.open()
            page = pdf_document.new_page(width=595, height=842)  # A4 size
            
            # Add text to page
            text_rect = fitz.Rect(50, 50, 545, 792)
            page.insert_textbox(text_rect, text, fontsize=10, fontname="helv")
            
            # Save PDF
            pdf_document.save(str(output_path))
            pdf_document.close()
            
            return True
            
        except ImportError:
            print(f"  ✗ PyMuPDF not installed, cannot convert {text_path.name}")
            return False
        except Exception as e:
            print(f"  ✗ Failed to convert {text_path.name}: {e}")
            return False
    
    def copy_pdf(self, pdf_path: Path, output_path: Path) -> bool:
        """
        Copy existing PDF and optionally apply OCR.
        
        Args:
            pdf_path: Path to source PDF
            output_path: Path to output PDF
            
        Returns:
            True if successful, False otherwise
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(pdf_path, output_path)
            
            if self.use_ocr and self.deps['tesseract'] and self.deps['pdftoppm']:
                print(f"  Applying OCR to existing PDF...")
                self.apply_ocr_to_pdf(output_path)
            
            return True
            
        except Exception as e:
            print(f"  ✗ Failed to copy {pdf_path.name}: {e}")
            return False
    
    def merge_pdfs(self, pdf_paths: List[Path], output_path: Path) -> bool:
        """
        Merge multiple PDFs into a single PDF.
        
        Args:
            pdf_paths: List of PDF paths to merge
            output_path: Path to output merged PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import fitz  # PyMuPDF
            
            # Create new PDF
            merged_pdf = fitz.open()
            
            # Add each PDF
            for pdf_path in pdf_paths:
                try:
                    pdf_doc = fitz.open(str(pdf_path))
                    merged_pdf.insert_pdf(pdf_doc)
                    pdf_doc.close()
                except Exception as e:
                    print(f"  ⚠ Failed to add {pdf_path.name}: {e}")
            
            # Save merged PDF
            merged_pdf.save(str(output_path))
            merged_pdf.close()
            
            return True
            
        except ImportError:
            print("  ✗ PyMuPDF not installed, cannot merge PDFs")
            return False
        except Exception as e:
            print(f"  ✗ Failed to merge PDFs: {e}")
            return False
    
    def apply_ocr_to_pdf(self, pdf_path: Path) -> bool:
        """
        Apply OCR to an existing PDF to make it searchable.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.deps['tesseract'] or not self.deps['pdftoppm']:
            return False
        
        try:
            from pdf2image import convert_from_path
            import pytesseract
            import fitz
            
            # Convert PDF to images
            images = convert_from_path(str(pdf_path), dpi=300)
            
            # Create new PDF with OCR
            temp_path = pdf_path.with_suffix('.ocr.pdf')
            pdf_document = fitz.open()
            
            for i, image in enumerate(images):
                # Perform OCR
                ocr_text = pytesseract.image_to_string(image, lang='deu+eng')
                
                # Convert PIL image to PDF page
                import io
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PDF')
                img_buffer.seek(0)
                
                img_pdf = fitz.open("pdf", img_buffer.read())
                pdf_document.insert_pdf(img_pdf)
                
                # Add OCR text as invisible layer
                if ocr_text.strip():
                    page = pdf_document[-1]
                    page.insert_text((10, 10), ocr_text, fontsize=0.1, color=(1, 1, 1))
            
            # Save and replace
            pdf_document.save(str(temp_path))
            pdf_document.close()
            
            temp_path.replace(pdf_path)
            return True
            
        except ImportError:
            return False
        except Exception as e:
            print(f"  ⚠ OCR failed: {e}")
            return False
    
    def convert_file(self, file_path: Path) -> bool:
        """
        Convert a single file to PDF.
        
        Args:
            file_path: Path to file to convert
            
        Returns:
            True if successful, False otherwise
        """
        ext = file_path.suffix.lower()
        
        # Generate output filename
        relative_path = file_path.relative_to(self.source_folder)
        output_name = f"{relative_path.parent / file_path.stem}.pdf".replace('/', '_').replace('\\', '_')
        if output_name.startswith('._'):
            output_name = output_name[2:]
        output_path = self.output_folder / output_name
        
        # Handle duplicate names
        if output_path.exists():
            counter = 1
            while output_path.exists():
                output_path = self.output_folder / f"{output_path.stem}_{counter}.pdf"
                counter += 1
        
        print(f"Converting: {file_path.name}")
        
        success = False
        
        if ext in self.OFFICE_FORMATS:
            success = self.convert_office_to_pdf(file_path, output_path)
            if success and self.use_ocr and self.deps['tesseract'] and self.deps['pdftoppm']:
                print(f"  Applying OCR...")
                self.apply_ocr_to_pdf(output_path)
        elif ext in self.IMAGE_FORMATS:
            success = self.convert_image_to_pdf(file_path, output_path)
        elif ext in self.TEXT_FORMATS:
            success = self.convert_text_to_pdf(file_path, output_path)
        elif ext in self.PDF_FORMATS:
            success = self.copy_pdf(file_path, output_path)
        
        if success:
            print(f"  ✓ Saved to: {output_path.name}")
            self.converted_pdfs.append(output_path)
        
        return success
    
    def convert_all(self):
        """Convert all files in the source folder."""
        # Create output directory
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"Source folder: {self.source_folder}")
        print(f"Output folder: {self.output_folder}")
        print()
        
        self.print_dependencies()
        
        # Collect files
        files = self.collect_files()
        self.stats['total'] = len(files)
        
        if not files:
            print("No convertible files found.")
            return
        
        print(f"Found {len(files)} files to convert")
        print("=" * 60)
        
        # Convert each file
        for file_path in files:
            if self.convert_file(file_path):
                self.stats['converted'] += 1
            else:
                self.stats['failed'] += 1
            print()
        
        # Merge all PDFs if requested
        if self.merge_output and self.converted_pdfs:
            print("=" * 60)
            print("Merging all PDFs into single document...")
            merged_path = self.output_folder / "merged_all_documents.pdf"
            if self.merge_pdfs(self.converted_pdfs, merged_path):
                print(f"✓ Merged PDF saved to: {merged_path}")
            else:
                print("✗ Failed to merge PDFs")
            print()
        
        # Print summary
        print("=" * 60)
        print("Conversion Summary:")
        print(f"  Total files:     {self.stats['total']}")
        print(f"  Converted:       {self.stats['converted']}")
        print(f"  Failed:          {self.stats['failed']}")
        print(f"\nAll PDFs saved to: {self.output_folder}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert documents to searchable PDFs for AI analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/documents
  %(prog)s /path/to/documents -o /path/to/output
  %(prog)s /path/to/documents --no-ocr
  %(prog)s /path/to/documents --merge
  
Supported formats:
  Office: .pptx, .docx, .doc, .ppt, .xlsx, .xls, .odt, .odp, .ods, .rtf
  Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .tif, .webp, .svg, .heic
  Text: .txt, .md, .csv, .tsv, .log, .json, .xml, .html, .htm
  PDF: .pdf (will be copied and optionally OCR'd)
        """
    )
    
    parser.add_argument(
        'source_folder',
        help='Path to folder containing documents to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_folder',
        help='Output folder for PDFs (default: source_folder/converted_pdfs)'
    )
    
    parser.add_argument(
        '--no-ocr',
        dest='use_ocr',
        action='store_false',
        default=True,
        help='Disable OCR (faster but PDFs won\'t be searchable)'
    )
    
    parser.add_argument(
        '-m', '--merge',
        dest='merge_output',
        action='store_true',
        default=False,
        help='Merge all PDFs into a single output file'
    )
    
    args = parser.parse_args()
    
    # Validate source folder
    source = Path(args.source_folder)
    if not source.exists():
        print(f"Error: Source folder '{source}' does not exist!")
        sys.exit(1)
    
    if not source.is_dir():
        print(f"Error: '{source}' is not a directory!")
        sys.exit(1)
    
    # Convert documents
    output = Path(args.output_folder) if args.output_folder else None
    converter = DocumentConverter(source, output, args.use_ocr, args.merge_output)
    converter.convert_all()


if __name__ == "__main__":
    main()

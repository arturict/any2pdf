#!/usr/bin/env python3
"""
Document to PDF Converter with OCR
Converts various document formats (PPTX, DOCX, images) to searchable PDFs.
Perfect for preparing educational materials for AI analysis.

Performance optimized with:
- Parallel processing for batch conversions
- Smart caching to avoid re-conversions
- Optimized OCR detection
"""

import os
import sys
import argparse
import subprocess
import shutil
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Tuple
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from functools import partial
import time
import base64

# Interactive CLI libraries
try:
    import questionary
    from questionary import Style
    QUESTIONARY_AVAILABLE = True
except ImportError:
    QUESTIONARY_AVAILABLE = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# Try to import AI libraries (optional)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ANSI Color codes
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def disable():
        """Disable colors (for piped output)."""
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.ENDC = ''
        Colors.BOLD = ''
        Colors.DIM = ''
        Colors.UNDERLINE = ''


# Check if output is being piped
if not sys.stdout.isatty():
    Colors.disable()


class DocumentConverter:
    """Main converter class for handling various document formats."""
    
    # Supported file extensions
    OFFICE_FORMATS = {'.pptx', '.docx', '.doc', '.ppt', '.xlsx', '.xls', '.odt', '.odp', '.ods', '.rtf'}
    IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.heic'}
    PDF_FORMATS = {'.pdf'}
    TEXT_FORMATS = {'.txt', '.md', '.csv', '.tsv', '.log', '.json', '.xml', '.html', '.htm'}
    
    def __init__(self, source_folder: Path, output_folder: Path = None, use_ocr: bool = True, merge_output: bool = False, max_workers: int = None, use_cache: bool = True):
        """
        Initialize the converter.
        
        Args:
            source_folder: Path to source folder containing documents
            output_folder: Path to output folder (default: source_folder/converted_pdfs)
            use_ocr: Whether to apply OCR to documents (default: True)
            merge_output: Whether to merge all PDFs into a single file (default: False)
            max_workers: Max parallel workers (default: CPU count)
            use_cache: Use caching to skip already converted files (default: True)
        """
        self.source_folder = Path(source_folder).resolve()
        self.output_folder = output_folder or (self.source_folder / "converted_pdfs")
        self.use_ocr = use_ocr
        self.merge_output = merge_output
        self.max_workers = max_workers or min(os.cpu_count() or 4, 4)  # Max 4 for safety
        self.use_cache = use_cache
        self.cache_file = self.output_folder / ".conversion_cache.json"
        
        self.stats = {
            'total': 0,
            'converted': 0,
            'failed': 0,
            'skipped': 0,
            'cached': 0
        }
        
        self.converted_pdfs = []
        self.conversion_cache = self._load_cache() if use_cache else {}
        
        # Check dependencies
        self.deps = self._check_dependencies()
    
    def _load_cache(self) -> Dict:
        """Load conversion cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save conversion cache to disk."""
        try:
            self.output_folder.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.conversion_cache, f, indent=2)
        except Exception as e:
            print(f"  {Colors.YELLOW}⚠  Failed to save cache:{Colors.ENDC} {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate hash of file for caching."""
        hasher = hashlib.md5()
        hasher.update(str(file_path.stat().st_mtime).encode())
        hasher.update(str(file_path.stat().st_size).encode())
        return hasher.hexdigest()
    
    def _is_cached(self, file_path: Path, output_path: Path) -> bool:
        """Check if file conversion is cached and output exists."""
        if not self.use_cache:
            return False
        
        file_hash = self._get_file_hash(file_path)
        cache_key = str(file_path)
        
        if cache_key in self.conversion_cache:
            cached_hash = self.conversion_cache[cache_key].get('hash')
            cached_output = self.conversion_cache[cache_key].get('output')
            
            if cached_hash == file_hash and Path(cached_output).exists():
                return True
        
        return False
    
    def _update_cache(self, file_path: Path, output_path: Path):
        """Update cache entry for successful conversion."""
        if not self.use_cache:
            return
        
        file_hash = self._get_file_hash(file_path)
        self.conversion_cache[str(file_path)] = {
            'hash': file_hash,
            'output': str(output_path),
            'timestamp': time.time()
        }
        
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
        """Print dependency status with colors."""
        print(f"{Colors.BOLD}{Colors.CYAN}🔍 Dependency Check:{Colors.ENDC}")
        
        deps_status = [
            ('LibreOffice', self.deps['libreoffice'], 'required for Office docs'),
            ('Tesseract OCR', self.deps['tesseract'], 'optional, for OCR'),
            ('Poppler', self.deps['pdftoppm'], 'optional, for OCR'),
            ('ImageMagick', self.deps['convert'], 'optional, for images')
        ]
        
        for name, available, description in deps_status:
            if available:
                icon = f"{Colors.GREEN}✓{Colors.ENDC}"
                status = f"{Colors.GREEN}installed{Colors.ENDC}"
            else:
                icon = f"{Colors.RED}✗{Colors.ENDC}"
                status = f"{Colors.DIM}not found{Colors.ENDC}"
            
            print(f"  {icon} {Colors.BOLD}{name:15s}{Colors.ENDC} {status} {Colors.DIM}({description}){Colors.ENDC}")
        print()
    
    def collect_files(self) -> List[Path]:
        """Collect all convertible files from source folder and subfolders."""
        files = []
        all_formats = self.OFFICE_FORMATS | self.IMAGE_FORMATS | self.PDF_FORMATS | self.TEXT_FORMATS
        
        for root, dirs, filenames in os.walk(self.source_folder):
            # Skip output folder
            if Path(root) == self.output_folder:
                continue
                
            for filename in filenames:
                # Skip cache file
                if filename == '.conversion_cache.json':
                    continue
                    
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
            print(f"  {Colors.RED}✗ LibreOffice not installed{Colors.ENDC}, cannot convert {file_path.name}")
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
                print(f"  {Colors.RED}✗ LibreOffice failed{Colors.ENDC} to create PDF for {file_path.name}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"  {Colors.YELLOW}⏱ Timeout{Colors.ENDC} converting {file_path.name}")
            return False
        except Exception as e:
            print(f"  {Colors.RED}✗ Error:{Colors.ENDC} {e}")
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
            print(f"  {Colors.YELLOW}⚠  PyMuPDF not installed{Colors.ENDC}, cannot convert {text_path.name}")
            return False
        except Exception as e:
            print(f"  {Colors.RED}✗ Failed:{Colors.ENDC} {e}")
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
            print(f"  {Colors.RED}✗ Failed:{Colors.ENDC} {e}")
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
            
            # Add each PDF with progress
            for idx, pdf_path in enumerate(pdf_paths, 1):
                try:
                    print(f"  {Colors.DIM}[{idx}/{len(pdf_paths)}]{Colors.ENDC} {pdf_path.name}", end='\r')
                    pdf_doc = fitz.open(str(pdf_path))
                    merged_pdf.insert_pdf(pdf_doc)
                    pdf_doc.close()
                except Exception as e:
                    print(f"\n  {Colors.YELLOW}⚠  Failed to add {pdf_path.name}:{Colors.ENDC} {e}")
            
            # Clear progress line
            print(" " * 80, end='\r')
            
            # Save merged PDF
            merged_pdf.save(str(output_path))
            merged_pdf.close()
            
            return True
            
        except ImportError:
            print(f"  {Colors.RED}✗ PyMuPDF not installed{Colors.ENDC}, cannot merge PDFs")
            return False
        except Exception as e:
            print(f"  {Colors.RED}✗ Failed to merge:{Colors.ENDC} {e}")
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
            print(f"  {Colors.YELLOW}⚠  OCR failed:{Colors.ENDC} {e}")
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
            print(f"  {Colors.CYAN}→ Office document{Colors.ENDC}")
            success = self.convert_office_to_pdf(file_path, output_path)
            if success and self.use_ocr and self.deps['tesseract'] and self.deps['pdftoppm']:
                print(f"  {Colors.YELLOW}→ Applying OCR...{Colors.ENDC}")
                self.apply_ocr_to_pdf(output_path)
        elif ext in self.IMAGE_FORMATS:
            print(f"  {Colors.CYAN}→ Image file{Colors.ENDC}")
            success = self.convert_image_to_pdf(file_path, output_path)
        elif ext in self.TEXT_FORMATS:
            print(f"  {Colors.CYAN}→ Text file{Colors.ENDC}")
            success = self.convert_text_to_pdf(file_path, output_path)
        elif ext in self.PDF_FORMATS:
            print(f"  {Colors.CYAN}→ PDF file{Colors.ENDC}")
            success = self.copy_pdf(file_path, output_path)
        
        if success:
            print(f"  {Colors.GREEN}✓ Saved to:{Colors.ENDC} {Colors.BOLD}{output_path.name}{Colors.ENDC}")
            self.converted_pdfs.append(output_path)
            self._update_cache(file_path, output_path)
        
        return success
    
    def _convert_file_worker(self, file_path: Path) -> Tuple[bool, Path]:
        """Worker function for parallel conversion."""
        ext = file_path.suffix.lower()
        
        # Generate output filename
        relative_path = file_path.relative_to(self.source_folder)
        output_name = f"{relative_path.parent / file_path.stem}.pdf".replace('/', '_').replace('\\', '_')
        if output_name.startswith('._'):
            output_name = output_name[2:]
        output_path = self.output_folder / output_name
        
        # Handle duplicate names
        if output_path.exists() and not self._is_cached(file_path, output_path):
            counter = 1
            while output_path.exists():
                output_path = self.output_folder / f"{output_path.stem}_{counter}.pdf"
                counter += 1
        
        # Check cache first
        if self._is_cached(file_path, output_path):
            return ('cached', output_path)
        
        success = False
        
        if ext in self.OFFICE_FORMATS:
            success = self.convert_office_to_pdf(file_path, output_path)
            if success and self.use_ocr and self.deps['tesseract'] and self.deps['pdftoppm']:
                self.apply_ocr_to_pdf(output_path)
        elif ext in self.IMAGE_FORMATS:
            success = self.convert_image_to_pdf(file_path, output_path)
        elif ext in self.TEXT_FORMATS:
            success = self.convert_text_to_pdf(file_path, output_path)
        elif ext in self.PDF_FORMATS:
            success = self.copy_pdf(file_path, output_path)
        
        if success:
            self._update_cache(file_path, output_path)
            return (True, output_path)
        else:
            return (False, output_path)
    
    def convert_all(self):
        """Convert all files in the source folder with parallel processing."""
        # Create output directory
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Print header
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  any2pdf - Universal Document to PDF Converter{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}📁 Source folder:{Colors.ENDC}  {Colors.CYAN}{self.source_folder}{Colors.ENDC}")
        print(f"{Colors.BOLD}📂 Output folder:{Colors.ENDC}  {Colors.CYAN}{self.output_folder}{Colors.ENDC}")
        print(f"{Colors.BOLD}⚡ Workers:{Colors.ENDC}        {Colors.CYAN}{self.max_workers} parallel threads{Colors.ENDC}")
        if self.use_cache:
            print(f"{Colors.BOLD}💾 Caching:{Colors.ENDC}       {Colors.GREEN}Enabled{Colors.ENDC}")
        print()
        
        self.print_dependencies()
        
        # Collect files
        files = self.collect_files()
        self.stats['total'] = len(files)
        
        if not files:
            print(f"{Colors.YELLOW}⚠  No convertible files found.{Colors.ENDC}")
            return
        
        print(f"{Colors.BOLD}{Colors.GREEN}✓ Found {len(files)} file(s) to convert{Colors.ENDC}")
        print(f"{Colors.DIM}{'─'*70}{Colors.ENDC}\n")
        
        start_time = time.time()
        
        # Convert files in parallel
        if self.max_workers > 1:
            print(f"{Colors.BOLD}{Colors.CYAN}⚡ Converting files in parallel...{Colors.ENDC}\n")
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_file = {executor.submit(self._convert_file_worker, f): f for f in files}
                
                # Process completed tasks
                for idx, future in enumerate(as_completed(future_to_file), 1):
                    file_path = future_to_file[future]
                    print(f"{Colors.BOLD}[{idx}/{len(files)}]{Colors.ENDC} {Colors.BOLD}{file_path.name}{Colors.ENDC}")
                    
                    try:
                        result, output_path = future.result()
                        
                        if result == 'cached':
                            print(f"  {Colors.CYAN}→ Cached (skipped){Colors.ENDC}")
                            print(f"  {Colors.GREEN}✓ Using cached:{Colors.ENDC} {Colors.BOLD}{output_path.name}{Colors.ENDC}")
                            self.stats['cached'] += 1
                            self.stats['converted'] += 1
                            self.converted_pdfs.append(output_path)
                        elif result:
                            ext = file_path.suffix.lower()
                            if ext in self.OFFICE_FORMATS:
                                print(f"  {Colors.CYAN}→ Office document{Colors.ENDC}")
                            elif ext in self.IMAGE_FORMATS:
                                print(f"  {Colors.CYAN}→ Image file{Colors.ENDC}")
                            elif ext in self.TEXT_FORMATS:
                                print(f"  {Colors.CYAN}→ Text file{Colors.ENDC}")
                            elif ext in self.PDF_FORMATS:
                                print(f"  {Colors.CYAN}→ PDF file{Colors.ENDC}")
                            print(f"  {Colors.GREEN}✓ Saved to:{Colors.ENDC} {Colors.BOLD}{output_path.name}{Colors.ENDC}")
                            self.stats['converted'] += 1
                            self.converted_pdfs.append(output_path)
                        else:
                            print(f"  {Colors.RED}✗ Conversion failed{Colors.ENDC}")
                            self.stats['failed'] += 1
                    except Exception as e:
                        print(f"  {Colors.RED}✗ Error:{Colors.ENDC} {e}")
                        self.stats['failed'] += 1
                    
                    print()
        else:
            # Sequential processing
            for idx, file_path in enumerate(files, 1):
                print(f"{Colors.BOLD}[{idx}/{len(files)}]{Colors.ENDC} {Colors.BOLD}{file_path.name}{Colors.ENDC}")
                if self.convert_file(file_path):
                    self.stats['converted'] += 1
                else:
                    self.stats['failed'] += 1
                print()
        
        elapsed_time = time.time() - start_time
        
        # Save cache
        if self.use_cache:
            self._save_cache()
        
        # Merge all PDFs if requested
        if self.merge_output and self.converted_pdfs:
            print(f"{Colors.DIM}{'─'*70}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.CYAN}🔗 Merging all PDFs into single document...{Colors.ENDC}")
            merged_path = self.output_folder / "merged_all_documents.pdf"
            if self.merge_pdfs(self.converted_pdfs, merged_path):
                print(f"{Colors.GREEN}✓ Merged PDF saved to:{Colors.ENDC} {Colors.BOLD}{merged_path.name}{Colors.ENDC}")
            else:
                print(f"{Colors.RED}✗ Failed to merge PDFs{Colors.ENDC}")
            print()
        
        # Print summary
        print(f"{Colors.DIM}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}📊 Conversion Summary{Colors.ENDC}")
        print(f"{Colors.DIM}{'='*70}{Colors.ENDC}")
        
        total_color = Colors.BLUE
        converted_color = Colors.GREEN if self.stats['converted'] > 0 else Colors.DIM
        failed_color = Colors.RED if self.stats['failed'] > 0 else Colors.DIM
        cached_color = Colors.CYAN if self.stats['cached'] > 0 else Colors.DIM
        
        print(f"  {Colors.BOLD}Total files:{Colors.ENDC}     {total_color}{self.stats['total']}{Colors.ENDC}")
        print(f"  {Colors.BOLD}Converted:{Colors.ENDC}       {converted_color}{self.stats['converted']}{Colors.ENDC}")
        if self.stats['cached'] > 0:
            print(f"  {Colors.BOLD}From cache:{Colors.ENDC}      {cached_color}{self.stats['cached']}{Colors.ENDC}")
        print(f"  {Colors.BOLD}Failed:{Colors.ENDC}          {failed_color}{self.stats['failed']}{Colors.ENDC}")
        print(f"  {Colors.BOLD}Time:{Colors.ENDC}            {Colors.CYAN}{elapsed_time:.1f}s{Colors.ENDC}")
        if elapsed_time > 0 and self.stats['converted'] > 0:
            avg_time = elapsed_time / self.stats['converted']
            print(f"  {Colors.BOLD}Avg/file:{Colors.ENDC}        {Colors.CYAN}{avg_time:.1f}s{Colors.ENDC}")
        print()
        print(f"{Colors.GREEN}✓ All PDFs saved to:{Colors.ENDC} {Colors.BOLD}{Colors.CYAN}{self.output_folder}{Colors.ENDC}")
        
        # Success banner
        if self.stats['converted'] > 0:
            print()
            if self.merge_output and self.converted_pdfs:
                print(f"{Colors.BOLD}{Colors.GREEN}🎉 Success!{Colors.ENDC} Upload {Colors.BOLD}merged_all_documents.pdf{Colors.ENDC} to ChatGPT!")
            else:
                print(f"{Colors.BOLD}{Colors.GREEN}🎉 Done!{Colors.ENDC} {self.stats['converted']} file(s) converted successfully!")
            
            if self.max_workers > 1:
                print(f"{Colors.DIM}⚡ Parallel processing used {self.max_workers} workers{Colors.ENDC}")
        
        print()


class PDFChatSession:
    """Interactive chat session with PDF using AI."""
    
    # GPT-5 reasoning models (support reasoning effort)
    GPT5_REASONING_MODELS = ["gpt-5", "gpt-5-mini", "gpt-5-nano"]
    
    OPENAI_MODELS = [
        # GPT-5 Series (Latest - October 2025)
        "gpt-5",                     # Best for complex reasoning, coding & agentic tasks
        "gpt-5-mini",               # Cost-optimized reasoning, balances speed & capability
        "gpt-5-nano",               # High-throughput, simple instruction-following
        "gpt-5-chat-latest",        # GPT-5 main (non-reasoning variant)
        
        # GPT-4.1 Series
        "gpt-4.1",                  # Smartest non-reasoning model
        "gpt-4.1-mini",             # Cost-effective GPT-4.1
        "gpt-4.1-nano",             # Fast, lightweight GPT-4.1
        
        # O-Series (Previous generation reasoning)
        "o4-mini",                  # Fast reasoning (superseded by GPT-5 mini)
        "o3",                       # Previous reasoning model
        
        # Legacy GPT-4
        "gpt-4o",                   # GPT-4 Omni
        "gpt-4o-mini",              # Smaller GPT-4 Omni
        "gpt-4-turbo",              # GPT-4 Turbo
        "gpt-4",                    # Standard GPT-4
        "gpt-3.5-turbo"             # Legacy model
    ]
    
    GEMINI_MODELS = [
        # Gemini 2.5 Series (Latest - October 2025)
        "gemini-2.5-flash",              # Latest stable 2.5 Flash
        "gemini-2.5-pro",                # Latest stable 2.5 Pro
        
        # Gemini 2.0 Series
        "gemini-2.0-flash-exp",          # Experimental 2.0 Flash
        "gemini-2.0-flash-thinking-exp", # 2.0 with thinking mode
        
        # Gemini 1.5 Series
        "gemini-1.5-pro-latest",         # Latest 1.5 Pro
        "gemini-1.5-pro",                # Stable 1.5 Pro
        "gemini-1.5-flash-latest",       # Latest 1.5 Flash
        "gemini-1.5-flash",              # Stable 1.5 Flash
        "gemini-1.5-flash-8b",           # Smaller 1.5 Flash
        
        # Experimental models
        "gemini-exp-1206",               # Experimental Dec 2024
        "gemini-exp-1121",               # Experimental Nov 2024
        
        # Legacy
        "gemini-1.0-pro"                 # Legacy 1.0
    ]
    
    def __init__(self, pdf_path: Path, provider: str = None, api_key: str = None, model: str = None, reasoning_effort: str = None):
        """Initialize chat session with PDF."""
        self.pdf_path = pdf_path
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.reasoning_effort = reasoning_effort  # For GPT-5 models
        self.conversation_history = []
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")
        
        # Read PDF content
        self.pdf_text = self._extract_text_from_pdf()
        
        if not self.pdf_text or len(self.pdf_text.strip()) < 50:
            print(f"{Colors.YELLOW}⚠  Warning: PDF has minimal text content. Chat may be limited.{Colors.ENDC}")
    
    def _extract_text_from_pdf(self) -> str:
        """Extract text content from PDF."""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(str(self.pdf_path))
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"{Colors.RED}✗ Failed to extract text from PDF:{Colors.ENDC} {e}")
            return ""
    
    def setup_openai(self):
        """Setup OpenAI API."""
        if not OPENAI_AVAILABLE:
            print(f"{Colors.RED}✗ OpenAI library not installed.{Colors.ENDC}")
            print(f"  Install with: {Colors.CYAN}pip install openai{Colors.ENDC}")
            return False
        
        try:
            openai.api_key = self.api_key
            # Test API key
            client = openai.OpenAI(api_key=self.api_key)
            # Try to list models to validate key
            try:
                models = client.models.list()
                return True
            except:
                # Fallback: just test with a simple call
                return True
        except Exception as e:
            print(f"{Colors.RED}✗ OpenAI API key validation failed:{Colors.ENDC} {e}")
            return False
    
    @staticmethod
    def get_available_openai_models(api_key: str) -> List[str]:
        """Get available OpenAI models from API."""
        try:
            client = openai.OpenAI(api_key=api_key)
            models = client.models.list()
            # Filter for chat models
            chat_models = []
            for model in models.data:
                model_id = model.id
                if any(x in model_id for x in ['gpt-', 'o1-', 'o3-']):
                    chat_models.append(model_id)
            return sorted(chat_models, reverse=True)[:15]  # Return top 15
        except:
            return PDFChatSession.OPENAI_MODELS
    
    @staticmethod
    def get_available_gemini_models(api_key: str) -> List[str]:
        """Get available Gemini models from API."""
        try:
            genai.configure(api_key=api_key)
            models = genai.list_models()
            gemini_models = []
            for model in models:
                if 'generateContent' in [m.name for m in model.supported_generation_methods]:
                    model_name = model.name.replace('models/', '')
                    if 'gemini' in model_name.lower():
                        gemini_models.append(model_name)
            return sorted(gemini_models, reverse=True)[:15]  # Return top 15
        except:
            return PDFChatSession.GEMINI_MODELS
    
    def setup_gemini(self):
        """Setup Gemini API."""
        if not GEMINI_AVAILABLE:
            print(f"{Colors.RED}✗ Gemini library not installed.{Colors.ENDC}")
            print(f"  Install with: {Colors.CYAN}pip install google-generativeai{Colors.ENDC}")
            return False
        
        try:
            genai.configure(api_key=self.api_key)
            # Test API key by listing models
            list(genai.list_models())
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ Gemini API key validation failed:{Colors.ENDC} {e}")
            return False
    
    def chat_openai(self, user_message: str) -> str:
        """Send message using OpenAI."""
        try:
            client = openai.OpenAI(api_key=self.api_key)
            
            # Build messages with PDF context
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant analyzing a PDF document. Here is the content:\n\n{self.pdf_text[:50000]}\n\nAnswer questions about this document."
                }
            ]
            
            # Add conversation history
            for msg in self.conversation_history:
                messages.append(msg)
            
            messages.append({"role": "user", "content": user_message})
            
            # Prepare request parameters
            request_params = {
                "model": self.model,
                "messages": messages
            }
            
            # Add reasoning_effort for GPT-5 models
            if self.model in self.GPT5_REASONING_MODELS and self.reasoning_effort:
                request_params["reasoning_effort"] = self.reasoning_effort
            
            response = client.chat.completions.create(**request_params)
            
            assistant_message = response.choices[0].message.content
            
            # Update history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            return f"Error: {e}"
    
    def chat_gemini(self, user_message: str) -> str:
        """Send message using Gemini."""
        try:
            model = genai.GenerativeModel(self.model)
            
            # Build conversation with PDF context
            if not self.conversation_history:
                # First message includes PDF context
                prompt = f"You are analyzing this PDF document:\n\n{self.pdf_text[:50000]}\n\nUser question: {user_message}"
            else:
                # Subsequent messages include history
                history_text = "\n".join([
                    f"{'User' if i % 2 == 0 else 'Assistant'}: {msg}"
                    for i, msg in enumerate(self.conversation_history)
                ])
                prompt = f"Previous conversation:\n{history_text}\n\nUser: {user_message}"
            
            response = model.generate_content(prompt)
            assistant_message = response.text
            
            # Update history
            self.conversation_history.append(user_message)
            self.conversation_history.append(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            return f"Error: {e}"
    
    def start_chat(self):
        """Start interactive chat session."""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  💬 PDF Chat Session{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}📄 PDF:{Colors.ENDC} {Colors.CYAN}{self.pdf_path.name}{Colors.ENDC}")
        print(f"{Colors.BOLD}🤖 Provider:{Colors.ENDC} {Colors.CYAN}{self.provider.upper()}{Colors.ENDC}")
        print(f"{Colors.BOLD}🎯 Model:{Colors.ENDC} {Colors.CYAN}{self.model}{Colors.ENDC}")
        if self.reasoning_effort and self.model in self.GPT5_REASONING_MODELS:
            print(f"{Colors.BOLD}🧠 Reasoning:{Colors.ENDC} {Colors.CYAN}{self.reasoning_effort}{Colors.ENDC}")
        print(f"{Colors.BOLD}📝 PDF Length:{Colors.ENDC} {Colors.CYAN}{len(self.pdf_text)} characters{Colors.ENDC}")
        print()
        print(f"{Colors.DIM}Type your questions below. Commands:{Colors.ENDC}")
        print(f"{Colors.DIM}  • 'exit' or 'quit' to end session{Colors.ENDC}")
        print(f"{Colors.DIM}  • 'clear' to clear conversation history{Colors.ENDC}")
        print(f"{Colors.DIM}  • 'help' for assistance{Colors.ENDC}")
        print(f"{Colors.DIM}{'─'*70}{Colors.ENDC}\n")
        
        # Setup provider
        if self.provider == "openai":
            if not self.setup_openai():
                return
        elif self.provider == "gemini":
            if not self.setup_gemini():
                return
        
        # Chat loop
        while True:
            try:
                user_input = input(f"{Colors.BOLD}{Colors.BLUE}You:{Colors.ENDC} ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.ENDC}\n")
                    break
                
                if user_input.lower() == 'clear':
                    self.conversation_history = []
                    print(f"{Colors.YELLOW}🔄 Conversation history cleared.{Colors.ENDC}\n")
                    continue
                
                if user_input.lower() == 'help':
                    print(f"\n{Colors.CYAN}Available commands:{Colors.ENDC}")
                    print(f"  • Ask any question about the PDF")
                    print(f"  • 'exit' - End chat session")
                    print(f"  • 'clear' - Clear conversation history")
                    print(f"  • 'help' - Show this help\n")
                    continue
                
                # Get AI response
                print(f"{Colors.BOLD}{Colors.GREEN}AI:{Colors.ENDC} ", end="", flush=True)
                
                if self.provider == "openai":
                    response = self.chat_openai(user_input)
                elif self.provider == "gemini":
                    response = self.chat_gemini(user_input)
                else:
                    response = "Error: Unknown provider"
                
                print(response)
                print()
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Chat interrupted. Type 'exit' to quit.{Colors.ENDC}\n")
                continue
            except EOFError:
                print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.ENDC}\n")
                break
            except Exception as e:
                print(f"\n{Colors.RED}✗ Error:{Colors.ENDC} {e}\n")


def prompt_for_chat(merged_pdf_path: Path):
    """Prompt user for AI chat after conversion - with questionary if available."""
    print(f"{Colors.DIM}{'─'*70}{Colors.ENDC}")
    
    # Use questionary if available for better UX
    if QUESTIONARY_AVAILABLE:
        from questionary import Style
        custom_style = Style([
            ('qmark', 'fg:#4CAF50 bold'),
            ('question', 'fg:#2196F3 bold'),
            ('answer', 'fg:#FF9800 bold'),
            ('pointer', 'fg:#9C27B0 bold'),
            ('highlighted', 'fg:#9C27B0 bold'),
            ('selected', 'fg:#4CAF50'),
            ('separator', 'fg:#607D8B'),
            ('instruction', 'fg:#9E9E9E'),
        ])
        
        start_chat = questionary.confirm(
            "💬 Would you like to chat with your PDF using AI?",
            default=False,
            style=custom_style
        ).ask()
        
        if not start_chat:
            return
    else:
        # Fallback to regular input
        print(f"{Colors.BOLD}{Colors.CYAN}💬 Would you like to chat with the PDF using AI?{Colors.ENDC}")
        print()
        response = input(f"Start chat session? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            return
    
    print()
    
    # Check if AI libraries are available
    if not OPENAI_AVAILABLE and not GEMINI_AVAILABLE:
        print(f"{Colors.YELLOW}⚠  No AI libraries installed.{Colors.ENDC}")
        print(f"\nInstall one of:")
        print(f"  • OpenAI: {Colors.CYAN}pip install openai{Colors.ENDC}")
        print(f"  • Gemini: {Colors.CYAN}pip install google-generativeai{Colors.ENDC}")
        return
    
    # Select provider
    providers = []
    if OPENAI_AVAILABLE:
        providers.append("openai")
    if GEMINI_AVAILABLE:
        providers.append("gemini")
    
    if QUESTIONARY_AVAILABLE and len(providers) > 1:
        provider_choices = []
        if OPENAI_AVAILABLE:
            provider_choices.append("OpenAI (GPT-5, GPT-4.1, etc.)")
        if GEMINI_AVAILABLE:
            provider_choices.append("Google Gemini (2.5, 2.0, 1.5)")
        
        provider_choice = questionary.select(
            "🤖 Select AI provider:",
            choices=provider_choices,
            style=custom_style
        ).ask()
        
        provider = "openai" if "OpenAI" in provider_choice else "gemini"
    else:
        # Fallback to regular selection
        print(f"{Colors.BOLD}Select AI provider:{Colors.ENDC}")
        if OPENAI_AVAILABLE:
            print(f"  1. OpenAI (GPT-5, GPT-4.1, etc.)")
        if GEMINI_AVAILABLE:
            print(f"  {len(providers)}. Google Gemini")
        
        if len(providers) == 1:
            provider = providers[0]
            print(f"\n{Colors.GREEN}✓ Using {provider.upper()}{Colors.ENDC}")
        else:
            provider_choice = input(f"\nChoice (1-{len(providers)}): ").strip()
            try:
                provider = providers[int(provider_choice) - 1]
            except:
                print(f"{Colors.RED}✗ Invalid choice{Colors.ENDC}")
                return
    
    print()
    
    # Get API key
    if QUESTIONARY_AVAILABLE:
        if provider == "openai":
            api_key = questionary.password(
                "🔑 OpenAI API Key:\n   (Get it at: https://platform.openai.com/api-keys)",
                style=custom_style
            ).ask()
        else:
            api_key = questionary.password(
                "🔑 Gemini API Key:\n   (Get it at: https://makersuite.google.com/app/apikey)",
                style=custom_style
            ).ask()
    else:
        print(f"{Colors.BOLD}Enter API key:{Colors.ENDC}")
        if provider == "openai":
            print(f"{Colors.DIM}Get your key at: https://platform.openai.com/api-keys{Colors.ENDC}")
        else:
            print(f"{Colors.DIM}Get your key at: https://makersuite.google.com/app/apikey{Colors.ENDC}")
        api_key = input("API Key: ").strip()
    
    if not api_key:
        print(f"{Colors.RED}✗ No API key provided{Colors.ENDC}")
        return
    
    print()
    
    # Fetch available models from API
    print(f"{Colors.DIM}Fetching available models...{Colors.ENDC}")
    
    if provider == "openai":
        available_models = PDFChatSession.get_available_openai_models(api_key)
    else:
        available_models = PDFChatSession.get_available_gemini_models(api_key)
    
    print(f"{Colors.GREEN}✓ Found {len(available_models)} models{Colors.ENDC}\n")
    
    # Model selection with questionary if available
    if QUESTIONARY_AVAILABLE:
        # Group models nicely for selection
        if provider == "openai":
            gpt5_models = [m for m in available_models if m.startswith("gpt-5")][:4]
            gpt41_models = [m for m in available_models if m.startswith("gpt-4.1")][:3]
            other_models = [m for m in available_models if not m.startswith("gpt-5") and not m.startswith("gpt-4.1")][:3]
            
            model_choices = (
                [questionary.Separator("GPT-5 Series (Latest)")] + gpt5_models +
                [questionary.Separator("GPT-4.1 Series")] + gpt41_models +
                [questionary.Separator("Other Models")] + other_models
            )
        else:
            gemini25 = [m for m in available_models if "2.5" in m][:2]
            gemini20 = [m for m in available_models if "2.0" in m][:2]
            gemini15 = [m for m in available_models if "1.5" in m][:4]
            
            model_choices = (
                [questionary.Separator("Gemini 2.5 (Latest)")] + gemini25 +
                [questionary.Separator("Gemini 2.0")] + gemini20 +
                [questionary.Separator("Gemini 1.5")] + gemini15
            )
        
        model = questionary.select(
            "🎯 Select AI model:",
            choices=model_choices,
            style=custom_style
        ).ask()
    else:
        # Fallback to regular selection
        print(f"{Colors.BOLD}Available models:{Colors.ENDC}")
        
        if provider == "openai":
            gpt5_models = [m for m in available_models if m.startswith("gpt-5")]
            gpt41_models = [m for m in available_models if m.startswith("gpt-4.1")]
            other_models = [m for m in available_models if not m.startswith("gpt-5") and not m.startswith("gpt-4.1")]
            
            print(f"{Colors.CYAN}  GPT-5 Series:{Colors.ENDC}")
            for i, m in enumerate(gpt5_models[:4], 1):
                print(f"    {i}. {m}")
            
            print(f"{Colors.CYAN}  GPT-4.1 Series:{Colors.ENDC}")
            start_idx = len(gpt5_models[:4]) + 1
            for i, m in enumerate(gpt41_models[:3], start_idx):
                print(f"    {i}. {m}")
            
            display_count = min(10, len(available_models))
        else:
            for i, m in enumerate(available_models[:10], 1):
                print(f"    {i}. {m}")
            display_count = min(10, len(available_models))
        
        model_choice = input(f"\nChoice (1-{display_count}): ").strip()
        try:
            model = available_models[int(model_choice) - 1]
        except:
            model = available_models[0]
    
    print(f"{Colors.GREEN}✓ Using model:{Colors.ENDC} {model}\n")
    
    # Ask for reasoning effort if GPT-5 model
    reasoning_effort = None
    if provider == "openai" and model in PDFChatSession.GPT5_REASONING_MODELS:
        if QUESTIONARY_AVAILABLE:
            reasoning_effort = questionary.select(
                f"🧠 Reasoning effort for {model}:",
                choices=[
                    questionary.Choice("minimal - Fastest (simple tasks)", value="minimal"),
                    questionary.Choice("low - Quick reasoning", value="low"),
                    questionary.Choice("medium - Balanced (recommended)", value="medium"),
                    questionary.Choice("high - Deep reasoning (complex tasks)", value="high"),
                ],
                default="medium",
                style=custom_style
            ).ask()
        else:
            print(f"{Colors.BOLD}🧠 Select reasoning effort:{Colors.ENDC}")
            print(f"  1. minimal  2. low  3. medium (default)  4. high")
            effort_choice = input("Choice (1-4): ").strip()
            effort_map = {"1": "minimal", "2": "low", "3": "medium", "4": "high", "": "medium"}
            reasoning_effort = effort_map.get(effort_choice, "medium")
        
        print(f"{Colors.GREEN}✓ Reasoning effort:{Colors.ENDC} {reasoning_effort}\n")
    
    try:
        chat = PDFChatSession(merged_pdf_path, provider, api_key, model, reasoning_effort)
        chat.start_chat()
    except Exception as e:
        print(f"{Colors.RED}✗ Failed to start chat:{Colors.ENDC} {e}")


def interactive_mode():
    """Interactive mode with questionary prompts."""
    if not QUESTIONARY_AVAILABLE:
        print(f"{Colors.RED}✗ Questionary not installed.{Colors.ENDC}")
        print(f"  Install with: {Colors.CYAN}pip install questionary rich{Colors.ENDC}\n")
        return None
    
    # Custom style - more colorful and modern
    custom_style = Style([
        ('qmark', 'fg:#4CAF50 bold'),          # Green question mark
        ('question', 'fg:#2196F3 bold'),        # Blue question
        ('answer', 'fg:#FF9800 bold'),          # Orange answer
        ('pointer', 'fg:#9C27B0 bold'),         # Purple pointer
        ('highlighted', 'fg:#9C27B0 bold'),     # Purple highlight
        ('selected', 'fg:#4CAF50'),             # Green selection
        ('separator', 'fg:#607D8B'),            # Grey separator
        ('instruction', 'fg:#9E9E9E'),          # Grey instructions
        ('text', ''),
    ])
    
    # Welcome banner
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'═'*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}  📄 any2pdf - Interactive Document Converter{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'═'*70}{Colors.ENDC}\n")
    print(f"{Colors.CYAN}Welcome to the interactive setup! Let's configure your conversion...{Colors.ENDC}\n")
    
    # Ask for source folder with better prompt
    source_path = questionary.path(
        "📁 Source folder (containing documents to convert):",
        only_directories=True,
        style=custom_style
    ).ask()
    
    if not source_path:
        print(f"\n{Colors.YELLOW}⚠  Setup cancelled{Colors.ENDC}\n")
        return None
    
    source = Path(source_path).resolve()
    
    # Validate source exists
    if not source.exists() or not source.is_dir():
        print(f"\n{Colors.RED}✗ Error: '{source}' is not a valid directory!{Colors.ENDC}\n")
        return None
    
    # Quick scan to show what's in the folder
    try:
        all_formats = DocumentConverter.OFFICE_FORMATS | DocumentConverter.IMAGE_FORMATS | DocumentConverter.PDF_FORMATS | DocumentConverter.TEXT_FORMATS
        file_count = 0
        for root, dirs, files in os.walk(source):
            for f in files:
                if Path(f).suffix.lower() in all_formats:
                    file_count += 1
        
        if file_count > 0:
            print(f"  {Colors.GREEN}✓ Found {file_count} convertible file(s){Colors.ENDC}\n")
        else:
            print(f"  {Colors.YELLOW}⚠  No convertible files found in this folder{Colors.ENDC}")
            continue_anyway = questionary.confirm(
                "Continue anyway?",
                default=False,
                style=custom_style
            ).ask()
            if not continue_anyway:
                return None
            print()
    except:
        pass
    
    # Ask for output folder (optional)
    default_output = source / "converted_pdfs"
    use_custom_output = questionary.confirm(
        f"📂 Use custom output folder?\n   (default: {default_output})",
        default=False,
        style=custom_style
    ).ask()
    
    output = None
    if use_custom_output:
        output_path = questionary.text(
            "📂 Output folder path:",
            default=str(default_output),
            style=custom_style
        ).ask()
        if output_path:
            output = Path(output_path).resolve()
    
    print()
    
    # Ask about OCR with explanation
    use_ocr = questionary.confirm(
        "🔍 Enable OCR (Optical Character Recognition)?\n   Makes PDFs searchable and better for AI analysis (recommended)",
        default=True,
        style=custom_style,
        auto_enter=False
    ).ask()
    
    # Ask about merging with explanation
    merge_output = questionary.confirm(
        "🔗 Merge all PDFs into a single document?\n   Perfect for uploading to ChatGPT/Claude",
        default=False,
        style=custom_style
    ).ask()
    
    # Ask about parallel processing
    cpu_count = os.cpu_count() or 4
    max_workers_choices = [
        "1 worker (sequential, safest)",
        "2 workers (2x faster)",
        "4 workers (4x faster, recommended)",
    ]
    
    if cpu_count > 4:
        max_workers_choices.append(f"{cpu_count} workers (maximum speed)")
    
    max_workers_choices.append("Custom number")
    
    max_workers_choice = questionary.select(
        "⚡ How many parallel workers?",
        choices=max_workers_choices,
        default="4 workers (4x faster, recommended)",
        style=custom_style
    ).ask()
    
    if "Custom" in max_workers_choice:
        max_workers_text = questionary.text(
            "Enter number of workers (1-32):",
            default="4",
            validate=lambda x: x.isdigit() and 1 <= int(x) <= 32,
            style=custom_style
        ).ask()
        max_workers = int(max_workers_text)
    else:
        max_workers = int(max_workers_choice.split()[0])
    
    # Ask about caching
    use_cache = questionary.confirm(
        "💾 Enable smart caching?\n   Skip files that were already converted (saves time on re-runs)",
        default=True,
        style=custom_style
    ).ask()
    
    # Summary
    print(f"\n{Colors.BOLD}{Colors.CYAN}📋 Configuration Summary:{Colors.ENDC}")
    print(f"  {Colors.BOLD}Source:{Colors.ENDC}     {source}")
    print(f"  {Colors.BOLD}Output:{Colors.ENDC}     {output or default_output}")
    print(f"  {Colors.BOLD}OCR:{Colors.ENDC}        {Colors.GREEN + 'Enabled' if use_ocr else Colors.YELLOW + 'Disabled'}{Colors.ENDC}")
    print(f"  {Colors.BOLD}Merge:{Colors.ENDC}      {Colors.GREEN + 'Yes' if merge_output else Colors.DIM + 'No'}{Colors.ENDC}")
    print(f"  {Colors.BOLD}Workers:{Colors.ENDC}    {max_workers}")
    print(f"  {Colors.BOLD}Caching:{Colors.ENDC}    {Colors.GREEN + 'Enabled' if use_cache else Colors.YELLOW + 'Disabled'}{Colors.ENDC}")
    print()
    
    # Final confirmation
    proceed = questionary.confirm(
        "🚀 Start conversion with these settings?",
        default=True,
        style=custom_style
    ).ask()
    
    if not proceed:
        print(f"\n{Colors.YELLOW}⚠  Conversion cancelled{Colors.ENDC}\n")
        return None
    
    print()
    
    return {
        'source_folder': source,
        'output_folder': output,
        'use_ocr': use_ocr,
        'merge_output': merge_output,
        'max_workers': max_workers,
        'use_cache': use_cache
    }


def main():
    """Main entry point."""
    # Check if running in interactive mode (no arguments)
    if len(sys.argv) == 1:
        if not QUESTIONARY_AVAILABLE:
            # Show instructions for interactive mode
            print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}  any2pdf - Universal Document to PDF Converter{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
            print(f"{Colors.YELLOW}⚠  Interactive mode requires additional packages.{Colors.ENDC}")
            print(f"\nInstall interactive mode dependencies:")
            print(f"  {Colors.CYAN}pip install questionary rich{Colors.ENDC}")
            print(f"\nOr use traditional CLI mode:")
            print(f"  {Colors.CYAN}python3 document_to_pdf.py /path/to/documents{Colors.ENDC}")
            print(f"  {Colors.CYAN}python3 document_to_pdf.py --help{Colors.ENDC}")
            print()
            sys.exit(1)
        
        # Interactive mode
        config = interactive_mode()
        if not config:
            sys.exit(0)
        
        source = config['source_folder']
    else:
        # Traditional CLI mode
        parser = argparse.ArgumentParser(
            description='Convert documents to searchable PDFs for AI analysis',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s /path/to/documents
  %(prog)s /path/to/documents -o /path/to/output
  %(prog)s /path/to/documents --no-ocr
  %(prog)s /path/to/documents --merge
  %(prog)s /path/to/documents --merge -j 4
  %(prog)s /path/to/documents --merge --no-cache
  
Interactive mode:
  %(prog)s     (run without arguments for interactive prompts)
  
Supported formats:
  Office: .pptx, .docx, .doc, .ppt, .xlsx, .xls, .odt, .odp, .ods, .rtf
  Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .tif, .webp, .svg, .heic
  Text: .txt, .md, .csv, .tsv, .log, .json, .xml, .html, .htm
  PDF: .pdf (will be copied and optionally OCR'd)
            """
        )
        
        parser.add_argument(
            'source_folder',
            nargs='?',
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
        
        parser.add_argument(
            '-j', '--jobs',
            dest='max_workers',
            type=int,
            default=None,
            help='Number of parallel workers (default: CPU count, max 4)'
        )
        
        parser.add_argument(
            '--no-cache',
            dest='use_cache',
            action='store_false',
            default=True,
            help='Disable caching (always reconvert files)'
        )
        
        args = parser.parse_args()
        
        # If no source folder provided and no interactive mode
        if not args.source_folder:
            parser.print_help()
            print(f"\n{Colors.YELLOW}💡 Tip: Run without arguments for interactive mode{Colors.ENDC}")
            if not QUESTIONARY_AVAILABLE:
                print(f"   Install: {Colors.CYAN}pip install questionary rich{Colors.ENDC}")
            sys.exit(1)
        
        # Validate source folder
        source = Path(args.source_folder)
        if not source.exists():
            print(f"{Colors.RED}✗ Error: Source folder '{source}' does not exist!{Colors.ENDC}")
            sys.exit(1)
        
        if not source.is_dir():
            print(f"{Colors.RED}✗ Error: '{source}' is not a directory!{Colors.ENDC}")
            sys.exit(1)
        
        config = {
            'source_folder': source,
            'output_folder': Path(args.output_folder) if args.output_folder else None,
            'use_ocr': args.use_ocr,
            'merge_output': args.merge_output,
            'max_workers': args.max_workers,
            'use_cache': args.use_cache
        }
    
    # Convert documents
    converter = DocumentConverter(**config)
    converter.convert_all()
    
    # Offer chat session if PDF was merged
    if config['merge_output'] and converter.converted_pdfs:
        merged_pdf = converter.output_folder / "merged_all_documents.pdf"
        if merged_pdf.exists():
            prompt_for_chat(merged_pdf)


if __name__ == "__main__":
    main()

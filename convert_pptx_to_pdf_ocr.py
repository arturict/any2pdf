#!/usr/bin/env python3
"""
Convert PPTX files to PDF with OCR processing.
"""

import os
import sys
from pathlib import Path
import subprocess
import shutil


def check_dependencies():
    """Check if required tools are installed."""
    tools = {
        'libreoffice': ['libreoffice', '--version'],
        'unoconv': ['unoconv', '--version'],
        'tesseract': ['tesseract', '--version'],
        'pdftoppm': ['pdftoppm', '-v']
    }
    
    available = {}
    for tool, cmd in tools.items():
        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=5)
            available[tool] = True
        except:
            available[tool] = False
    
    return available


def pptx_to_pdf_with_ocr(pptx_path, output_pdf_path, has_libreoffice, has_tesseract, has_poppler):
    """
    Convert PPTX to PDF and apply OCR if tools are available.
    """
    print(f"Processing: {pptx_path.name}")
    
    # Step 1: Convert PPTX to PDF using LibreOffice
    temp_pdf = pptx_path.with_suffix('.pdf')
    
    if has_libreoffice:
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(pptx_path.parent),
            str(pptx_path)
        ]
    else:
        print(f"  ⚠ LibreOffice not found. Cannot convert {pptx_path.name}")
        print("  Please install: sudo apt-get install libreoffice")
        return False
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout converting {pptx_path.name}")
        return False
    except Exception as e:
        print(f"  ✗ Error converting {pptx_path.name}: {e}")
        return False
    
    if not temp_pdf.exists():
        print(f"  ✗ Failed to create PDF for {pptx_path.name}")
        return False
    
    # Step 2: Apply OCR to the PDF if tools available
    if has_tesseract and has_poppler:
        try:
            from pdf2image import convert_from_path
            import pytesseract
            import fitz
            
            images = convert_from_path(str(temp_pdf), dpi=300)
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
                page = pdf_document[-1]
                page.insert_text((10, 10), ocr_text, fontsize=0.1, color=(1, 1, 1))
            
            pdf_document.save(str(output_pdf_path))
            pdf_document.close()
            temp_pdf.unlink()
            
            print(f"  ✓ Created with OCR: {output_pdf_path.name}")
            return True
            
        except Exception as e:
            print(f"  ⚠ OCR failed, using PDF without OCR: {e}")
            if temp_pdf.exists():
                temp_pdf.rename(output_pdf_path)
                print(f"  ✓ Created (without OCR): {output_pdf_path.name}")
            return True
    else:
        # No OCR tools, just use the converted PDF
        temp_pdf.rename(output_pdf_path)
        print(f"  ✓ Created (without OCR): {output_pdf_path.name}")
        if not has_tesseract:
            print(f"    (Install tesseract-ocr for OCR support)")
        return True


def process_folder(folder_path):
    """
    Process all PPTX files in the folder.
    """
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        print(f"Error: {folder} is not a valid directory!")
        return
    
    pptx_files = list(folder.glob("*.pptx"))
    
    if not pptx_files:
        print("No PPTX files found in the folder.")
        return
    
    print("Checking dependencies...")
    deps = check_dependencies()
    print(f"  LibreOffice: {'✓' if deps['libreoffice'] else '✗'}")
    print(f"  Tesseract OCR: {'✓' if deps['tesseract'] else '✗'}")
    print(f"  Poppler (pdftoppm): {'✓' if deps['pdftoppm'] else '✗'}")
    print()
    
    if not deps['libreoffice']:
        print("ERROR: LibreOffice is required for PPTX conversion.")
        print("Please install: sudo apt-get install libreoffice")
        return
    
    print(f"Found {len(pptx_files)} PPTX files to convert")
    print("-" * 50)
    
    converted = 0
    failed = 0
    
    for pptx_file in pptx_files:
        output_pdf = pptx_file.with_suffix('.pdf')
        
        if pptx_to_pdf_with_ocr(pptx_file, output_pdf, 
                                deps['libreoffice'], 
                                deps['tesseract'], 
                                deps['pdftoppm']):
            # Remove original PPTX file
            pptx_file.unlink()
            converted += 1
        else:
            failed += 1
    
    print("-" * 50)
    print(f"Conversion complete!")
    print(f"Converted: {converted} files")
    if failed > 0:
        print(f"Failed: {failed} files")


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_pptx_to_pdf_ocr.py <folder_path>")
        print("\nExample:")
        print("  python convert_pptx_to_pdf_ocr.py flattened_files")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    process_folder(folder_path)


if __name__ == "__main__":
    main()

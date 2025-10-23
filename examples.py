#!/usr/bin/env python3
"""
Example script showing advanced usage of the document converter.
"""

from pathlib import Path
from document_to_pdf import DocumentConverter


def example_basic():
    """Basic usage example."""
    print("Example 1: Basic Conversion")
    print("-" * 40)
    
    converter = DocumentConverter(
        source_folder="./my_documents",
        output_folder="./pdfs",
        use_ocr=True
    )
    converter.convert_all()
    print()


def example_with_merge():
    """Convert and merge all PDFs into one."""
    print("Example 2: Convert and Merge into Single PDF")
    print("-" * 40)
    
    converter = DocumentConverter(
        source_folder="./my_documents",
        output_folder="./pdfs",
        use_ocr=True,
        merge_output=True
    )
    converter.convert_all()
    print()


def example_without_ocr():
    """Convert without OCR for faster processing."""
    print("Example 3: Fast Conversion (No OCR)")
    print("-" * 40)
    
    converter = DocumentConverter(
        source_folder="./my_documents",
        use_ocr=False,
        merge_output=True
    )
    converter.convert_all()
    print()


def example_custom_workflow():
    """Custom workflow with manual file selection."""
    print("Example 4: Custom Workflow")
    print("-" * 40)
    
    # Initialize converter
    converter = DocumentConverter(
        source_folder="./my_documents",
        output_folder="./selected_pdfs"
    )
    
    # Collect files
    files = converter.collect_files()
    
    # Filter only PPTX files
    pptx_files = [f for f in files if f.suffix.lower() == '.pptx']
    
    print(f"Found {len(pptx_files)} PPTX files")
    
    # Convert each manually
    for file_path in pptx_files:
        converter.convert_file(file_path)
    
    print(f"\nConverted {converter.stats['converted']} files")
    print()


def example_check_before_convert():
    """Check dependencies before converting."""
    print("Example 5: Check Dependencies First")
    print("-" * 40)
    
    converter = DocumentConverter(source_folder="./my_documents")
    
    # Print dependency status
    converter.print_dependencies()
    
    # Check if LibreOffice is available
    if not converter.deps['libreoffice']:
        print("ERROR: LibreOffice is required!")
        print("Install with: sudo apt-get install libreoffice")
        return
    
    # Check if OCR is available
    if not converter.deps['tesseract']:
        print("WARNING: OCR not available, PDFs won't be searchable")
        print("Install with: sudo apt-get install tesseract-ocr")
    
    # Proceed with conversion
    print("\nStarting conversion...")
    converter.convert_all()
    print()


def example_programmatic_usage():
    """Use the converter programmatically in your own code."""
    print("Example 6: Programmatic Usage")
    print("-" * 40)
    
    # Create converter
    converter = DocumentConverter(
        source_folder="./lectures",
        output_folder="./pdf_lectures",
        merge_output=True
    )
    
    # Get list of files
    files = converter.collect_files()
    
    # Process files
    success_count = 0
    for file_path in files:
        if converter.convert_file(file_path):
            success_count += 1
    
    # Merge if requested
    if converter.merge_output and converter.converted_pdfs:
        merged_path = converter.output_folder / "merged_all_documents.pdf"
        if converter.merge_pdfs(converter.converted_pdfs, merged_path):
            print(f"\nMerged all PDFs into: {merged_path}")
    
    # Print results
    print(f"\nSuccessfully converted {success_count}/{len(files)} files")
    
    # Access statistics
    print(f"Stats: {converter.stats}")
    print()


def example_text_files():
    """Convert text files to PDF."""
    print("Example 7: Text Files to PDF")
    print("-" * 40)
    
    converter = DocumentConverter(
        source_folder="./text_documents",
        merge_output=True
    )
    
    # This will convert TXT, MD, CSV, JSON, XML, HTML, etc.
    converter.convert_all()
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Document to PDF Converter - Advanced Examples")
    print("=" * 60)
    print()
    
    print("This script demonstrates various usage patterns.")
    print("Uncomment the example you want to run.\n")
    
    # Uncomment one of these to run:
    # example_basic()
    # example_with_merge()
    # example_without_ocr()
    # example_custom_workflow()
    # example_check_before_convert()
    # example_programmatic_usage()
    # example_text_files()
    
    print("To run an example, edit this file and uncomment one of the function calls.")

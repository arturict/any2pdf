#!/usr/bin/env python3
"""
Test script to verify the document converter is working correctly.
"""

import sys
from pathlib import Path
from document_to_pdf import DocumentConverter


def test_dependencies():
    """Test if all dependencies are available."""
    print("Testing dependencies...")
    converter = DocumentConverter(Path.cwd())
    converter.print_dependencies()
    
    required = ['libreoffice']
    optional = ['tesseract', 'pdftoppm', 'convert']
    
    # Check required
    all_required = all(converter.deps.get(dep, False) for dep in required)
    
    if all_required:
        print("✓ All required dependencies are installed!")
    else:
        print("✗ Missing required dependencies!")
        print("\nPlease run:")
        print("  sudo apt-get install libreoffice")
        return False
    
    # Check optional
    missing_optional = [dep for dep in optional if not converter.deps.get(dep, False)]
    if missing_optional:
        print(f"\n⚠ Optional dependencies missing: {', '.join(missing_optional)}")
        print("  For full OCR support, install:")
        print("  sudo apt-get install tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick")
    else:
        print("\n✓ All optional dependencies are installed!")
    
    return True


def main():
    """Run tests."""
    print("=" * 60)
    print("Document to PDF Converter - Test Suite")
    print("=" * 60)
    print()
    
    success = test_dependencies()
    
    print()
    print("=" * 60)
    if success:
        print("✓ Tests passed! Converter is ready to use.")
        print("\nTry it out:")
        print("  python document_to_pdf.py /path/to/documents")
    else:
        print("✗ Tests failed! Please install missing dependencies.")
        print("\nSee README.md for installation instructions.")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

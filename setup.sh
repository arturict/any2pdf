#!/bin/bash
# Quick setup script for Ubuntu/Debian systems

echo "=== Document to PDF Converter - Setup Script ==="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "Please do not run as root/sudo. The script will ask for sudo when needed."
   exit 1
fi

# Install system dependencies
echo "Step 1: Installing system dependencies..."
echo "This requires sudo privileges."
sudo apt-get update
sudo apt-get install -y \
    libreoffice \
    tesseract-ocr \
    tesseract-ocr-deu \
    poppler-utils \
    imagemagick \
    python3-venv \
    python3-pip

# Create virtual environment
echo ""
echo "Step 2: Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment and install packages
echo ""
echo "Step 3: Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To use the converter:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the converter:"
echo "     python document_to_pdf.py /path/to/documents"
echo ""
echo "For more information, see README.md"

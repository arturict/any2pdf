#!/bin/bash
# One-click installation script for any2pdf

set -e

echo "========================================="
echo "  any2pdf - Installation Script"
echo "========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📦 Detected: Linux"
    echo "Installing system dependencies..."
    sudo apt-get update -qq
    sudo apt-get install -y libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick python3-venv python3-pip
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 Detected: macOS"
    echo "Installing system dependencies via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install it from https://brew.sh"
        exit 1
    fi
    brew install libreoffice tesseract tesseract-lang poppler imagemagick python3
    
else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "Please use WSL on Windows or install dependencies manually."
    exit 1
fi

echo ""
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo ""
echo "📚 Installing Python packages..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "========================================="
echo "  ✅ Installation Complete!"
echo "========================================="
echo ""
echo "To use any2pdf, run:"
echo "  source venv/bin/activate"
echo "  python convert.py"
echo ""
echo "Or in one step:"
echo "  ./convert.sh wirtschaft"
echo ""

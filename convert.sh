#!/bin/bash
# Simple wrapper script for document_to_pdf.py

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Run the converter
python document_to_pdf.py "$@"

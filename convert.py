#!/usr/bin/env python3
"""
Simple wrapper script for easy usage - just run: python convert.py
"""
import subprocess
import sys

if __name__ == "__main__":
    # If no arguments, run in interactive mode
    if len(sys.argv) == 1:
        subprocess.run([sys.executable, "document_to_pdf.py"])
    else:
        # Pass all arguments to document_to_pdf.py
        subprocess.run([sys.executable, "document_to_pdf.py"] + sys.argv[1:])

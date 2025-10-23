#!/bin/bash

# Test Examples for any2pdf
# Demonstrates various use cases

set -e

BLUE='\033[94m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
BOLD='\033[1m'
ENDC='\033[0m'

echo -e "${BOLD}${BLUE}╔═══════════════════════════════════════════════════╗${ENDC}"
echo -e "${BOLD}${BLUE}║       any2pdf - Test Examples & Demos            ║${ENDC}"
echo -e "${BOLD}${BLUE}╚═══════════════════════════════════════════════════╝${ENDC}"
echo ""

# Create test directory
TEST_DIR="./test_examples"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

echo -e "${BOLD}${GREEN}Creating test files...${ENDC}"

# 1. Create text file
cat > "$TEST_DIR/document.txt" << 'TEXTEOF'
Test Document
=============

This is a test document for any2pdf.

Features:
- Multiple format support
- OCR capabilities
- AI chat integration
- GPT-5 reasoning control

Perfect for converting documents to searchable PDFs!
TEXTEOF

# 2. Create markdown file
cat > "$TEST_DIR/readme.md" << 'MDEOF'
# Project Documentation

## Overview
This is a sample markdown file for testing any2pdf.

## Features
- **Format Support**: Office, Images, Text, PDF
- **AI Chat**: OpenAI GPT-5 & Google Gemini
- **Performance**: Multi-threading, Smart caching

## Usage
```bash
python document_to_pdf.py ./docs --merge
```

## Benefits
✅ Fast conversion
✅ AI-powered chat
✅ Multiple formats
MDEOF

# 3. Create JSON file
cat > "$TEST_DIR/data.json" << 'JSONEOF'
{
  "project": "any2pdf",
  "version": "1.2.0",
  "features": [
    "Document conversion",
    "AI chat integration",
    "GPT-5 support",
    "Gemini 2.5 support",
    "Reasoning control"
  ],
  "providers": {
    "openai": ["gpt-5", "gpt-5-mini", "gpt-4.1"],
    "gemini": ["gemini-2.5-flash", "gemini-2.5-pro"]
  }
}
JSONEOF

# 4. Create CSV file
cat > "$TEST_DIR/data.csv" << 'CSVEOF'
Feature,Status,Provider
Document Conversion,Active,N/A
AI Chat,Active,OpenAI
AI Chat,Active,Gemini
GPT-5 Support,Active,OpenAI
Reasoning Control,Active,OpenAI
Multi-threading,Active,N/A
Smart Caching,Active,N/A
CSVEOF

# 5. Create HTML file
cat > "$TEST_DIR/page.html" << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <title>any2pdf Test Page</title>
</head>
<body>
    <h1>any2pdf - Universal Document Converter</h1>
    <h2>Features</h2>
    <ul>
        <li>Convert Office documents (PPTX, DOCX, XLSX)</li>
        <li>Convert images (JPG, PNG, GIF, SVG)</li>
        <li>Convert text files (TXT, MD, JSON, CSV)</li>
        <li>AI Chat with GPT-5 & Gemini 2.5</li>
        <li>Reasoning effort control</li>
    </ul>
    <h2>Performance</h2>
    <p>Multi-threading support for 50-70% faster conversion!</p>
</body>
</html>
HTMLEOF

echo -e "${GREEN}✓ Created 5 test files in $TEST_DIR${ENDC}"
echo ""

# Run tests
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
echo -e "${BOLD}Test 1: Basic Conversion (No Merge)${ENDC}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
python3 document_to_pdf.py "$TEST_DIR" -o "$TEST_DIR/output_basic" --no-ocr
echo -e "${GREEN}✓ Test 1 completed${ENDC}"
echo ""

echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
echo -e "${BOLD}Test 2: Conversion with Merge${ENDC}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
python3 document_to_pdf.py "$TEST_DIR" -o "$TEST_DIR/output_merged" --merge --no-ocr
echo -e "${GREEN}✓ Test 2 completed${ENDC}"
echo ""

echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
echo -e "${BOLD}Test 3: Conversion with OCR${ENDC}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
python3 document_to_pdf.py "$TEST_DIR" -o "$TEST_DIR/output_ocr" --merge
echo -e "${GREEN}✓ Test 3 completed${ENDC}"
echo ""

# Display results
echo -e "${BOLD}${GREEN}╔═══════════════════════════════════════════════════╗${ENDC}"
echo -e "${BOLD}${GREEN}║              Test Results Summary                 ║${ENDC}"
echo -e "${BOLD}${GREEN}╚═══════════════════════════════════════════════════╝${ENDC}"
echo ""

echo -e "${BOLD}Test 1 - Basic Conversion:${ENDC}"
ls -lh "$TEST_DIR/output_basic"/*.pdf 2>/dev/null | awk '{print "  " $9 " - " $5}' || echo "  No files"
echo ""

echo -e "${BOLD}Test 2 - With Merge:${ENDC}"
ls -lh "$TEST_DIR/output_merged"/*.pdf 2>/dev/null | awk '{print "  " $9 " - " $5}' || echo "  No files"
if [ -f "$TEST_DIR/output_merged/merged_all_documents.pdf" ]; then
    echo -e "  ${GREEN}✓ Merged PDF created!${ENDC}"
fi
echo ""

echo -e "${BOLD}Test 3 - With OCR:${ENDC}"
ls -lh "$TEST_DIR/output_ocr"/*.pdf 2>/dev/null | awk '{print "  " $9 " - " $5}' || echo "  No files"
if [ -f "$TEST_DIR/output_ocr/merged_all_documents.pdf" ]; then
    echo -e "  ${GREEN}✓ OCR-processed merged PDF created!${ENDC}"
fi
echo ""

echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
echo -e "${BOLD}Next Steps:${ENDC}"
echo -e "  1. Test AI Chat: ${YELLOW}python3 document_to_pdf.py $TEST_DIR --merge${ENDC}"
echo -e "     ${DIM}(Answer 'y' when prompted for chat)${ENDC}"
echo -e ""
echo -e "  2. With OpenAI GPT-5:"
echo -e "     - Select provider: ${CYAN}1${ENDC} (OpenAI)"
echo -e "     - Enter API key"
echo -e "     - Choose model: ${CYAN}gpt-5${ENDC}"
echo -e "     - Select reasoning: ${CYAN}medium${ENDC}"
echo -e ""
echo -e "  3. With Google Gemini:"
echo -e "     - Select provider: ${CYAN}2${ENDC} (Gemini)"
echo -e "     - Enter API key"
echo -e "     - Choose model: ${CYAN}gemini-2.5-flash${ENDC}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════${ENDC}"
echo ""

echo -e "${BOLD}${GREEN}✅ All tests completed successfully!${ENDC}"
echo -e "${DIM}Test files created in: $TEST_DIR${ENDC}"
echo -e "${DIM}Output directories:${ENDC}"
echo -e "${DIM}  - $TEST_DIR/output_basic${ENDC}"
echo -e "${DIM}  - $TEST_DIR/output_merged${ENDC}"
echo -e "${DIM}  - $TEST_DIR/output_ocr${ENDC}"

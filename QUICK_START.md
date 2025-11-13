# 🚀 Quick Start Guide

## Fastest Way to Get Started (2 Steps!)

### 1. Install
```bash
./install.sh
```

### 2. Convert
```bash
source venv/bin/activate
python convert.py
```

That's it! Follow the interactive prompts.

---

## Alternative: Command Line

```bash
# Activate environment (after install.sh)
source venv/bin/activate

# Convert a folder
./convert.sh wirtschaft

# Convert with merged PDF
./convert.sh docs --merge

# Convert with 4 parallel workers (faster!)
./convert.sh docs --merge -j 4
```

---

## Examples

```bash
# Interactive mode - easiest for beginners
python convert.py

# Quick conversion of current folder
./convert.sh .

# Convert specific folder with all options
./convert.sh ~/Documents/presentations --merge -j 4

# Convert without OCR (faster but not searchable)
./convert.sh ~/Pictures --no-ocr
```

---

## Common Use Cases

### For Students/Teachers
```bash
# Convert lecture slides to searchable PDF
./convert.sh lecture_slides --merge

# Then chat with AI about the content
# (select 'y' when prompted after conversion)
```

### For Business
```bash
# Convert all documents for archival
./convert.sh quarterly_reports --merge -j 8

# Upload merged PDF to ChatGPT/Claude for analysis
```

### For Developers
```bash
# Convert documentation to PDF
./convert.sh docs/ -o ./pdfs/ -j 4
```

---

## Need Help?

- See full [README.md](README.md) for detailed documentation
- Check [docs/USAGE.md](docs/USAGE.md) for advanced features
- File issues on GitHub: [github.com/arturict/any2pdf](https://github.com/arturict/any2pdf)

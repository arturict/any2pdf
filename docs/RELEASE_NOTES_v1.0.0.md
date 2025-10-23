# 🎉 any2pdf v1.0.0 - First Stable Release

> **Convert ANY file format to searchable PDFs - Perfect for ChatGPT & AI Tools!**

We're excited to announce the first stable release of **any2pdf**! 🚀

## 🌟 Highlights

This release brings a comprehensive solution for converting any document format to searchable PDFs, with special optimization for AI tools like ChatGPT and Claude.

### ✨ Key Features

- **30+ File Formats Supported**
  - Office: PPTX, DOCX, XLSX, PPT, DOC, XLS, ODT, ODP, ODS, RTF
  - Images: JPG, PNG, GIF, BMP, TIFF, WEBP, SVG, HEIC
  - Text: TXT, MD, CSV, TSV, LOG, JSON, XML, HTML, HTM
  - PDF: Existing PDFs (copy & OCR)

- **🔗 PDF Merge Functionality**
  - Combine all documents into ONE searchable PDF
  - Perfect for uploading to ChatGPT
  - Maintains readability and structure

- **🔍 OCR Text Recognition**
  - German and English language support
  - Makes scanned documents searchable
  - Intelligent text extraction

- **📁 Recursive Processing**
  - Automatically processes all subfolders
  - Smart duplicate handling
  - Sorted output for better organization

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/arturict/any2pdf.git
cd any2pdf

# 2. Run setup
./setup.sh

# 3. Convert and merge everything
source venv/bin/activate
python document_to_pdf.py /path/to/documents --merge

# 4. Upload merged_all_documents.pdf to ChatGPT!
```

## 📦 What's Included

- **Core Converter**: `document_to_pdf.py` (561 lines, battle-tested)
- **Helper Scripts**: `convert.sh`, `flatten_files.py`, `setup.sh`
- **Comprehensive Docs**: README, Quick Start, Usage Guide, Examples
- **Test Suite**: Sample files and test scripts
- **GitHub Integration**: Issue templates, PR template, contributing guide

## 💡 Use Cases

Perfect for:
- 🎓 Students preparing lecture materials for AI analysis
- 👨‍🏫 Teachers bundling teaching materials
- 🔬 Researchers preparing documents for analysis
- 💼 Professionals merging project documentation
- 🤖 Anyone preparing docs for ChatGPT/Claude

## 📚 Documentation

- [README](README.md) - Complete documentation
- [Quick Start](QUICKSTART.md) - Get started in 2 minutes
- [Usage Guide](USAGE.md) - Detailed instructions
- [Features](FEATURES.md) - Feature overview
- [Contributing](CONTRIBUTING.md) - How to contribute

## 🛠️ Installation

### Ubuntu/Debian
```bash
sudo apt-get update && sudo apt-get install -y \
    libreoffice tesseract-ocr tesseract-ocr-deu \
    poppler-utils imagemagick

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS
```bash
brew install libreoffice tesseract tesseract-lang poppler imagemagick

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🎯 Usage Examples

### For ChatGPT (Recommended)
```bash
./convert.sh ./documents --merge
# → Upload converted_pdfs/merged_all_documents.pdf
```

### Individual PDFs
```bash
python document_to_pdf.py ./documents
```

### Fast Mode (No OCR)
```bash
python document_to_pdf.py ./documents --no-ocr --merge
```

## 📊 Performance

| Files | Without OCR | With OCR |
|-------|-------------|----------|
| 10 files | ~30 seconds | ~2 minutes |
| 50 files | ~2 minutes | ~8 minutes |
| 100 files | ~5 minutes | ~15 minutes |

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - Free for personal and commercial use

## 🙏 Acknowledgments

Built with amazing open-source tools:
- LibreOffice - Office document conversion
- Tesseract OCR - Text recognition
- PyMuPDF - PDF creation & merging
- Pillow - Image processing

## 💬 Feedback & Support

- 🐛 [Report Issues](https://github.com/arturict/any2pdf/issues)
- 💡 [Request Features](https://github.com/arturict/any2pdf/issues)
- 💬 [Discussions](https://github.com/arturict/any2pdf/discussions)

## ⭐ Show Your Support

If you find this project useful, please give it a ⭐ on GitHub!

---

**Made with ❤️ for the AI community**

Thank you for using any2pdf! 🎉

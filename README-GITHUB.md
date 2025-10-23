# any2pdf 📄→📑

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/github/v/release/arturict/any2pdf)](https://github.com/arturict/any2pdf/releases)

> **Convert ANY file format to searchable PDFs - Perfect for ChatGPT & AI Tools!**

Convert 30+ file formats from folders (including subfolders) into searchable PDFs with OCR. Optionally merge everything into one single PDF - ideal for uploading to ChatGPT, Claude, or other AI tools!

![any2pdf Demo](https://via.placeholder.com/800x400/1e293b/ffffff?text=any2pdf+Demo)

## ✨ Features

- 📄 **30+ File Formats**: Office docs, images, text files, and existing PDFs
- 🔗 **PDF Merge**: Combine all documents into one searchable PDF
- 🔍 **OCR**: Extract text from images and scans (German & English)
- 📁 **Recursive**: Processes all subfolders automatically
- 🚀 **Simple**: One command does it all
- 🤖 **AI-Ready**: Optimized for ChatGPT, Claude & similar tools

## 🎯 Quick Start

```bash
# 1. Clone & setup
git clone https://github.com/arturict/any2pdf.git
cd any2pdf
./setup.sh

# 2. Convert & merge everything into ONE PDF
source venv/bin/activate
python document_to_pdf.py /path/to/documents --merge

# 3. Upload merged_all_documents.pdf to ChatGPT! 🎉
```

## 📚 Supported Formats

<table>
<tr>
<td>

**Office Documents (10)**
- PPTX, PPT
- DOCX, DOC
- XLSX, XLS
- ODT, ODP, ODS
- RTF

</td>
<td>

**Images (9)**
- JPG, JPEG, PNG
- GIF, BMP
- TIFF, TIF
- WEBP, SVG, HEIC

</td>
</tr>
<tr>
<td>

**Text Files (9)**
- TXT, MD
- CSV, TSV
- LOG
- JSON, XML
- HTML, HTM

</td>
<td>

**PDF**
- Existing PDFs
- Copy & OCR
- Merge capabilities

</td>
</tr>
</table>

## 💡 Usage Examples

### 🤖 For ChatGPT/Claude (Recommended)
```bash
# Merge all lecture materials into ONE PDF
./convert.sh ./lectures --merge
# → Upload converted_pdfs/merged_all_documents.pdf to ChatGPT
```

### 📄 Individual PDFs
```bash
# Convert to separate PDFs (no merge)
python document_to_pdf.py ./documents
```

### ⚡ Fast Mode (No OCR)
```bash
# Quick conversion without text recognition
python document_to_pdf.py ./files --no-ocr --merge
```

### 🎯 Custom Output
```bash
# Specify custom output folder
python document_to_pdf.py ./docs -o ./output --merge
```

## ��️ Installation

### Ubuntu/Debian
```bash
# System dependencies
sudo apt-get update && sudo apt-get install -y \
    libreoffice \
    tesseract-ocr tesseract-ocr-deu \
    poppler-utils \
    imagemagick

# Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS
```bash
# System dependencies
brew install libreoffice tesseract tesseract-lang poppler imagemagick

# Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
> ⚠️ **Windows users**: Please use [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/windows/wsl/install) and follow the Ubuntu/Debian instructions.
> 
> **Detailed WSL Guide**: See [WSL_SETUP.md](WSL_SETUP.md) for step-by-step instructions.
> 
> ```powershell
> # In PowerShell (as Administrator):
> wsl --install
> ```
> 
> After WSL installation, open Ubuntu terminal and follow Ubuntu/Debian instructions above.

### Automated Setup
```bash
# Use the setup script (Ubuntu/Debian/WSL only)
./setup.sh
```

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 2 minutes
- **[Usage Guide](USAGE.md)** - Detailed usage instructions
- **[Features](FEATURES.md)** - Feature overview & comparison
- **[Changelog](CHANGELOG.md)** - Version history

## 🎓 Use Cases

| User | Use Case |
|------|----------|
| 🎓 **Students** | Prepare lecture materials for AI analysis |
| 👨‍🏫 **Teachers** | Bundle teaching materials |
| 🔬 **Researchers** | Prepare documents for analysis |
| 💼 **Professionals** | Merge project documentation |
| 🤖 **AI Enthusiasts** | Prepare any docs for ChatGPT/Claude |

## 🚀 Command Line Options

```bash
python document_to_pdf.py [FOLDER] [OPTIONS]

Options:
  -o, --output OUTPUT   Custom output folder
  --no-ocr             Disable OCR (faster but not searchable)
  -m, --merge          Merge all PDFs into one file
  -h, --help           Show help message

Examples:
  python document_to_pdf.py ./docs
  python document_to_pdf.py ./docs --merge
  python document_to_pdf.py ./docs -o ./output --merge
  python document_to_pdf.py ./docs --no-ocr --merge
```

## 📊 Performance

| Files | Without OCR | With OCR |
|-------|-------------|----------|
| 10 files | ~30 seconds | ~2 minutes |
| 50 files | ~2 minutes | ~8 minutes |
| 100 files | ~5 minutes | ~15 minutes |

*Performance depends on file size and system specifications*

## 🔧 Dependencies

### System Requirements
- Python 3.7+
- LibreOffice (Office document conversion)
- Tesseract OCR (Text recognition, optional)
- Poppler (PDF processing, optional)
- ImageMagick (Image conversion, optional)

### Python Packages
- Pillow - Image processing
- pytesseract - OCR wrapper
- PyMuPDF (fitz) - PDF creation & merging
- pdf2image - PDF to image conversion

## 💡 Pro Tips

1. **For ChatGPT**: Always use `--merge` to get ONE document
2. **Large batches**: Conversion may take several minutes for 100+ files
3. **OCR Quality**: High-resolution scans (300 DPI) give best results
4. **Performance**: `--no-ocr` is 3-5x faster but PDFs won't be searchable
5. **Languages**: Install additional Tesseract languages with `apt-get install tesseract-ocr-[lang]`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with amazing open-source tools:
- [LibreOffice](https://www.libreoffice.org/) - Office document conversion
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Text recognition
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF creation & merging
- [Pillow](https://python-pillow.org/) - Image processing

## 🆘 Support

- 📖 [Documentation](https://github.com/arturict/any2pdf/blob/main/README.md)
- 🐛 [Issue Tracker](https://github.com/arturict/any2pdf/issues)
- 💬 [Discussions](https://github.com/arturict/any2pdf/discussions)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ for the AI community**

[🌟 Star this repo](https://github.com/arturict/any2pdf) | [🐛 Report Bug](https://github.com/arturict/any2pdf/issues) | [✨ Request Feature](https://github.com/arturict/any2pdf/issues)

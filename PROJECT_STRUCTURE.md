# any2pdf - Project Structure

```
any2pdf/
│
├── 📚 Documentation
│   ├── README.md              # Main documentation (GitHub version)
│   ├── README-GITHUB.md       # Enhanced GitHub README with badges
│   ├── QUICKSTART.md          # 2-minute quick start guide
│   ├── USAGE.md               # Detailed usage instructions
│   ├── FEATURES.md            # Feature overview & comparison
│   ├── SUMMARY.md             # Compact project summary
│   ├── CHANGELOG.md           # Version history
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   └── PROJECT_INFO.md        # Original project information
│
├── 🔧 Core Scripts
│   ├── document_to_pdf.py     # Main converter (561 lines)
│   │   ├── DocumentConverter class
│   │   ├── Office document conversion
│   │   ├── Image conversion with OCR
│   │   ├── Text file conversion
│   │   ├── PDF processing & merge
│   │   └── CLI interface
│   │
│   ├── convert.sh             # Simple wrapper script
│   └── flatten_files.py       # Utility: collect files from subfolders
│
├── 🧪 Testing & Examples
│   ├── test_converter.py      # Dependency & functionality tests
│   ├── examples.py            # Code examples for developers
│   └── test_files/            # Sample test files
│       ├── test.txt
│       ├── test.md
│       └── test.csv
│
├── ⚙️ Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── setup.sh              # Automated setup script (Ubuntu/Debian)
│   ├── .gitignore            # Git ignore rules
│   └── LICENSE               # MIT License
│
├── 🐙 GitHub Configuration
│   └── .github/
│       ├── ISSUE_TEMPLATE/
│       │   ├── bug_report.md
│       │   └── feature_request.md
│       └── PULL_REQUEST_TEMPLATE.md
│
└── 📦 Output (ignored by git)
    ├── converted_pdfs/        # Individual converted PDFs
    │   └── merged_all_documents.pdf  # Merged output
    └── venv/                  # Python virtual environment
```

## 📊 File Statistics

| Category | Files | Lines of Code |
|----------|-------|---------------|
| Core Python | 3 | ~650 |
| Documentation | 9 | ~2000 |
| Configuration | 4 | ~50 |
| Tests | 2 | ~250 |
| **Total** | **18** | **~2950** |

## 🔄 Data Flow

```
Input Files (any format)
    ↓
[document_to_pdf.py]
    ├→ Office → LibreOffice → PDF
    ├→ Images → ImageMagick/OCR → PDF
    ├→ Text → PyMuPDF → PDF
    └→ PDF → Copy + OCR → PDF
    ↓
Individual PDFs
    ↓
[Optional: --merge]
    ↓
merged_all_documents.pdf
```

## 🎯 Key Components

### DocumentConverter Class
```python
class DocumentConverter:
    ├── __init__()              # Initialize converter
    ├── _check_dependencies()   # Check system tools
    ├── collect_files()         # Find convertible files
    ├── convert_office_to_pdf() # Office docs conversion
    ├── convert_image_to_pdf()  # Image conversion
    ├── convert_text_to_pdf()   # Text files conversion
    ├── copy_pdf()              # PDF processing
    ├── apply_ocr_to_pdf()      # OCR application
    ├── merge_pdfs()            # PDF merging
    └── convert_all()           # Main workflow
```

## 🚀 Workflow

1. **Initialization**: Check dependencies, create output folder
2. **Discovery**: Recursively find all convertible files
3. **Conversion**: Convert each file to PDF
4. **OCR**: Apply text recognition (optional)
5. **Merge**: Combine all PDFs (optional)
6. **Summary**: Report statistics

## 📝 Documentation Hierarchy

```
Entry Points:
├── README.md (Overview & Quick Start)
├── QUICKSTART.md (2-minute guide)
└── USAGE.md (Detailed guide)

Reference:
├── FEATURES.md (Feature list)
├── CHANGELOG.md (Version history)
└── SUMMARY.md (Project overview)

Development:
├── CONTRIBUTING.md (Contribution guide)
├── examples.py (Code examples)
└── PROJECT_STRUCTURE.md (This file)
```

## 🔧 Dependencies Map

```
System Level:
├── LibreOffice → Office documents
├── Tesseract → OCR
├── Poppler → PDF processing
└── ImageMagick → Image conversion

Python Level:
├── Pillow → Image processing
├── pytesseract → OCR wrapper
├── PyMuPDF → PDF creation/merge
└── pdf2image → PDF to image
```

## 📦 Release Artifacts

```
Release v1.0.0
├── Source Code (tar.gz, zip)
├── Documentation Bundle
└── Pre-configured Scripts
```

---

**any2pdf** - Project Structure v1.0

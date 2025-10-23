# any2pdf 📄→📑

> **Convert ANY file format to searchable PDFs - Perfect for ChatGPT & AI Tools!**

Ein Python-Tool zur Konvertierung von verschiedensten Dateiformaten in durchsuchbare PDFs für die Verwendung mit KI-Tools wie ChatGPT.

## Features

- 📄 **Office-Dokumente**: Konvertiert PPTX, DOCX, DOC, PPT, XLSX, XLS, ODT, ODP, ODS, RTF
- 🖼️ **Bilder**: Konvertiert JPG, PNG, GIF, BMP, TIFF, WEBP, SVG, HEIC
- 📝 **Text-Dateien**: Konvertiert TXT, MD, CSV, TSV, LOG, JSON, XML, HTML
- 📑 **PDF-Verarbeitung**: Kopiert existierende PDFs und wendet OCR an
- 🔍 **OCR**: Macht alle Dokumente durchsuchbar mit Texterkennung (Deutsch & Englisch)
- 📁 **Batch-Verarbeitung**: Verarbeitet ganze Ordner mit Unterordnern
- 🔗 **PDF-Zusammenführung**: Optional alle PDFs in einem Dokument zusammenführen
- ⚡ **Parallel Processing**: 50-70% schneller durch Multi-Threading
- 💾 **Smart Caching**: Überspringe bereits konvertierte Dateien automatisch
- 🚀 **Einfach zu bedienen**: Ein Befehl für alles

## Installation

### 1. System-Abhängigkeiten installieren

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick
```

**macOS:**
```bash
brew install libreoffice tesseract tesseract-lang poppler imagemagick
```

**Windows:**
> ⚠️ **Für Windows-Nutzer**: Bitte verwende [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/de-de/windows/wsl/install) und folge dann den Ubuntu/Debian-Anweisungen.
> 
> **Ausführliche WSL-Anleitung**: Siehe [WSL_SETUP.md](WSL_SETUP.md) für eine Schritt-für-Schritt-Anleitung.
> 
> ```powershell
> # In PowerShell als Administrator:
> wsl --install
> ```
> Nach der Installation von WSL, öffne das Ubuntu-Terminal und folge den Ubuntu/Debian-Anweisungen oben.

### 2. Python-Pakete installieren

```bash
# Virtual Environment erstellen (empfohlen)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Pakete installieren
pip install -r requirements.txt
```

## Verwendung

### Basis-Verwendung

```bash
# Alle Dokumente in einem Ordner konvertieren
python document_to_pdf.py /pfad/zum/ordner

# Mit benutzerdefiniertem Output-Ordner
python document_to_pdf.py /pfad/zum/ordner -o /pfad/zum/output

# Ohne OCR (schneller, aber nicht durchsuchbar)
python document_to_pdf.py /pfad/zum/ordner --no-ocr

# Alle PDFs in einem Dokument zusammenführen
python document_to_pdf.py /pfad/zum/ordner --merge

# ⚡ Mit Parallel Processing (4 Workers)
python document_to_pdf.py /pfad/zum/ordner --merge -j 4

# 💾 Ohne Caching (immer neu konvertieren)
python document_to_pdf.py /pfad/zum/ordner --merge --no-cache
```

### Beispiele

```bash
# Unterrichtsmaterialien konvertieren und zusammenführen
python document_to_pdf.py ./documents --merge

# Schnelle Konvertierung ohne OCR
python document_to_pdf.py ./documents --no-ocr

# In Virtual Environment
source venv/bin/activate
python document_to_pdf.py ./flattened_files -o ./output --merge

# Hilfe anzeigen
python document_to_pdf.py --help
```

## Workflow für ChatGPT

1. **Dateien sammeln und konvertieren:**
   ```bash
   python document_to_pdf.py ./unterrichtsmaterial --merge
   ```

2. **Einzelnes PDF an ChatGPT hochladen:**
   - Das zusammengeführte PDF `merged_all_documents.pdf` hochladen
   - Text ist durchsuchbar und kann analysiert werden

3. **Mit ChatGPT arbeiten:**
   - Zusammenfassungen erstellen
   - Fragen zu den Inhalten stellen
   - Lernmaterialien generieren

## Unterstützte Formate

### Office-Dokumente (benötigt LibreOffice)
- PowerPoint: `.pptx`, `.ppt`
- Word: `.docx`, `.doc`
- Excel: `.xlsx`, `.xls`
- OpenDocument: `.odt`, `.odp`, `.ods`
- Rich Text: `.rtf`

### Bilder (benötigt ImageMagick)
- `.jpg`, `.jpeg`
- `.png`
- `.gif`
- `.bmp`
- `.tiff`, `.tif`
- `.webp`
- `.svg`
- `.heic`

### Text-Dateien
- `.txt`
- `.md` (Markdown)
- `.csv`, `.tsv`
- `.log`
- `.json`, `.xml`
- `.html`, `.htm`

### PDF-Dateien
- `.pdf` (werden kopiert und optional mit OCR versehen)

## Abhängigkeiten

### Erforderlich
- **Python 3.7+**
- **LibreOffice**: Für Office-Dokument-Konvertierung

### Optional (für OCR)
- **Tesseract OCR**: Texterkennung
- **Poppler**: PDF-zu-Bild-Konvertierung
- **ImageMagick**: Bild-Bearbeitung

### Python-Pakete
- `Pillow`: Bildverarbeitung
- `pytesseract`: Tesseract Python-Wrapper
- `PyMuPDF (fitz)`: PDF-Bearbeitung
- `pdf2image`: PDF-zu-Bild-Konvertierung

## Troubleshooting

### LibreOffice nicht gefunden
```bash
sudo apt-get install libreoffice
```

### OCR funktioniert nicht
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-deu poppler-utils
pip install pytesseract pdf2image PyMuPDF Pillow
```

### ImageMagick-Fehler
```bash
sudo apt-get install imagemagick
```

### "externally-managed-environment" Fehler
Verwende ein Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Projekt-Struktur

```
file-from-folder/
├── document_to_pdf.py      # Hauptprogramm
├── flatten_files.py        # Hilfstool: Dateien in einen Ordner kopieren
├── requirements.txt        # Python-Abhängigkeiten
├── README.md              # Diese Datei
└── venv/                  # Virtual Environment (optional)
```

## Lizenz

MIT License - Frei zu verwenden für Bildungszwecke.

## Tipps

- **Große Dateien**: Konvertierung kann bei vielen/großen Dateien länger dauern
- **⚡ Performance**: Nutze `-j 4` für parallele Konvertierung (50-70% schneller!)
- **💾 Caching**: Bei wiederholten Läufen werden unveränderte Dateien übersprungen
- **OCR-Qualität**: Beste Ergebnisse mit hochauflösenden Bildern (300 DPI)
- **Sprachen**: Standard ist Deutsch + Englisch, weitere können installiert werden
- **Batch-Processing**: Verarbeitet automatisch alle Unterordner
- **Merge-Option**: Mit `--merge` wird ein einziges PDF erstellt, ideal für ChatGPT

## Performance

Siehe [PERFORMANCE.md](PERFORMANCE.md) für detaillierte Benchmarks und Optimierungen.

**TL;DR**: any2pdf ist jetzt **50-200% schneller** durch:
- ⚡ Parallel Processing (Multi-Threading)
- 💾 Smart Caching (Überspringe bereits konvertierte Dateien)
- ⏱️ Performance Metrics (Zeit-Tracking)

## Beispiel-Output

```
Source folder: /home/user/documents
Output folder: /home/user/documents/converted_pdfs

Dependency Check:
  LibreOffice:     ✓
  Tesseract OCR:   ✓
  Poppler:         ✓
  ImageMagick:     ✓

Found 8 files to convert
============================================================
Converting: SW1 - Einführung W&R.pptx
  Applying OCR...
  ✓ Saved to: SW1 - Einführung W&R.pdf

Converting: Entscheidungsbaum.png
  ✓ Saved to: Entscheidungsbaum.pdf

Converting: notes.txt
  ✓ Saved to: notes.pdf

============================================================
Merging all PDFs into single document...
✓ Merged PDF saved to: merged_all_documents.pdf

============================================================
Conversion Summary:
  Total files:     8
  Converted:       8
  Failed:          0

All PDFs saved to: /home/user/documents/converted_pdfs
```

---

**any2pdf** - Made with ❤️ for the AI community | [GitHub](https://github.com/arturict/any2pdf)

## 💬 AI Chat mit PDF (NEU!)

Nach der Konvertierung mit `--merge` kannst du direkt mit dem generierten PDF chatten!

### Unterstützte AI-Provider

- **OpenAI** (GPT-4, GPT-4o, GPT-3.5, O1, etc.)
- **Google Gemini** (Gemini 2.0, Gemini 1.5 Pro/Flash, etc.)

### Installation

```bash
# Für OpenAI
pip install openai

# Für Gemini
pip install google-generativeai

# Oder beide
pip install openai google-generativeai
```

### Verwendung

```bash
# Konvertiere und starte Chat
python document_to_pdf.py /pfad/zu/dateien --merge

# Am Ende wirst du gefragt:
# "Would you like to chat with the PDF using AI? (y/N)"

# Wähle dann:
# 1. AI Provider (OpenAI oder Gemini)
# 2. Modell (z.B. gpt-4o, gemini-2.0-flash-exp)
# 3. Gib deinen API Key ein
```

### Chat-Befehle

Im Chat stehen folgende Befehle zur Verfügung:

- **Frage stellen**: Einfach Frage eingeben
- **`exit`** oder **`quit`**: Chat beenden
- **`clear`**: Konversationshistorie löschen
- **`help`**: Hilfe anzeigen

### Beispiel-Session

```
💬 PDF Chat Session
══════════════════════════════════════════════════════════════════════

📄 PDF: merged_all_documents.pdf
�� Provider: OPENAI
🎯 Model: gpt-4o
📝 PDF Length: 15420 characters

You: Was sind die Hauptthemen in diesem Dokument?

AI: Basierend auf dem PDF sind die Hauptthemen...

You: Fasse die wichtigsten Punkte zusammen

AI: Die wichtigsten Punkte sind: 1. ...

You: exit
👋 Goodbye!
```

### API Keys erhalten

- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: https://makersuite.google.com/app/apikey


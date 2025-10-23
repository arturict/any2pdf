# any2pdf 📄→📑

> **Convert ANY file format to searchable PDFs - Perfect for ChatGPT & AI Tools!**

Ein Python-Tool zur Konvertierung von verschiedensten Dateiformaten in durchsuchbare PDFs für die Verwendung mit KI-Tools wie ChatGPT.

## ✨ Features

- 📄 **Office-Dokumente**: Konvertiert PPTX, DOCX, DOC, PPT, XLSX, XLS, ODT, ODP, ODS, RTF
- 🖼️ **Bilder**: Konvertiert JPG, PNG, GIF, BMP, TIFF, WEBP, SVG, HEIC
- 📝 **Text-Dateien**: Konvertiert TXT, MD, CSV, TSV, LOG, JSON, XML, HTML
- 📑 **PDF-Verarbeitung**: Kopiert existierende PDFs und wendet OCR an
- 🔍 **OCR**: Macht alle Dokumente durchsuchbar mit Texterkennung (Deutsch & Englisch)
- 📁 **Batch-Verarbeitung**: Verarbeitet ganze Ordner mit Unterordnern
- 🔗 **PDF-Zusammenführung**: Optional alle PDFs in einem Dokument zusammenführen
- 🤖 **AI Chat Integration**: Chatte mit deinen PDFs über OpenAI (GPT-5, GPT-4.1) oder Google Gemini (2.5-Pro, 2.0)
- 🧠 **GPT-5 Reasoning Control**: Wähle Reasoning Effort (minimal/low/medium/high) für optimale Balance zwischen Speed & Quality
- ⚡ **Parallel Processing**: 50-70% schneller durch Multi-Threading
- 💾 **Smart Caching**: Überspringe bereits konvertierte Dateien automatisch
- 🚀 **Einfach zu bedienen**: Ein Befehl für alles

## 🚀 Quickstart

```bash
# 1. System-Abhängigkeiten installieren (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick

# 2. Python-Umgebung einrichten
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Dateien konvertieren
python document_to_pdf.py /pfad/zum/ordner --merge

# Nach der Konvertierung: Mit PDF chatten!
# Wähle AI Provider (OpenAI/Gemini), Modell und bei GPT-5 das Reasoning Level
```

**Windows-Nutzer**: Verwende [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/de-de/windows/wsl/install) für beste Kompatibilität:
```powershell
wsl --install  # In PowerShell als Administrator
```

## Installation

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick

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

### Windows
⚠️ **Verwende WSL (Windows Subsystem for Linux)** für beste Kompatibilität:

```powershell
# In PowerShell als Administrator:
wsl --install
```

Nach Installation von WSL, öffne Ubuntu-Terminal und folge den Ubuntu/Debian-Anweisungen.

## Verwendung

### Basis-Verwendung

```bash
# Alle Dokumente in einem Ordner konvertieren
python document_to_pdf.py /pfad/zum/ordner

# Mit Zusammenführung aller PDFs
python document_to_pdf.py /pfad/zum/ordner --merge

# Mit benutzerdefiniertem Output-Ordner
python document_to_pdf.py /pfad/zum/ordner -o /pfad/zum/output

# ⚡ Mit Parallel Processing (4 Workers)
python document_to_pdf.py /pfad/zum/ordner --merge -j 4

# Ohne OCR (schneller, aber nicht durchsuchbar)
python document_to_pdf.py /pfad/zum/ordner --no-ocr
```

### AI Chat Integration 🤖

Nach der PDF-Erstellung kannst du direkt mit deinen Dokumenten chatten:

```bash
python document_to_pdf.py ./documents --merge

# Nach der Konvertierung:
💬 Would you like to chat with the PDF using AI? (y/N): y

# Wähle:
# 1. AI Provider (OpenAI/Gemini)
# 2. Modell (z.B. gpt-5, gemini-2.5-flash)
# 3. Bei GPT-5: Reasoning Effort (minimal/low/medium/high)
```

#### Unterstützte AI Modelle

**OpenAI (GPT-5 Series)**
- `gpt-5` - Neuestes Modell mit reasoning
- `gpt-5-mini` - Schneller & günstiger
- `gpt-5-nano` - Sehr schnell für einfache Fragen
- `gpt-4.1`, `gpt-4.1-mini`, `o4-mini` - Legacy Modelle

**Google Gemini**
- `gemini-2.5-flash`, `gemini-2.5-pro` - Neueste Modelle
- `gemini-2.0-flash-exp`, `gemini-2.0-flash-thinking-exp`
- `gemini-1.5-pro`, `gemini-1.5-flash` - Legacy Modelle

#### GPT-5 Reasoning Effort 🧠

- **minimal** - ⚡⚡⚡⚡⚡ Schnellste Antworten (einfache Fragen)
- **low** - ⚡⚡⚡⚡ Schnelles Reasoning (direkte Fragen)
- **medium** - ⚡⚡⚡ Ausgewogen (DEFAULT, empfohlen)
- **high** - ⚡⚡ Tiefes Reasoning (komplexe Analyse)

## Workflow für ChatGPT / AI Tools

**Option A - Integrierter Chat (empfohlen):**
```bash
python document_to_pdf.py ./unterrichtsmaterial --merge
# Nach der Konvertierung 'y' eingeben, Provider/Modell wählen und direkt chatten!
```

**Option B - PDF hochladen:**
```bash
python document_to_pdf.py ./unterrichtsmaterial --merge
# Das zusammengeführte PDF 'merged_all_documents.pdf' zu ChatGPT/Claude hochladen
```

### Was du mit dem PDF machen kannst:
- Zusammenfassungen erstellen
- Fragen zu den Inhalten stellen
- Lernmaterialien generieren
- Code analysieren lassen
- Komplexe Dokumente verstehen

## Unterstützte Formate

**Office:** `.pptx`, `.docx`, `.doc`, `.ppt`, `.xlsx`, `.xls`, `.odt`, `.odp`, `.ods`, `.rtf`  
**Bilder:** `.jpg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`, `.heic`  
**Text:** `.txt`, `.md`, `.csv`, `.tsv`, `.log`, `.json`, `.xml`, `.html`  
**PDF:** `.pdf` (werden kopiert und optional mit OCR versehen)

## Dokumentation

- 📖 [Vollständige Anleitung](docs/USAGE.md) - Ausführliche Nutzungsanleitung
- ⚡ [Performance](docs/PERFORMANCE.md) - Benchmarks und Optimierungen
- 🏗️ [Projekt-Struktur](docs/PROJECT_STRUCTURE.md) - Code-Organisation
- 📋 [Changelog](CHANGELOG.md) - Versionshistorie

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

### "externally-managed-environment" Fehler
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Tipps

- ⚡ **Performance**: Nutze `-j 4` für parallele Konvertierung (50-70% schneller!)
- 💾 **Caching**: Bei wiederholten Läufen werden unveränderte Dateien übersprungen
- 🎯 **OCR-Qualität**: Beste Ergebnisse mit hochauflösenden Bildern (300 DPI)
- 🤖 **AI Chat**: Integrierter Chat spart Zeit beim Hochladen großer PDFs

## Lizenz

MIT License - Frei zu verwenden für Bildungszwecke.

---

**any2pdf** - Made with ❤️ for the AI community | [GitHub](https://github.com/arturict/any2pdf)

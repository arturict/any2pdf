# any2pdf 📄→📑

> **Convert ANY file format to searchable PDFs - Perfect for ChatGPT & AI Tools!**

Ein Python-Tool zur Konvertierung von verschiedensten Dateiformaten in durchsuchbare PDFs für die Verwendung mit KI-Tools wie ChatGPT.

**🎯 NEW: Now even easier! Just run `./install.sh` and `python convert.py` - that's it!**

📖 **[→ Quick Start Guide](QUICK_START.md)** | 📚 [Full Documentation](docs/USAGE.md)

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
# 1. One-Click Installation 🎯
./install.sh

# 2. Start Converting! ✨
source venv/bin/activate
python convert.py

# That's it! Interactive mode guides you through everything.
```

**Or use the CLI directly:**
```bash
./convert.sh wirtschaft  # Convert folder 'wirtschaft'
./convert.sh docs --merge  # Convert and merge all PDFs
```

**Windows-Nutzer**: Verwende [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/de-de/windows/wsl/install):
```powershell
wsl --install  # In PowerShell als Administrator
# Then run ./install.sh in Ubuntu terminal
```

## 📥 Installation

### Automatic (Recommended) 🎯

```bash
./install.sh
```

That's it! Works on Ubuntu, Debian, and macOS.

### Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### macOS
```bash
brew install libreoffice tesseract tesseract-lang poppler imagemagick

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows
⚠️ **Use WSL (Windows Subsystem for Linux)**:

```powershell
# In PowerShell as Administrator:
wsl --install
```

After WSL installation, open Ubuntu terminal and run `./install.sh`
</details>

## Verwendung

### 💫 Interaktiver Modus (Empfohlen)

Der einfachste Weg - perfekt für Anfänger:

```bash
# Super einfach - nur:
python convert.py

# Oder:
python document_to_pdf.py
```

**Features:**
- 🎨 Moderne, farbige Terminal-UI
- 📁 Visueller Ordner-Browser
- ✅ Echtzeit-Validierung
- 💡 Hilfreiche Erklärungen zu jeder Option
- 🎯 Intelligente Standard-Einstellungen

**Walkthrough:**
1. Wähle Source-Ordner (mit Pfad-Autovervollständigung)
2. Optional: Custom Output-Ordner
3. OCR aktivieren? (Empfohlen für durchsuchbare PDFs)
4. Alle PDFs zusammenführen? (Perfekt für ChatGPT)
5. Anzahl paralleler Workers (4 empfohlen)
6. Smart Caching aktivieren? (Spart Zeit bei Re-Runs)
7. Konfiguration bestätigen und starten!

**[→ Ausführliche Anleitung: Interactive Mode Guide](docs/INTERACTIVE_MODE.md)**

### ⌨️ CLI-Modus (Für Experten & Scripts)

Direkter Zugriff mit Kommandozeilen-Flags:

```bash
# Quick way with convert.sh wrapper:
./convert.sh wirtschaft              # Convert folder
./convert.sh docs --merge            # Convert and merge
./convert.sh docs --merge -j 4       # With parallel processing

# Or directly with python:
python convert.py /pfad/zum/ordner
python convert.py /pfad/zum/ordner --merge
python convert.py /pfad/zum/ordner -o /pfad/zum/output
python convert.py /pfad/zum/ordner --merge -j 4
python convert.py /pfad/zum/ordner --no-ocr
python convert.py --help
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
./convert.sh ./unterrichtsmaterial --merge
# Oder: python convert.py ./unterrichtsmaterial --merge
# Nach der Konvertierung 'y' eingeben, Provider/Modell wählen und direkt chatten!
```

**Option B - PDF hochladen:**
```bash
./convert.sh ./unterrichtsmaterial --merge
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

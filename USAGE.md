# Document to PDF Converter - Verwendungsanleitung

> **any2pdf** - Convert anything to PDF!

## Dateien

- **document_to_pdf.py** - Hauptprogramm für Konvertierung aller Formate
- **flatten_files.py** - Hilfstool zum Sammeln von Dateien aus Unterordnern
- **convert.sh** - Einfacher Wrapper (führt Setup aus falls nötig)
- **requirements.txt** - Python-Abhängigkeiten
- **setup.sh** - Automatisches Setup-Script für Ubuntu/Debian
- **README.md** - Vollständige Dokumentation

## Verwendung

### Schnellstart (empfohlen)

```bash
# Einfach ausführen - Setup erfolgt automatisch
./convert.sh ./meine_dokumente --merge
```

### Quick Start (mit setup.sh)

```bash
# Alle Abhängigkeiten automatisch installieren
./setup.sh

# Virtual Environment aktivieren
source venv/bin/activate

# Dokumente konvertieren und zusammenführen
python document_to_pdf.py ./deine_dokumente --merge
```

### Manuelles Setup

```bash
# System-Tools installieren
sudo apt-get update
sudo apt-get install -y libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick

# Python Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Konvertieren
python document_to_pdf.py ./deine_dokumente --merge
```

## Workflow für ChatGPT/Claude

### Einfachster Workflow (alles in einem PDF)

1. **Alle Dateien konvertieren und mergen**
   ```bash
   ./convert.sh ./meine_dokumente --merge
   ```

2. **Ein PDF hochladen**
   - Lade `converted_pdfs/merged_all_documents.pdf` zu ChatGPT hoch
   - Fertig! Alle Dateien sind in einem durchsuchbaren PDF

### Alternativer Workflow (einzelne PDFs)

1. **Dateien vorbereiten** (optional)
   - Sammle alle Materialien in einem Ordner
   - Oder nutze `flatten_files.py` um Dateien aus Unterordnern zu sammeln
   ```bash
   python flatten_files.py ./meine_dokumente
   ```

2. **Konvertieren**
   ```bash
   python document_to_pdf.py ./flattened_files
   ```

3. **Nutzen**
   - Alle PDFs sind im `converted_pdfs` Ordner
   - Hochladen zu ChatGPT, Claude oder anderen KI-Tools
   - PDFs sind durchsuchbar dank OCR

## Kommandozeilen-Optionen

```bash
# Basis: Konvertiere alles
python document_to_pdf.py /pfad/zum/ordner

# Merge: Alle in einem PDF
python document_to_pdf.py /pfad/zum/ordner --merge

# Eigener Output-Ordner
python document_to_pdf.py /pfad/zum/ordner -o /pfad/zum/output --merge

# Ohne OCR (schneller, aber nicht durchsuchbar)
python document_to_pdf.py /pfad/zum/ordner --no-ocr

# Alle Optionen kombiniert
python document_to_pdf.py /pfad/zum/ordner -o ./output --merge --no-ocr
```

## Unterstützte Formate

### Office-Dokumente
✅ PowerPoint: `.pptx`, `.ppt`
✅ Word: `.docx`, `.doc`
✅ Excel: `.xlsx`, `.xls`
✅ OpenDocument: `.odt`, `.odp`, `.ods`
✅ Rich Text: `.rtf`

### Bilder
✅ Standard: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
✅ Erweitert: `.tiff`, `.tif`, `.webp`, `.svg`, `.heic`

### Text-Dateien
✅ Plain Text: `.txt`
✅ Markdown: `.md`
✅ Daten: `.csv`, `.tsv`
✅ Logs: `.log`
✅ Markup: `.json`, `.xml`, `.html`, `.htm`

### PDF
✅ Existierende PDFs: `.pdf` (werden kopiert und mit OCR versehen)

## Features

✅ Alle gängigen Office-Formate → PDF
✅ Alle Bildformate → PDF  
✅ Text-Dateien → PDF
✅ Existierende PDFs verarbeiten
✅ OCR für durchsuchbaren Text (Deutsch & Englisch)
✅ **PDF-Zusammenführung** (alle Dokumente in einem PDF)
✅ Batch-Verarbeitung
✅ Automatische Namensgebung
✅ Vollständige Unterordner-Unterstützung

## Beispiele

### Beispiel 1: Unterrichtsmaterialien für ChatGPT vorbereiten
```bash
# Konvertiere und merge alles
./convert.sh ./unterricht --merge

# → Ergebnis: converted_pdfs/merged_all_documents.pdf
# → Zu ChatGPT hochladen und analysieren lassen
```

### Beispiel 2: Gemischte Dateitypen konvertieren
```bash
# Ordner mit PPTX, DOCX, JPG, PDF, TXT Dateien
python document_to_pdf.py ./gemischte_dateien --merge

# Alle werden zu PDFs konvertiert und zusammengeführt
```

### Beispiel 3: Schnelle Konvertierung ohne OCR
```bash
# Wenn keine Texterkennung benötigt wird
python document_to_pdf.py ./bilder --no-ocr --merge
```

### Beispiel 4: Aus Unterordnern sammeln und konvertieren
```bash
# Schritt 1: Dateien sammeln
python flatten_files.py ./projekt_ordner

# Schritt 2: Konvertieren und mergen
python document_to_pdf.py ./flattened_files --merge
```

## Test-Beispiel

```bash
# Teste mit mitgelieferten Test-Dateien
cd test_files
../convert.sh . --merge

# Prüfe das Ergebnis
ls -la converted_pdfs/
```

## Tipps & Tricks

💡 **Für ChatGPT**: Nutze immer `--merge` um alle Dateien in einem PDF zu haben
💡 **Große Mengen**: Konvertierung kann bei vielen Dateien Zeit brauchen
💡 **OCR-Qualität**: Beste Ergebnisse mit hochauflösenden Bildern (300 DPI)
💡 **Performance**: Ohne `--no-ocr` ist langsamer, aber PDFs sind durchsuchbar
💡 **Sprachen**: Standard ist Deutsch + Englisch, weitere per Tesseract installierbar

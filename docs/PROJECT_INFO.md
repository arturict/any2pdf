# Document to PDF Converter - Projektinformationen

## 📋 Übersicht

Ein vollständiges Python-Tool zur Konvertierung von Unterrichtsmaterialien in durchsuchbare PDFs für die Verwendung mit KI-Tools wie ChatGPT, Claude, etc.

## 🎯 Hauptzweck

- Schnelle Konvertierung von Office-Dokumenten (PPTX, DOCX) und Bildern zu PDF
- OCR-Integration für durchsuchbaren Text
- Optimiert für Upload zu KI-Assistenten
- Batch-Verarbeitung von ganzen Ordnern mit Unterordnern

## 📁 Projektstruktur

```
file-from-folder/
├── document_to_pdf.py          # 🎯 Hauptprogramm
├── flatten_files.py            # 📦 Dateien aus Unterordnern sammeln
├── test_converter.py           # ✅ Dependency-Tests
├── examples.py                 # 📚 Verwendungsbeispiele
│
├── requirements.txt            # 📦 Python-Abhängigkeiten
├── setup.sh                    # 🚀 Automatisches Setup
│
├── README.md                   # 📖 Vollständige Dokumentation
├── USAGE.md                    # 📝 Verwendungsanleitung
├── QUICKSTART.md               # ⚡ Schnellstart
├── PROJECT_INFO.md             # ℹ️ Diese Datei
│
├── LICENSE                     # ⚖️ MIT Lizenz
├── .gitignore                  # 🚫 Git-Ausschlüsse
│
├── venv/                       # 🐍 Python Virtual Environment
├── converted_pdfs/             # 📄 Output-Ordner (Beispiel)
└── flattened_files/            # 📁 Flache Dateien (Beispiel)
```

## 🔧 Kernfunktionalitäten

### 1. document_to_pdf.py
- **Hauptfunktion:** Konvertiert Dokumente zu PDFs
- **Features:**
  - Office-Dokumente via LibreOffice
  - Bilder mit OCR
  - Batch-Verarbeitung
  - Automatische Namensgebung bei Duplikaten
  - Unterordner-Support
  - OCR optional aktivierbar/deaktivierbar

### 2. flatten_files.py
- **Funktion:** Sammelt Dateien aus Unterordnern
- **Nutzen:** Vorbereitung für Batch-Konvertierung
- **Feature:** Automatische Umbenennung bei Duplikaten

### 3. test_converter.py
- **Funktion:** Prüft Systemabhängigkeiten
- **Nutzen:** Schnelle Diagnose von Installationsproblemen

## 🛠️ Technologie-Stack

### Python-Bibliotheken
- **Pillow** - Bildverarbeitung
- **pytesseract** - OCR-Integration
- **PyMuPDF (fitz)** - PDF-Manipulation
- **pdf2image** - PDF-zu-Bild-Konvertierung

### System-Tools
- **LibreOffice** - Office-Dokument-Konvertierung (erforderlich)
- **Tesseract OCR** - Texterkennung (optional)
- **Poppler** - PDF-Utilities (optional)
- **ImageMagick** - Bild-zu-PDF (optional)

## 📊 Unterstützte Formate

### Input-Formate

#### Office-Dokumente (LibreOffice erforderlich)
- PowerPoint: `.pptx`, `.ppt`
- Word: `.docx`, `.doc`
- Excel: `.xlsx`, `.xls`
- OpenDocument: `.odt`, `.odp`

#### Bilder (ImageMagick oder Python-Libs)
- Standard: `.jpg`, `.jpeg`, `.png`
- Erweitert: `.gif`, `.bmp`, `.tiff`, `.tif`, `.webp`

### Output-Format
- PDF mit eingebettetem Text (durchsuchbar)
- Optimiert für KI-Analyse

## 🚀 Verwendungsszenarien

### 1. Unterrichtsmaterialien für ChatGPT vorbereiten
```bash
python document_to_pdf.py ./kursmaterial
# → Upload zu ChatGPT für Zusammenfassungen
```

### 2. Präsentationen archivieren
```bash
python document_to_pdf.py ./presentations -o ./archive
```

### 3. Schnelle Konvertierung ohne OCR
```bash
python document_to_pdf.py ./docs --no-ocr
```

### 4. Dokumente aus verschiedenen Ordnern sammeln
```bash
python flatten_files.py ./verschiedene_ordner
python document_to_pdf.py ./flattened_files
```

## 💡 Best Practices

1. **Virtual Environment verwenden**
   ```bash
   source venv/bin/activate
   ```

2. **Dependencies vorher prüfen**
   ```bash
   python test_converter.py
   ```

3. **OCR für bessere Ergebnisse**
   - Mit OCR: Text ist durchsuchbar und kopierbar
   - Ohne OCR: Schneller, aber nur Bilder

4. **Große Batches**
   - Bei vielen Dateien kann Konvertierung lange dauern
   - LibreOffice braucht Zeit pro Dokument

5. **Für KI-Tools**
   - OCR aktiviert lassen
   - PDFs einzeln oder in kleinen Batches hochladen
   - Gute Ergebnisse bei klaren, hochauflösenden Quellen

## 📈 Performance

- **PPTX → PDF:** ~10-30 Sekunden pro Datei
- **DOCX → PDF:** ~5-15 Sekunden pro Datei
- **Bild → PDF (mit OCR):** ~5-10 Sekunden pro Bild
- **Bild → PDF (ohne OCR):** ~1-2 Sekunden pro Bild

*Zeiten variieren je nach Dateigröße und Systemleistung*

## 🔍 Troubleshooting

### Problem: LibreOffice nicht gefunden
```bash
sudo apt-get install libreoffice
```

### Problem: OCR funktioniert nicht
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-deu poppler-utils
pip install pytesseract pdf2image PyMuPDF
```

### Problem: Virtual Environment Fehler
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: Konvertierung schlägt fehl
- Prüfe Dateinamen (keine Sonderzeichen)
- Prüfe Dateigröße (sehr große Dateien können Timeout verursachen)
- Prüfe Datei-Integrität (korrupte Dateien)

## 🎓 Lernmaterial-Workflow

### Kompletter Workflow für Studierende

1. **Material sammeln**
   ```bash
   # Alle Vorlesungsfolien, Skripte, etc. in einen Ordner
   python flatten_files.py ~/Downloads/Semester3
   ```

2. **Zu PDF konvertieren**
   ```bash
   source venv/bin/activate
   python document_to_pdf.py ~/Downloads/Semester3/flattened_files
   ```

3. **Zu ChatGPT/Claude hochladen**
   - Alle PDFs aus `converted_pdfs/` Ordner
   - Einzeln oder als Gruppe

4. **Mit KI arbeiten**
   - "Erstelle eine Zusammenfassung dieser Vorlesung"
   - "Erkläre die Hauptkonzepte"
   - "Generiere Übungsfragen"
   - "Erstelle Karteikarten"

## 📝 Lizenz

MIT License - Frei verwendbar für Bildungszwecke

## 🤝 Beiträge

Dieses Projekt ist für persönliche und Bildungszwecke erstellt.
Verbesserungsvorschläge sind willkommen!

## 📞 Support

Bei Problemen:
1. Prüfe `README.md` für Installation
2. Führe `python test_converter.py` aus
3. Prüfe `TROUBLESHOOTING.md` für bekannte Probleme

## 🔄 Updates

Das Projekt ist stabil und funktional. Mögliche zukünftige Erweiterungen:
- Web-Interface
- Weitere Ausgabeformate
- Cloud-Integration
- Batch-OCR-Optimierung

---

**Version:** 1.0  
**Datum:** Oktober 2025  
**Python:** 3.7+  
**Plattform:** Linux (Ubuntu/Debian), macOS

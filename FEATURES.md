# any2pdf - Feature Summary

## 🎯 Hauptziel

Konvertiere ALLE gängigen Dateiformate aus einem Ordner (und Unterordner) in durchsuchbare PDFs - ideal für die Verwendung mit ChatGPT, Claude und anderen KI-Tools.

## ✨ Neue Features (nach Update)

### 1. Erweiterte Format-Unterstützung
- **Office**: PPTX, DOCX, DOC, PPT, XLSX, XLS, ODT, ODP, ODS, RTF (neu: ODS, RTF)
- **Bilder**: JPG, PNG, GIF, BMP, TIFF, WEBP, SVG, HEIC (neu: SVG, HEIC)
- **Text**: TXT, MD, CSV, TSV, LOG, JSON, XML, HTML, HTM (komplett neu!)
- **PDF**: Existierende PDFs werden kopiert und optional mit OCR versehen (neu!)

### 2. PDF-Zusammenführung (--merge)
- **NEU**: Alle konvertierten PDFs werden in EINEM großen PDF zusammengeführt
- Ideal für ChatGPT: Einfach ein Dokument hochladen statt viele einzelne
- Sortierte Ausgabe für bessere Übersicht

### 3. Bessere Benutzerfreundlichkeit
- **convert.sh**: Einfacher Wrapper-Script, macht automatisch Setup
- **Erweiterte Fehlerbehandlung**: Bessere Fehlermeldungen
- **Sortierte Ausgabe**: Dateien werden alphabetisch sortiert verarbeitet
- **Duplikat-Handling**: Automatische Umbenennung bei Namenskonflikten

### 4. Text-Datei-Konvertierung
- Neu: Direkte Konvertierung von TXT, MD, CSV, JSON, XML, HTML zu PDF
- Formatierung wird beibehalten
- Keine externen Tools nötig (nutzt PyMuPDF)

## 🚀 Schnellstart

```bash
# Einfachste Verwendung - alles automatisch!
./convert.sh /pfad/zu/dateien --merge

# Oder manuell
python3 document_to_pdf.py /pfad/zu/dateien --merge
```

## 📊 Vergleich Alt vs. Neu

| Feature | Vorher | Jetzt |
|---------|--------|-------|
| Office-Formate | 8 Formate | 10 Formate |
| Bild-Formate | 7 Formate | 9 Formate |
| Text-Formate | 0 | 9 Formate |
| PDF-Verarbeitung | ✗ | ✓ |
| PDF-Merge | ✗ | ✓ |
| Wrapper-Script | ✗ | ✓ |
| Duplikat-Handling | Basis | Erweitert |

## 💡 Hauptanwendungsfall: ChatGPT

### Workflow
1. Ordner mit gemischten Dateien haben
2. Einen Befehl ausführen:
   ```bash
   ./convert.sh ./meine-dokumente --merge
   ```
3. Ein PDF hochladen: `converted_pdfs/merged_all_documents.pdf`
4. Fertig! ChatGPT kann alles analysieren

### Vorteile
- ✅ Ein PDF statt viele einzelne Dateien
- ✅ Alle Dateitypen werden unterstützt
- ✅ Text ist durchsuchbar (OCR)
- ✅ Maximale Kompatibilität mit KI-Tools

## 🛠️ Technische Verbesserungen

1. **Modularere Code-Struktur**
   - Neue Methoden: `convert_text_to_pdf()`, `copy_pdf()`, `merge_pdfs()`
   - Bessere Trennung der Konvertierungslogiken

2. **Robustere Fehlerbehandlung**
   - Automatische Duplikat-Umbenennung
   - Bessere Timeout-Behandlung
   - Fortfahren bei Fehlern statt Abbruch

3. **Optimierte Performance**
   - Sortierte Verarbeitung
   - Besseres Memory-Management bei Merge

## 📝 Kommandozeilen-Optionen

```bash
# Alle Optionen
python document_to_pdf.py [ORDNER] [OPTIONEN]

Optionen:
  -o, --output OUTPUT    Eigener Output-Ordner
  --no-ocr              Ohne OCR (schneller)
  -m, --merge           Alle PDFs zusammenführen
  -h, --help            Hilfe anzeigen
```

## 🎓 Beispiele

### Beispiel 1: Unterrichtsmaterialien
```bash
# PPTX, DOCX, PDF, Bilder alle zusammen
./convert.sh ./unterricht --merge
```

### Beispiel 2: Gemischter Ordner
```bash
# Word, Excel, Bilder, Text-Dateien, PDFs
./convert.sh ./dokumente --merge -o ./output
```

### Beispiel 3: Ohne OCR (schnell)
```bash
# Schnelle Konvertierung für Testing
./convert.sh ./test_files --no-ocr --merge
```

## 📦 Dateistruktur

```
file-from-folder/
├── document_to_pdf.py      # Hauptprogramm ⭐
├── convert.sh              # Einfacher Wrapper (neu)
├── flatten_files.py        # Hilfstool
├── examples.py             # Erweiterte Beispiele
├── requirements.txt        # Python-Dependencies
├── setup.sh                # Auto-Setup
├── README.md               # Hauptdokumentation
├── QUICKSTART.md           # Schnellstart-Guide
├── USAGE.md                # Ausführliche Anleitung
└── test_files/             # Test-Dateien
```

## 🔧 Abhängigkeiten

### System
- LibreOffice (Office-Dokumente)
- Tesseract OCR (Texterkennung)
- Poppler (PDF-Verarbeitung)
- ImageMagick (Bild-Konvertierung)

### Python
- Pillow (Bildverarbeitung)
- pytesseract (OCR)
- PyMuPDF (PDF-Erstellung/Merge)
- pdf2image (PDF-zu-Bild)

## 🎯 Zielgruppen

1. **Studierende**: Unterrichtsmaterialien für KI-gestützte Zusammenfassungen
2. **Lehrer**: Materialen bündeln und aufbereiten
3. **Researchers**: Dokumente für Analyse vorbereiten
4. **Allgemein**: Beliebige Dokumente für ChatGPT/Claude aufbereiten

## 🚨 Breaking Changes

Keine! Alle bestehenden Funktionen bleiben erhalten. Neue Features sind optional (--merge).

## 📈 Zukünftige Erweiterungen (optional)

- [ ] Fortschrittsbalken für lange Konvertierungen
- [ ] Multi-Threading für parallele Konvertierung
- [ ] Web-UI für einfachere Bedienung
- [ ] Automatische Kompression für kleinere PDFs
- [ ] Weitere OCR-Sprachen

## 🙏 Feedback

Dieses Tool ist jetzt ein generisches, robustes Werkzeug für die Konvertierung verschiedenster Dateiformate in durchsuchbare PDFs - perfekt für die Verwendung mit modernen KI-Tools!

**any2pdf** - [GitHub](https://github.com/arturict/any2pdf) | Made with ❤️ for the AI community

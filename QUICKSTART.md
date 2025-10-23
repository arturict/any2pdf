# Quick Reference

## Installation (Eine Zeile)
```bash
sudo apt-get update && sudo apt-get install -y libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils imagemagick && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

## Oder automatisch:
```bash
./setup.sh
```

## Verwendung

### Basis (alles in EINEM PDF)
```bash
source venv/bin/activate
python document_to_pdf.py /pfad/zum/ordner --merge
```

### Einzelne PDFs
```bash
python document_to_pdf.py /pfad/zum/ordner
```

### Mit Output-Ordner
```bash
python document_to_pdf.py /pfad/zum/ordner -o /pfad/zum/output --merge
```

### Ohne OCR (schneller)
```bash
python document_to_pdf.py /pfad/zum/ordner --no-ocr --merge
```

## Hilfsprogramme

### Dateien aus Unterordnern sammeln
```bash
python flatten_files.py /pfad/zum/ordner
```

### Testen
```bash
python test_converter.py
```

## Unterstützte Formate

**Office:** .pptx, .docx, .doc, .ppt, .xlsx, .xls, .odt, .odp, .ods, .rtf  
**Bilder:** .jpg, .jpeg, .png, .gif, .bmp, .tiff, .tif, .webp, .svg, .heic  
**Text:** .txt, .md, .csv, .tsv, .log, .json, .xml, .html, .htm  
**PDF:** .pdf (wird kopiert und mit OCR versehen)

## Typischer Workflow für ChatGPT

1. Alle Dateien in einem PDF zusammenführen
   ```bash
   source venv/bin/activate
   python document_to_pdf.py ./meine_dokumente --merge
   ```

2. Das `merged_all_documents.pdf` zu ChatGPT hochladen

3. Zusammenfassungen erstellen lassen oder Fragen stellen

**Das war's!** Alle Dateien sind jetzt in einem durchsuchbaren PDF! 🎉

## Troubleshooting

**Virtual Environment aktivieren:**
```bash
source venv/bin/activate
```

**Dependencies prüfen:**
```bash
python test_converter.py
```

**LibreOffice installieren:**
```bash
sudo apt-get install libreoffice
```

**OCR installieren:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-deu poppler-utils
```

## Output

- **Ohne --merge**: Einzelne PDFs in `<source_folder>/converted_pdfs/`
- **Mit --merge**: Ein `merged_all_documents.pdf` im Output-Ordner
- Oder im angegebenen Output-Ordner mit `-o`

Die PDFs sind:
- ✅ Durchsuchbar (mit OCR)
- ✅ Optimiert für KI-Analyse (ChatGPT, Claude)
- ✅ Deutsch & Englisch Text erkannt
- ✅ Behalten Original-Layout
- ✅ Alle Formate zusammen in einem Dokument (mit --merge)

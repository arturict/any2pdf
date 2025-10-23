# Changelog

## Version 2.0 (Oktober 2024)

### 🎉 Neue Features

#### Format-Unterstützung erweitert
- **Text-Dateien**: Neu unterstützt TXT, MD, CSV, TSV, LOG, JSON, XML, HTML, HTM (9 neue Formate)
- **Bilder**: Neu unterstützt SVG, HEIC (2 neue Formate)
- **Office**: Neu unterstützt ODS, RTF (2 neue Formate)
- **PDF**: Existierende PDFs können jetzt verarbeitet werden (kopieren + OCR)
- **Gesamt**: Von 15 auf 30+ unterstützte Formate erweitert!

#### PDF-Zusammenführung (--merge)
- Neue Option `--merge` / `-m` zum Zusammenführen aller PDFs
- Erstellt `merged_all_documents.pdf` im Output-Ordner
- Ideal für ChatGPT: Ein PDF statt viele einzelne Dateien
- Sortierte Zusammenführung für bessere Übersicht

#### Benutzerfreundlichkeit
- **convert.sh**: Neuer Wrapper-Script für einfache Verwendung
- Automatischer Setup-Check und Aktivierung
- Verbesserte Fehlerbehandlung
- Bessere Duplikat-Erkennung und -Umbenennung
- Sortierte Dateiverarbeitung (alphabetisch)

### 🔧 Technische Verbesserungen

#### Code-Struktur
- Neue Methode: `convert_text_to_pdf()` für Text-Dateien
- Neue Methode: `copy_pdf()` für PDF-Verarbeitung
- Neue Methode: `merge_pdfs()` für PDF-Zusammenführung
- Bessere Modularisierung und Wartbarkeit

#### Robustheit
- Verbesserte Fehlerbehandlung bei Namenskonflikten
- Automatische Duplikat-Umbenennung mit Countern
- Fortfahren bei Fehlern statt Abbruch
- Tracking aller konvertierten PDFs für Merge

#### Performance
- Sortierte Verarbeitung für konsistente Ergebnisse
- Optimiertes Memory-Management beim Mergen
- Besseres Timeout-Handling

### 📚 Dokumentation

#### Neue Dokumente
- **FEATURES.md**: Feature-Übersicht und Vergleich Alt vs. Neu
- **SUMMARY.md**: Kompakte Projekt-Zusammenfassung
- **CHANGELOG.md**: Diese Datei

#### Aktualisierte Dokumente
- **README.md**: Alle neuen Features dokumentiert
- **QUICKSTART.md**: Merge-Workflow hinzugefügt
- **USAGE.md**: Erweiterte Beispiele und Tipps
- **examples.py**: Neue Beispiele für Text-Konvertierung und Merge

### 🐛 Bugfixes
- Duplikat-Handling bei Output-Dateien verbessert
- Pfad-Handling für Windows-Kompatibilität optimiert
- Bessere Fehlerbehandlung bei fehlenden Dependencies

### ⚠️ Breaking Changes
Keine! Alle bestehenden Funktionen bleiben kompatibel. Neue Features sind optional.

---

## Version 1.0 (Original)

### Features
- PPTX, DOCX, DOC, PPT Konvertierung
- Basis-Bilder-Konvertierung (JPG, PNG, GIF, BMP, TIFF, WEBP)
- OCR für durchsuchbare PDFs (Deutsch & Englisch)
- Batch-Verarbeitung mit Unterordner-Support
- LibreOffice-Integration
- Tesseract OCR-Integration

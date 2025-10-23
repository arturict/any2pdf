# Windows Setup mit WSL (Windows Subsystem for Linux)

## 🪟 Warum WSL für any2pdf?

any2pdf benötigt mehrere Linux-Tools (LibreOffice, Tesseract OCR, etc.), die unter Windows nicht optimal laufen. Mit WSL erhältst du:

- ✅ **Native Linux-Umgebung** unter Windows
- ✅ **Bessere Performance** und Kompatibilität
- ✅ **Einfache Installation** aller Dependencies
- ✅ **Zugriff auf deine Windows-Dateien** (unter `/mnt/c/`)

## 📦 Installation

### Schritt 1: WSL installieren

```powershell
# Öffne PowerShell als Administrator und führe aus:
wsl --install
```

Das installiert:
- WSL 2
- Ubuntu (Standard-Distribution)
- Virtual Machine Platform

**Neustart erforderlich!** Starte deinen Computer nach der Installation neu.

### Schritt 2: Ubuntu einrichten

Nach dem Neustart:
1. Ubuntu öffnet sich automatisch
2. Erstelle einen Benutzernamen (z.B. dein Windows-Username)
3. Erstelle ein Passwort (wird beim Tippen nicht angezeigt - das ist normal!)

### Schritt 3: Ubuntu aktualisieren

```bash
# Im Ubuntu-Terminal:
sudo apt update && sudo apt upgrade -y
```

### Schritt 4: any2pdf installieren

```bash
# 1. System-Dependencies installieren
sudo apt-get update && sudo apt-get install -y \
    git \
    libreoffice \
    tesseract-ocr tesseract-ocr-deu \
    poppler-utils \
    imagemagick \
    python3 \
    python3-pip \
    python3-venv

# 2. Repository klonen
cd ~
git clone https://github.com/arturict/any2pdf.git
cd any2pdf

# 3. Setup ausführen
./setup.sh
```

## 🚀 Verwendung

### Dateien von Windows konvertieren

Deine Windows-Laufwerke sind unter `/mnt/` verfügbar:
- `C:\` → `/mnt/c/`
- `D:\` → `/mnt/d/`

```bash
# Aktiviere die virtuelle Umgebung
cd ~/any2pdf
source venv/bin/activate

# Beispiel: Dateien von C:\Users\DeinName\Documents konvertieren
python document_to_pdf.py /mnt/c/Users/DeinName/Documents --merge

# Oder mit relativem Pfad
python document_to_pdf.py /mnt/c/Users/$USER/Documents --merge
```

### Output auf Windows-Desktop speichern

```bash
# Konvertierte PDFs direkt auf den Desktop
python document_to_pdf.py /mnt/c/Users/$USER/Documents \
    -o /mnt/c/Users/$USER/Desktop/converted_pdfs \
    --merge
```

## 💡 Tipps & Tricks

### 1. Ubuntu-Terminal schnell öffnen

**Methode A: Über Windows-Suche**
- Windows-Taste drücken
- "Ubuntu" tippen
- Enter drücken

**Methode B: Über Windows Terminal**
- Windows Terminal installieren (aus Microsoft Store)
- Automatisch Ubuntu-Tab verfügbar

### 2. Windows Explorer in WSL öffnen

```bash
# Öffnet den aktuellen Ordner im Windows Explorer
explorer.exe .
```

### 3. VS Code mit WSL verwenden

```bash
# VS Code im WSL-Modus öffnen
code .
```

### 4. Dateien zwischen Windows und WSL kopieren

```bash
# Von Windows nach WSL
cp /mnt/c/Users/DeinName/file.txt ~/any2pdf/

# Von WSL nach Windows
cp ~/any2pdf/output.pdf /mnt/c/Users/DeinName/Desktop/
```

### 5. Schnellzugriff mit Alias

Füge dies zu `~/.bashrc` hinzu:

```bash
# Bearbeite .bashrc
nano ~/.bashrc

# Füge am Ende hinzu:
alias any2pdf='cd ~/any2pdf && source venv/bin/activate'
alias docs='cd /mnt/c/Users/$USER/Documents'
alias desktop='cd /mnt/c/Users/$USER/Desktop'

# Speichern: Ctrl+O, Enter, Ctrl+X
# Neu laden:
source ~/.bashrc

# Jetzt kannst du einfach tippen:
any2pdf
docs
```

## 🔧 Troubleshooting

### Problem: "wsl --install" funktioniert nicht

**Lösung 1: Windows aktualisieren**
```powershell
# Prüfe Windows-Version (mindestens Windows 10 Version 2004)
winver
```

**Lösung 2: Manuell aktivieren**
```powershell
# In PowerShell als Administrator:
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
# Neustart
# Dann:
wsl --install -d Ubuntu
```

### Problem: Permission denied bei /mnt/c/

```bash
# Berechtigungen anpassen
sudo chmod -R a+rwx /mnt/c/Users/$USER/Documents
```

### Problem: LibreOffice startet nicht

```bash
# LibreOffice neu installieren
sudo apt-get remove --purge libreoffice
sudo apt-get install libreoffice
```

### Problem: OCR funktioniert nicht

```bash
# Tesseract neu installieren
sudo apt-get install --reinstall tesseract-ocr tesseract-ocr-deu
```

### Problem: Python-Module fehlen

```bash
cd ~/any2pdf
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 📚 WSL-Kommandos

```bash
# WSL-Status prüfen (in PowerShell)
wsl --status

# WSL-Version prüfen
wsl --version

# Ubuntu starten
wsl

# Ubuntu beenden
exit
# oder Ctrl+D

# WSL herunterfahren (in PowerShell)
wsl --shutdown

# Ubuntu zurücksetzen (VORSICHT: Löscht alle Daten!)
wsl --unregister Ubuntu
wsl --install -d Ubuntu
```

## 🎯 Vollständiges Beispiel

```bash
# 1. Ubuntu-Terminal öffnen
# 2. In any2pdf-Ordner wechseln
cd ~/any2pdf
source venv/bin/activate

# 3. Dateien von Windows konvertieren
python document_to_pdf.py /mnt/c/Users/DeinName/Documents/Unterricht --merge

# 4. Output ist in:
# Windows-Pfad: C:\Users\DeinName\Documents\Unterricht\converted_pdfs\
# WSL-Pfad: /mnt/c/Users/DeinName/Documents/Unterricht/converted_pdfs/

# 5. Merged PDF zu ChatGPT hochladen:
# → merged_all_documents.pdf
```

## 📖 Weitere Ressourcen

- [Microsoft WSL Dokumentation](https://learn.microsoft.com/de-de/windows/wsl/)
- [WSL Best Practices](https://learn.microsoft.com/de-de/windows/wsl/setup/environment)
- [WSL FAQ](https://learn.microsoft.com/de-de/windows/wsl/faq)

---

**any2pdf** - [GitHub](https://github.com/arturict/any2pdf) | Made with ❤️ for the AI community

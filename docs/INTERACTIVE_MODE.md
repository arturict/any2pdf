# Interactive Mode Guide

## Overview

The **any2pdf** interactive mode provides a beautiful, user-friendly CLI experience for converting documents to PDF. It uses modern terminal UI libraries to guide you through the conversion process with visual prompts and validations.

## Features

✨ **Modern Terminal UI**
- Color-coded prompts with icons
- Directory browser for easy folder selection
- Grouped model selection by version
- Real-time validation
- Progress indicators

🎯 **Smart Defaults**
- Recommends optimal settings
- Shows file count in source folder
- Pre-configured for best performance
- Intelligent caching enabled by default

🔍 **Helpful Context**
- Explains each option
- Shows what each setting does
- Provides quick tips
- Links to API key pages

## Installation

### Core Dependencies

```bash
# Install system dependencies
./setup.sh

# Install Python packages with interactive mode support
pip install -r requirements.txt
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install all packages
pip install -r requirements.txt
```

## Usage

### Starting Interactive Mode

Simply run the script without any arguments:

```bash
python3 document_to_pdf.py
```

Or with venv:

```bash
source venv/bin/activate
python3 document_to_pdf.py
```

### Step-by-Step Walkthrough

#### 1. Source Folder Selection

```
📁 Source folder (containing documents to convert):
> /path/to/your/documents
```

- Use arrow keys to navigate
- Press Tab for autocomplete
- Press Enter to select
- ESC or Ctrl+C to cancel

The script will automatically scan and show how many convertible files were found.

#### 2. Output Folder

```
📂 Use custom output folder?
   (default: /path/to/documents/converted_pdfs)
> ○ No
  ○ Yes
```

- Default creates a `converted_pdfs` subfolder
- Choose "Yes" to specify a custom location

#### 3. OCR Settings

```
🔍 Enable OCR (Optical Character Recognition)?
   Makes PDFs searchable and better for AI analysis (recommended)
> ● Yes
  ○ No
```

**Recommended:** Yes
- Makes PDFs searchable
- Better for AI chat
- Required for scanned documents

#### 4. Merge Option

```
🔗 Merge all PDFs into a single document?
   Perfect for uploading to ChatGPT/Claude
> ○ No
  ○ Yes
```

**Choose Yes if:**
- Uploading to ChatGPT/Claude
- Want single document for analysis
- Preparing course materials

#### 5. Parallel Workers

```
⚡ How many parallel workers?
> 1 worker (sequential, safest)
  2 workers (2x faster)
  4 workers (4x faster, recommended)
  8 workers (maximum speed)
  Custom number
```

**Recommendations:**
- **1 worker:** Safe, slower, debugging
- **2 workers:** Good for smaller machines
- **4 workers:** Recommended for most cases
- **8+ workers:** High-end systems only

#### 6. Smart Caching

```
💾 Enable smart caching?
   Skip files that were already converted (saves time on re-runs)
> ● Yes
  ○ No
```

**Recommended:** Yes
- Skips already converted files
- Saves time on re-runs
- Based on file modification time

#### 7. Configuration Summary

```
📋 Configuration Summary:
  Source:     /path/to/documents
  Output:     /path/to/documents/converted_pdfs
  OCR:        Enabled
  Merge:      Yes
  Workers:    4
  Caching:    Enabled

🚀 Start conversion with these settings?
> ● Yes
  ○ No
```

Review your settings and confirm to start.

### AI Chat Mode

After conversion (especially with merge), you'll be prompted:

```
💬 Would you like to chat with your PDF using AI?
> ○ No
  ○ Yes
```

#### Provider Selection

```
🤖 Select AI provider:
> OpenAI (GPT-5, GPT-4.1, etc.)
  Google Gemini (2.5, 2.0, 1.5)
```

#### API Key Entry

```
🔑 OpenAI API Key:
   (Get it at: https://platform.openai.com/api-keys)
> ••••••••••••••••••••
```

Your key is hidden while typing (password field).

#### Model Selection

Models are grouped by series for easy selection:

**OpenAI:**
```
🎯 Select AI model:
  ═══ GPT-5 Series (Latest) ═══
> gpt-5
  gpt-5-mini
  gpt-5-nano
  ═══ GPT-4.1 Series ═══
  gpt-4.1
  gpt-4.1-mini
```

**Gemini:**
```
🎯 Select AI model:
  ═══ Gemini 2.5 (Latest) ═══
> gemini-2.5-flash
  gemini-2.5-pro
  ═══ Gemini 2.0 ═══
  gemini-2.0-flash-exp
```

#### Reasoning Effort (GPT-5 only)

```
🧠 Reasoning effort for gpt-5:
> minimal - Fastest (simple tasks)
  low - Quick reasoning
  medium - Balanced (recommended)
  high - Deep reasoning (complex tasks)
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **↑ ↓** | Navigate options |
| **Space** | Toggle selection (confirm/select) |
| **Enter** | Confirm choice |
| **Tab** | Autocomplete paths |
| **ESC** | Cancel/Go back |
| **Ctrl+C** | Abort completely |

## Fallback Mode

If `questionary` or `rich` are not installed, the script automatically shows:

```
⚠  Interactive mode requires additional packages.

Install interactive mode dependencies:
  pip install questionary rich

Or use traditional CLI mode:
  python3 document_to_pdf.py /path/to/documents
  python3 document_to_pdf.py --help
```

You can still use traditional CLI mode with flags:

```bash
python3 document_to_pdf.py /path/to/docs --merge -j 4
```

## Tips & Tricks

### Quick Start

```bash
# One-liner: activate venv and start interactive mode
source venv/bin/activate && python3 document_to_pdf.py
```

### Canceling Operations

- Press **Ctrl+C** during prompts to cancel
- You can always go back by selecting "No" on confirmation
- Script will show "Setup cancelled" if you abort

### File Validation

The interactive mode automatically:
- ✓ Validates folder existence
- ✓ Counts convertible files
- ✓ Warns if no files found
- ✓ Checks write permissions
- ✓ Validates worker count (1-32)

### Error Handling

If something goes wrong:
1. Clear, color-coded error messages
2. Suggestions for fixes
3. Graceful fallback to CLI mode
4. Never crashes without explanation

## Comparison: Interactive vs CLI

| Feature | Interactive Mode | CLI Mode |
|---------|-----------------|----------|
| **Ease of use** | ★★★★★ Visual prompts | ★★★☆☆ Flags required |
| **Validation** | ★★★★★ Real-time | ★★★☆☆ After execution |
| **Documentation** | ★★★★★ Built-in help | ★★☆☆☆ --help flag |
| **Speed** | ★★★☆☆ Interactive | ★★★★★ Direct |
| **Automation** | ★☆☆☆☆ Manual | ★★★★★ Scriptable |
| **Best for** | First-time users | Scripts & automation |

## Examples

### Example 1: Course Material Conversion

```bash
python3 document_to_pdf.py
# Select: ~/Courses/Biology101
# OCR: Yes
# Merge: Yes
# Workers: 4
# Result: Single merged PDF ready for AI analysis
```

### Example 2: Image Archive

```bash
python3 document_to_pdf.py
# Select: ~/Photos/Receipts
# OCR: Yes (for text recognition)
# Merge: No (keep separate)
# Workers: 8
# Result: Individual searchable PDFs
```

### Example 3: Office Documents

```bash
python3 document_to_pdf.py
# Select: ~/Documents/Work/Reports
# OCR: No (already text-based)
# Merge: No
# Workers: 2
# Result: Fast conversion without OCR
```

## Troubleshooting

### "questionary not found"

**Solution:**
```bash
pip install questionary rich
```

### "No convertible files found"

**Check:**
- Folder contains supported formats
- You have read permissions
- Files aren't hidden (starting with .)

### Interactive mode not starting

**Verify:**
```bash
python3 -c "import questionary; print('OK')"
```

If error, reinstall:
```bash
pip install --upgrade questionary rich
```

### Colors not showing

**Cause:** Piped output or unsupported terminal

**Fix:**
- Use a modern terminal (iTerm2, Windows Terminal, etc.)
- Check `TERM` environment variable
- Don't pipe output: `... | less` disables colors

## Advanced Configuration

### Custom Styling

The interactive mode uses a beautiful color scheme:
- 🟢 Green: Success, confirmations
- 🔵 Blue: Questions, headers
- 🟠 Orange: Answers, selections
- 🟣 Purple: Highlighted options
- ⚪ Grey: Instructions, separators

### Environment Variables

```bash
# Use specific Python installation
PYTHON=/usr/bin/python3.11 ./document_to_pdf.py

# API keys (for non-interactive AI chat)
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
```

## See Also

- [README.md](../README.md) - Main documentation
- [USAGE.md](USAGE.md) - CLI reference
- [FEATURES.md](FEATURES.md) - Complete feature list
- [PERFORMANCE.md](PERFORMANCE.md) - Optimization guide

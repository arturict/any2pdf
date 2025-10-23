# GitHub Copilot Instructions for any2pdf

## Project Overview
**any2pdf** is a universal document-to-PDF converter with integrated AI chat capabilities. It converts various file formats (Office, images, text) into searchable PDFs and enables users to chat with their documents using OpenAI GPT-5 or Google Gemini models.

## Core Architecture

### Main File: `document_to_pdf.py`
- **Single monolithic file** - All functionality in one Python file
- **~1300 lines** of well-structured code
- **No external modules** - Everything is self-contained

### Key Components

#### 1. Document Conversion Pipeline
- **Supported formats**: PPTX, DOCX, DOC, XLS, XLSX, ODT, ODP, ODS, RTF, JPG, PNG, GIF, BMP, TIFF, WEBP, SVG, HEIC, TXT, MD, CSV, JSON, XML, HTML, PDF
- **OCR Integration**: Tesseract for text recognition (German & English)
- **Multi-threading**: Parallel processing for 50-70% faster conversion
- **Smart caching**: Skip already converted files

#### 2. AI Chat Integration (`PDFChatSession` class)
```python
class PDFChatSession:
    """Handles AI chat sessions with PDF content"""
    
    # Supported providers
    OPENAI_MODELS = ["gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-4.1", ...]
    GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", ...]
    GPT5_REASONING_MODELS = ["gpt-5", "gpt-5-mini", "gpt-5-nano"]
    
    def __init__(self, pdf_path, provider, api_key, model, reasoning_effort=None):
        # reasoning_effort: "minimal", "low", "medium", "high" for GPT-5
```

**Key Features:**
- Dynamic model fetching from OpenAI/Gemini APIs
- GPT-5 reasoning effort control (minimal/low/medium/high)
- Model sorting by provider and series
- Conversation history management
- Streaming responses
- Beautiful CLI output with colors

#### 3. PDF Merging
- Merge multiple PDFs into single document
- Preserve metadata and searchability
- Optional feature via `--merge` flag

## Code Style & Conventions

### Functions
- Use descriptive names: `convert_document_to_pdf()`, `apply_ocr_to_pdf()`
- Include docstrings with type hints
- Handle errors gracefully with try/except blocks
- Log progress with colored output using `Colors` class

### Colors Class
```python
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
```

### Error Handling
- Always wrap external commands in try/except
- Provide helpful error messages
- Continue processing other files on individual failures

## Important Implementation Details

### 1. GPT-5 Reasoning Effort
```python
# Only for GPT-5 models
if provider == "openai" and model in GPT5_REASONING_MODELS:
    # Prompt user for reasoning effort
    # Options: minimal, low, medium (default), high
    # Pass to API as: reasoning_effort parameter
```

### 2. Model Fetching
```python
def fetch_openai_models(api_key: str) -> List[str]:
    """Fetch available models from OpenAI API"""
    # GET https://api.openai.com/v1/models
    # Sort by series: GPT-5 → GPT-4.1 → Others

def fetch_gemini_models(api_key: str) -> List[str]:
    """Fetch available models from Gemini API"""
    # GET https://generativelanguage.googleapis.com/v1beta/models
    # Sort by version: 2.5 → 2.0 → 1.5
```

### 3. Chat Session Flow
1. User completes PDF conversion
2. Prompt: "Would you like to chat with the PDF?"
3. Select provider (OpenAI/Gemini)
4. Enter API key
5. Fetch and display available models
6. If GPT-5: Select reasoning effort
7. Start interactive chat loop

### 4. API Integration
```python
# OpenAI
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": model,
        "messages": conversation_history,
        "reasoning_effort": reasoning_effort,  # GPT-5 only
        "stream": True
    }
)

# Gemini
response = requests.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    headers={"x-goog-api-key": api_key},
    json={
        "contents": [{"parts": [{"text": prompt}]}]
    }
)
```

## Dependencies

### System Requirements
- **LibreOffice**: Office document conversion
- **Tesseract OCR**: Text recognition
- **Poppler**: PDF utilities
- **ImageMagick**: Image processing

### Python Packages
```python
import PyPDF2         # PDF manipulation
import pytesseract    # OCR
import subprocess     # External commands
import requests       # API calls
import json          # API responses
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
```

## Testing Guidelines

### Test Conversion
```bash
# Create test files
mkdir -p test_files
echo "Test content" > test_files/test.txt

# Run conversion
python document_to_pdf.py test_files --merge
```

### Test AI Chat
```bash
# With OpenAI
python document_to_pdf.py test_files --merge
# Answer 'y' to chat prompt
# Select OpenAI, enter API key, choose gpt-5, select reasoning effort

# With Gemini
python document_to_pdf.py test_files --merge
# Answer 'y' to chat prompt
# Select Gemini, enter API key, choose gemini-2.5-flash
```

## Common Modification Patterns

### Adding New File Format
1. Add extension to `SUPPORTED_FORMATS` dict
2. Implement converter function: `convert_X_to_pdf(input_path, output_path)`
3. Add handler in main conversion logic
4. Update documentation

### Adding New AI Provider
1. Add models list: `NEW_PROVIDER_MODELS = [...]`
2. Implement `fetch_new_provider_models(api_key)`
3. Implement `send_new_provider_message(prompt, ...)`
4. Add to provider selection menu
5. Update `PDFChatSession` class

### Modifying Chat Behavior
- Edit `PDFChatSession.start_chat()` for main loop
- Edit `send_openai_message()` / `send_gemini_message()` for API calls
- Edit `display_chat_header()` for session info display

## Performance Optimization

### Current Optimizations
- Multi-threading for parallel file processing
- Smart caching to skip converted files
- Streaming API responses for faster UI
- Efficient PDF text extraction

### Best Practices
- Use `ThreadPoolExecutor` for I/O-bound tasks
- Cache API model lists (10-minute timeout)
- Stream large PDF content instead of loading all at once
- Use subprocess timeouts to prevent hangs

## Security Considerations

### API Keys
- Never hardcode API keys
- Prompt user for keys at runtime
- Don't log API keys
- Consider environment variables for automation

### File Processing
- Validate file paths before processing
- Use proper temp file handling
- Clean up intermediate files
- Handle large files gracefully

## Windows Support via WSL

**Important**: Windows users MUST use WSL (Windows Subsystem for Linux)
- System dependencies not available natively on Windows
- LibreOffice, Tesseract work best in Linux environment
- See `WSL_SETUP.md` for installation guide

## Command-Line Interface

```bash
python document_to_pdf.py INPUT_DIR [OPTIONS]

Arguments:
  INPUT_DIR              Directory containing files to convert

Options:
  -o, --output DIR       Output directory (default: INPUT_DIR/output)
  --merge               Merge all PDFs into single file
  --no-ocr              Skip OCR step (faster but not searchable)
  --no-cache            Force re-conversion of all files
  -j, --jobs N          Number of parallel jobs (default: CPU count)
  -h, --help            Show help message
```

## Project Files Structure

```
any2pdf/
├── document_to_pdf.py          # Main application (all code)
├── requirements.txt            # Python dependencies
├── setup.sh                   # Quick setup script
├── README.md                  # Main documentation
├── FEATURES.md                # Feature documentation
├── USAGE.md                   # Usage examples
├── WSL_SETUP.md              # Windows setup guide
├── CHANGELOG.md              # Version history
├── .github/
│   └── copilot-instructions.md  # This file
└── test_files/                # Test documents
```

## Quick Reference for Common Tasks

### Run basic conversion
```bash
python document_to_pdf.py ./documents
```

### Run with merge and chat
```bash
python document_to_pdf.py ./documents --merge
# Answer 'y' when prompted for chat
```

### Debug mode (verbose output)
- Check subprocess return codes
- Print API response status codes
- Log conversion progress per file

### Add new reasoning effort level
1. Update `GPT5_REASONING_MODELS` if needed
2. Add to effort_map in chat prompt
3. Update display text
4. No API changes needed (OpenAI handles all values)

## Latest Updates (v1.2.0)

- ✅ GPT-5 reasoning effort control (minimal/low/medium/high)
- ✅ Model sorting by provider and series
- ✅ Latest models: GPT-5, GPT-4.1, Gemini 2.5
- ✅ Dynamic model fetching from APIs
- ✅ Improved chat UI with colored output

## Version Compatibility

- **Python**: 3.8+
- **OpenAI API**: Latest (GPT-5 support)
- **Gemini API**: v1beta (Gemini 2.5 support)
- **Dependencies**: See requirements.txt

## Contributing Guidelines

1. Keep everything in single file (document_to_pdf.py)
2. Maintain color-coded CLI output
3. Add comprehensive error handling
4. Update documentation for new features
5. Test with multiple file formats
6. Ensure Windows/WSL compatibility

---

**Remember**: This is a single-file application. Keep it simple, maintainable, and well-documented!

# GitHub Copilot Instructions for any2pdf

## Project Overview

**any2pdf** is a Python-based document converter that transforms various file formats into searchable PDFs, optimized for AI tools like ChatGPT. It includes integrated AI chat functionality using OpenAI (GPT-5 series) and Google Gemini models.

## Key Components

### Main Script: `document_to_pdf.py`

**Core Functionality:**
- Multi-format conversion: Office documents (PPTX, DOCX, XLSX), images (JPG, PNG, SVG, HEIC), text files (TXT, MD, JSON, XML, HTML), and PDFs
- OCR integration using Tesseract for searchable text
- PDF merging capability for creating single documents
- AI chat integration with streaming responses
- Multi-threading support for parallel processing
- Smart caching system to avoid redundant conversions

**Architecture:**
- `DocumentConverter` class: Handles all conversion logic
- `PDFChatSession` class: Manages AI chat interactions
- Uses LibreOffice for office document conversion
- Uses ImageMagick for image processing
- Uses Tesseract OCR for text recognition
- Uses PyMuPDF (fitz) for PDF manipulation

## Dependencies

**System Requirements:**
- LibreOffice (for office documents)
- Tesseract OCR (for text recognition)
- Poppler utils (for PDF processing)
- ImageMagick (for image conversion)

**Python Packages:**
- `PyMuPDF (fitz)` - PDF manipulation
- `Pillow (PIL)` - Image processing
- `pytesseract` - OCR wrapper
- `pdf2image` - PDF to image conversion
- `openai` - OpenAI API client (optional)
- `google-generativeai` - Gemini API client (optional)

## AI Integration Details

### Supported Providers

**OpenAI:**
- GPT-5 series: `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5-chat-latest`
- GPT-4.1 series: `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`
- Legacy: `o4-mini`, `o3`, `gpt-4o`

**Reasoning Effort Levels (GPT-5):**
- `minimal` - Fastest, minimal thinking
- `low` - Quick reasoning
- `medium` - Balanced (default)
- `high` - Deep reasoning for complex tasks

**Google Gemini:**
- Gemini 2.5: `gemini-2.5-flash`, `gemini-2.5-pro`
- Gemini 2.0: `gemini-2.0-flash-exp`, `gemini-2.0-flash-thinking-exp`
- Gemini 1.5: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-1.5-flash-8b`

### Chat Implementation

The `PDFChatSession` class handles:
- Dynamic model fetching from provider APIs
- Conversation history management
- Streaming responses for better UX
- Model sorting and grouping by series
- Reasoning effort selection for GPT-5
- Color-coded CLI output

## Code Style Guidelines

- Use type hints for function parameters and returns
- Follow PEP 8 conventions
- Use ANSI color codes via the `Colors` class for terminal output
- Implement error handling with try-except blocks
- Use context managers for file operations
- Add docstrings for classes and complex functions
- Keep functions focused and modular

## Performance Optimizations

- **Parallel Processing**: Use `-j` flag with `ThreadPoolExecutor` for concurrent conversions
- **Smart Caching**: SHA-256 hash-based caching in `.cache/` directory
- **Memory Management**: Stream large files, avoid loading everything into memory
- **OCR Detection**: Check if PDF already has text before applying OCR

## File Structure

```
any2pdf/
├── document_to_pdf.py          # Main converter script
├── flatten_files.py            # Helper for flattening directories
├── examples.py                 # Usage examples
├── test_converter.py           # Dependency checker
├── requirements.txt            # Python dependencies
├── CHANGELOG.md                # Version history
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── docs/                       # Extended documentation
│   ├── USAGE.md
│   ├── PERFORMANCE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── WSL_SETUP.md
│   ├── CONTRIBUTING.md
│   ├── FEATURES.md
│   └── QUICKSTART.md
└── .github/
    └── copilot-instructions.md # This file
```

## Common Patterns

### Adding New File Format Support

1. Add extension to the appropriate format list
2. Create conversion method following pattern: `convert_<format>_to_pdf()`
3. Update documentation in README.md
4. Test with sample files

### Adding New AI Provider

1. Import provider library (make it optional)
2. Add to `PDFChatSession.fetch_available_models()`
3. Implement provider-specific chat logic
4. Add model selection UI
5. Update documentation

### Error Handling

Always use try-except for:
- File operations
- External process calls (LibreOffice, Tesseract)
- API calls
- PDF operations

Continue processing other files if one fails (don't crash the entire batch).

## Platform Support

**Primary**: Ubuntu/Debian Linux
**Secondary**: macOS (with Homebrew)
**Windows**: WSL (Windows Subsystem for Linux) required

Always document Windows-specific instructions with WSL guidance.

## CLI Output Best Practices

- Use color coding consistently:
  - `Colors.GREEN` for success
  - `Colors.YELLOW` for warnings
  - `Colors.RED` for errors
  - `Colors.CYAN` for info
  - `Colors.BLUE` for headers
- Use emojis for visual clarity (📄, ✓, ⚡, 🤖, etc.)
- Show progress indicators for long operations
- Provide clear error messages with suggested fixes
- Use separators (═══) for section breaks

## API Key Management

- Never hardcode API keys
- Prompt users for keys at runtime
- Support environment variables: `OPENAI_API_KEY`, `GEMINI_API_KEY`
- Validate keys before using
- Handle API errors gracefully

## Important Notes for AI Assistants

1. **Windows Users**: Always remind to use WSL, don't suggest native Windows commands
2. **Virtual Environment**: Always recommend using venv for Python packages
3. **Dependencies**: Check system dependencies before suggesting Python-only solutions
4. **OCR**: OCR is optional but highly recommended for best results
5. **API Keys**: Remind users to get API keys from official sources
6. **Performance**: Suggest `-j` flag for large batches
7. **Caching**: Explain that `.cache/` directory speeds up repeated conversions
8. **Reasoning Effort**: Help users choose appropriate level based on their use case

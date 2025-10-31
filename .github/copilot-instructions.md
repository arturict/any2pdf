# GitHub Copilot Instructions for any2pdf

## Project Overview

**any2pdf** is a universal document-to-PDF converter with OCR support and AI chat integration. It converts office documents, images, text files, and PDFs into searchable PDFs optimized for AI tools like ChatGPT and Claude. Features interactive CLI with questionary prompts and fallback to traditional argparse mode.

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
- `questionary` - Interactive CLI prompts (optional)
- `rich` - Terminal UI enhancement (optional)

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

## CLI Modes

### Interactive Mode (Default - No Arguments)

Uses `questionary` for beautiful prompts:
- Directory browser for source/output folders
- Confirm prompts for OCR/merge/caching options
- Select lists for workers and AI models
- Password input for API keys
- Grouped model selection by series

Example:
```bash
python document_to_pdf.py
# Interactive prompts guide through all options
```

### Traditional CLI Mode

Falls back to argparse when arguments provided:
```bash
python document_to_pdf.py /path/to/docs --merge -j 4
```

## File Structure

```
any2pdf/
├── document_to_pdf.py          # Main converter + AI chat
├── flatten_files.py            # Helper for flattening directories
├── requirements.txt            # Python dependencies
├── setup.sh                    # System dependencies installer
├── CHANGELOG.md                # Version history
├── README.md                   # Main documentation (German)
├── LICENSE                     # MIT License
├── docs/                       # Extended documentation
│   ├── USAGE.md
│   ├── PERFORMANCE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── FEATURES.md
│   └── RELEASE_NOTES_*.md
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
- Use emojis for visual clarity (📄, ✓, ⚡, 🤖, 💬, 🔑, etc.)
- Show progress indicators for long operations
- Provide clear error messages with suggested fixes
- Use separators (═══) for section breaks
- For interactive mode, use questionary's built-in styling

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

## Testing Guidelines

### Running Tests

**Unit Tests:**
```bash
# Run the basic test suite
python3 test_converter.py
```

**Integration Tests:**
```bash
# Run full integration test suite with examples
bash test_examples.sh
```

**Test Structure:**
- `test_converter.py` - Unit tests for DocumentConverter class
- `test_examples.sh` - Integration tests with sample files
- `test_examples/` - Directory with test output (auto-created)
- `test_files/` - Sample files for testing

**Writing Tests:**
- Test each conversion format independently
- Include tests for error handling
- Test with and without OCR
- Test parallel processing with different worker counts
- Mock external dependencies (LibreOffice, Tesseract) when appropriate
- Verify cache behavior

### Test Dependencies

Before running tests, ensure all dependencies are installed:
```bash
# Quick dependency check
python3 test_converter.py  # Will report missing dependencies

# Install missing dependencies
bash setup.sh  # For Ubuntu/Debian
```

## Build and Linting

### Code Quality

**Python Style:**
- Follow PEP 8 conventions
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use docstrings for all public classes and functions

**Linting (recommended but not required):**
```bash
# Install linting tools (optional)
pip install pylint black flake8 mypy

# Run linters
pylint document_to_pdf.py
black --check document_to_pdf.py
flake8 document_to_pdf.py --max-line-length=100
mypy document_to_pdf.py
```

**Code Formatting:**
```bash
# Auto-format code (if black is installed)
black document_to_pdf.py flatten_files.py test_converter.py
```

### Pre-commit Checks

Before committing code:
1. Run tests: `python3 test_converter.py`
2. Check for syntax errors: `python3 -m py_compile document_to_pdf.py`
3. Test basic functionality: `python3 document_to_pdf.py --help`
4. Verify documentation is updated if adding features

## Repository Commands

### Setup and Installation

```bash
# Initial setup (Ubuntu/Debian)
bash setup.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Verify installation
python3 test_converter.py
```

### Development Workflow

```bash
# Activate virtual environment
source venv/bin/activate

# Run converter in development
python3 document_to_pdf.py ./test_files --merge -j 4

# Test changes
python3 test_converter.py
bash test_examples.sh

# Check dependencies
python3 -c "from document_to_pdf import DocumentConverter; import sys; converter = DocumentConverter(sys.path[0]); converter.print_dependencies()"
```

### Common Commands

```bash
# Convert with all features
python3 document_to_pdf.py /path/to/docs --merge -j 4

# Quick test without OCR
python3 document_to_pdf.py ./test_examples --no-ocr

# Test AI chat integration (requires API key)
python3 document_to_pdf.py ./test_examples --merge
# Then answer 'y' when prompted for chat

# Flatten directory structure (helper utility)
python3 flatten_files.py /path/to/nested/folders
```

## Contribution Workflow

### Making Changes

1. **Understand the Change:**
   - Read existing code and documentation
   - Identify affected components
   - Check if system dependencies are needed

2. **Implement Changes:**
   - Make minimal, focused changes
   - Follow existing code style
   - Update type hints
   - Add appropriate error handling

3. **Test Your Changes:**
   - Run unit tests: `python3 test_converter.py`
   - Run integration tests: `bash test_examples.sh`
   - Test manually with sample files
   - Test error cases

4. **Update Documentation:**
   - Update README.md if adding features
   - Update CHANGELOG.md
   - Add inline comments for complex logic
   - Update this file if workflow changes

5. **Commit Guidelines:**
   - Use clear, descriptive commit messages
   - Reference issue numbers if applicable
   - Keep commits focused and atomic

### Adding New Features

**Adding a New File Format:**
1. Add extension to appropriate format list (OFFICE_FORMATS, IMAGE_FORMATS, etc.)
2. Implement `convert_<format>_to_pdf()` method
3. Add error handling for missing dependencies
4. Test with sample files
5. Update README.md and docs/FEATURES.md

**Adding a New AI Provider:**
1. Add optional import at top of file
2. Implement in `PDFChatSession.fetch_available_models()`
3. Add provider-specific chat logic in `PDFChatSession.chat_with_pdf()`
4. Update model selection UI
5. Update README.md with provider documentation
6. Test with API key

## Debugging and Troubleshooting

### Common Issues

**LibreOffice Not Found:**
```bash
# Check if installed
which libreoffice
# Install if missing
sudo apt-get install libreoffice
```

**Tesseract OCR Issues:**
```bash
# Verify Tesseract installation
tesseract --version
# Check language data
tesseract --list-langs
# Install if missing
sudo apt-get install tesseract-ocr tesseract-ocr-deu
```

**Python Import Errors:**
```bash
# Activate virtual environment first
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

**Permission Errors:**
```bash
# Don't run with sudo
# Instead, fix permissions on output directory
chmod 755 /path/to/output
```

### Debugging Tips

1. **Enable Verbose Output:**
   - The converter already prints detailed status messages
   - Check for error messages in red
   - Look for warnings in yellow

2. **Test Individual Files:**
   ```bash
   # Create test directory with single file
   mkdir test_single
   cp problematic_file.pptx test_single/
   python3 document_to_pdf.py test_single
   ```

3. **Check Dependencies:**
   ```bash
   python3 test_converter.py
   # This will show which dependencies are missing
   ```

4. **Cache Issues:**
   ```bash
   # Clear cache if getting stale results
   rm -rf .cache/
   ```

5. **LibreOffice Process Issues:**
   ```bash
   # Kill stuck LibreOffice processes
   pkill -f soffice
   ```

## Security Best Practices

### API Key Management

- **Never commit API keys** to version control
- Use environment variables for keys: `OPENAI_API_KEY`, `GEMINI_API_KEY`
- Keys are requested at runtime if not in environment
- Don't log or print API keys in error messages

### File Handling

- Validate file extensions before processing
- Use subprocess with proper escaping for external commands
- Don't execute arbitrary code from input files
- Limit file sizes to prevent resource exhaustion
- Clean up temporary files after processing

### External Dependencies

- Pin dependency versions in requirements.txt
- Regularly update dependencies for security patches
- Validate external tool outputs before using
- Use subprocess with `shell=False` when possible
- Sanitize file paths to prevent directory traversal

### User Input Validation

- Validate all command-line arguments
- Check for malicious file paths (`../`, etc.)
- Limit parallel workers to reasonable values
- Validate model names before API calls

## Performance Considerations

### Optimization Checklist

When making changes that affect performance:
- [ ] Test with `-j` flag for parallel processing
- [ ] Verify caching works correctly
- [ ] Check memory usage with large files
- [ ] Test with batch of 10+ documents
- [ ] Profile if making algorithmic changes
- [ ] Document performance characteristics in code

### Benchmarking

```bash
# Time a conversion
time python3 document_to_pdf.py ./large_batch --merge -j 4

# Compare with/without parallel processing
time python3 document_to_pdf.py ./test_batch --merge -j 1
time python3 document_to_pdf.py ./test_batch --merge -j 4

# Test caching (should be much faster on second run)
time python3 document_to_pdf.py ./test_batch --merge
time python3 document_to_pdf.py ./test_batch --merge  # Should use cache
```

## Documentation Structure

- `README.md` - Main documentation (German) with quickstart
- `docs/USAGE.md` - Detailed usage instructions
- `docs/FEATURES.md` - Feature documentation
- `docs/PERFORMANCE.md` - Performance benchmarks and tips
- `docs/PROJECT_STRUCTURE.md` - Code organization
- `CHANGELOG.md` - Version history
- `.github/copilot-instructions.md` - This file (for AI assistants)

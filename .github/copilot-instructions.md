# GitHub Copilot Instructions for any2pdf

## Project Overview
**any2pdf** is a universal document-to-PDF conversion tool with AI-powered chat capabilities. It converts various file formats (images, DOCX, PPTX, etc.) into a single searchable PDF and enables interactive conversations about the content using OpenAI GPT-5 or Google Gemini.

## Tech Stack
- **Runtime**: Bun (TypeScript/JavaScript runtime)
- **Language**: TypeScript
- **Key Dependencies**:
  - `pdf-lib`: PDF manipulation
  - `sharp`: Image processing  
  - `mammoth`: DOCX conversion
  - `pptx2json`: PowerPoint parsing
  - `openai`: GPT API integration
  - `@google/generative-ai`: Gemini API integration
  - `chalk`: Terminal styling
  - `ora`: Loading spinners

## Project Structure
```
any2pdf/
├── src/
│   ├── index.ts              # CLI entry point
│   ├── converter.ts          # Core conversion logic
│   ├── chat.ts              # AI chat integration
│   └── utils.ts             # Utility functions
├── test_files/              # Test files for development
├── docs/                    # Documentation
├── README.md               # Main documentation
├── QUICKSTART.md          # Quick start guide
├── WSL_SETUP.md          # Windows/WSL setup
├── FEATURES.md           # Feature list
├── CONTRIBUTING.md       # Contribution guide
└── CHANGELOG.md         # Version history
```

## Key Features
1. **Multi-format support**: Images (JPG, PNG, GIF, BMP, TIFF, WebP), DOCX, PPTX, PDF
2. **OCR support**: Optional Tesseract integration for text recognition
3. **Recursive directory scanning**: Processes all files in subdirectories
4. **AI Chat**: Interactive chat with document content using GPT-5 or Gemini 2.0/2.5
5. **Performance optimized**: Parallel processing, caching, streaming

## AI Integration Details

### Supported Providers
- **OpenAI**: gpt-5, gpt-5-mini, gpt-5-nano (with configurable reasoning effort)
- **Google Gemini**: gemini-2.0-flash-exp, gemini-2.5-flash, gemini-2.5-pro

### Reasoning Effort (GPT-5 only)
- `minimal`: Fastest, lowest latency
- `low`: Fast responses
- `medium`: Default balanced approach
- `high`: Deep reasoning for complex queries

### Chat Implementation
- Uses streaming responses for real-time interaction
- Maintains conversation context
- Base64-encodes PDF content for API transmission
- Provider-specific API handling in `src/chat.ts`

## Development Guidelines

### Code Style
- Use TypeScript with strict type checking
- Async/await for asynchronous operations
- Clear error handling with descriptive messages
- Colorful CLI output using chalk
- Progress indicators with ora

### Performance Considerations
- Use parallel processing for multiple files
- Implement caching where applicable
- Stream responses for better UX
- Optimize image processing with sharp

### Error Handling
- Catch and log errors with context
- Provide user-friendly error messages
- Continue processing other files on single file failure
- Validate API keys before starting chat

### Testing
- Test files located in `test_files/`
- Run with: `bun run src/index.ts test_files output.pdf`
- Test chat feature after conversion

## Common Tasks

### Adding New File Format Support
1. Update `SUPPORTED_EXTENSIONS` in `converter.ts`
2. Add conversion logic in `convertFileToPdf()`
3. Handle format-specific edge cases
4. Update documentation

### Modifying AI Provider
1. Edit `src/chat.ts`
2. Update model lists and API endpoints
3. Handle provider-specific response formats
4. Test streaming and error handling

### CLI Improvements
1. Modify `src/index.ts` for CLI logic
2. Use chalk for consistent coloring
3. Add ora spinners for long operations
4. Update help text

## Platform-Specific Notes

### Windows Users
- Must use WSL (Windows Subsystem for Linux)
- See `WSL_SETUP.md` for setup instructions
- Native Windows support not available due to dependency requirements

### Linux/macOS
- Direct execution supported
- Tesseract OCR optional but recommended
- Install with package manager

## Important Commands
```bash
# Install dependencies
bun install

# Run conversion
bun run src/index.ts <input_folder> <output.pdf>

# Development
bun run src/index.ts test_files output.pdf

# Test with chat
# Follow prompts after PDF generation
```

## File Conversion Flow
1. Scan directory recursively for supported files
2. Sort files alphabetically
3. Convert each file to PDF pages:
   - Images: Convert using sharp, optional OCR
   - DOCX: Extract text and convert to PDF
   - PPTX: Extract slides as images/text
   - PDF: Copy pages directly
4. Merge all PDFs into single output
5. Optionally start AI chat session

## API Key Management
- Environment variables: `OPENAI_API_KEY`, `GOOGLE_API_KEY`
- Interactive prompts if not set
- Secure handling, never logged
- Validation before use

## Dependencies to Watch
- `pdf-lib`: Core PDF manipulation
- `sharp`: Image processing (requires native binaries)
- `tesseract.js`: OCR (optional, large dependency)
- Provider SDKs: Keep updated for latest models

## Testing Strategy
- Manual testing with diverse file types
- Test edge cases (empty files, corrupted files)
- Verify AI chat with different providers
- Check performance with large document sets

## Security Considerations
- API keys stored securely
- No sensitive data logged
- Input validation for file paths
- Safe PDF content encoding for AI APIs

## Future Enhancement Ideas
- Batch processing improvements
- Custom OCR language support
- More AI providers (Anthropic, etc.)
- Web UI option
- Progress persistence/resume
- Output format options

## Troubleshooting Common Issues
1. **PDF creation fails**: Check write permissions
2. **OCR not working**: Install Tesseract
3. **API errors**: Verify API keys and quotas
4. **WSL issues**: See WSL_SETUP.md
5. **Memory issues**: Process files in smaller batches

## Key Principles
- **User Experience First**: Clear messages, progress indicators
- **Performance Matters**: Optimize where possible
- **Flexibility**: Support multiple formats and providers
- **Error Resilience**: Gracefully handle failures
- **Documentation**: Keep docs updated with code changes

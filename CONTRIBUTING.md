# Contributing to any2pdf

First off, thank you for considering contributing to any2pdf! 🎉

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples
- Describe the behavior you observed and what you expected
- Include screenshots if applicable
- Note your environment (OS, Python version, etc.)

### ✨ Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- List any alternative solutions you've considered

### 🔧 Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message
6. Open a Pull Request!

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/any2pdf.git
cd any2pdf

# Install dependencies
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Run tests
python test_converter.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Update documentation for new features

## Testing

Before submitting a PR, test your changes:

```bash
# Test with sample files
python document_to_pdf.py ./test_files --merge

# Run the test suite
python test_converter.py
```

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally

Examples:
```
Add support for EPUB format
Fix OCR memory leak issue #123
Update documentation for merge feature
```

## Questions?

Feel free to open an issue with the question label!

---

Thank you for contributing! ❤️

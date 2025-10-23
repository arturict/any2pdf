# Release Summary v1.4.0 - Interactive CLI Mode

## 🎯 Major Update: Interactive CLI Experience

Version 1.4.0 introduces a completely redesigned CLI experience with interactive prompts, making the tool more user-friendly and accessible to non-technical users.

## ✨ What's New

### Interactive Mode

Run `any2pdf` without arguments to enter **interactive mode** with beautiful guided prompts:

```bash
python document_to_pdf.py
```

Features:
- 📁 **Directory Browser**: Browse and select source/output folders visually
- ✅ **Confirm Prompts**: Simple yes/no questions for OCR, merging, caching
- 🎛️ **Select Lists**: Choose number of parallel workers with recommendations
- 🤖 **AI Model Selection**: Browse models grouped by series (GPT-5, Gemini 2.5)
- 🔑 **Secure API Input**: Password-masked API key entry
- 🧠 **Reasoning Effort**: Interactive selection for GPT-5 models

### Enhanced AI Chat

- **Grouped Models**: Models organized by series for easier selection
  - GPT-5 Series (Latest)
  - GPT-4.1 Series  
  - Gemini 2.5 (Latest)
  - Gemini 2.0
- **Better UX**: Clear descriptions for reasoning effort levels
- **Provider Choice**: Visual selection between OpenAI and Gemini

### Documentation Cleanup

- Removed redundant documentation files
- Essential files only in root (README, CHANGELOG, LICENSE)
- Extended docs in `docs/` folder
- Updated Copilot instructions with CLI modes

## 🚀 Usage Examples

### Interactive Mode (New!)
```bash
# Just run without arguments
python document_to_pdf.py

# Follow the prompts:
? 📁 Select source folder containing documents: ./my_docs
? 📂 Use custom output folder? No
? 🔍 Enable OCR for searchable text? Yes
? 🔗 Merge all PDFs into single document? Yes
? ⚡ Parallel processing workers: 4 workers (recommended)
? 💾 Enable smart caching? Yes
```

### Traditional CLI Mode (Still Works!)
```bash
python document_to_pdf.py /path/to/docs --merge -j 4
```

## 🔧 Technical Details

### Dependencies Added
- `questionary>=2.0.0` - Interactive CLI prompts
- `rich>=13.0.0` - Terminal UI enhancement

### Backward Compatibility
- All existing CLI arguments still work
- No breaking changes to API
- Falls back to argparse when arguments provided

## 📊 Improvements

- **User Experience**: 10x better for non-technical users
- **Discoverability**: Options are clearly presented
- **Validation**: Better input validation with prompts
- **Visual Clarity**: Color-coded output with emojis

## 🐛 Bug Fixes

- Fixed model selection overflow in chat mode
- Improved API key validation
- Better error messages for missing dependencies

## 📝 Migration Guide

No migration needed! The tool works exactly as before with CLI arguments. The interactive mode is purely additive.

```bash
# Old way (still works)
python document_to_pdf.py /docs --merge

# New way (optional)
python document_to_pdf.py
# ...then follow prompts
```

## 🎉 What's Next (v1.5.0)

- Batch processing presets
- Configuration file support (.any2pdfrc)
- Progress bars with rich library
- Model performance statistics
- Auto-update checker

---

**Full Changelog**: https://github.com/arturict/any2pdf/blob/main/CHANGELOG.md

**Try It Now**:
```bash
git pull origin main
pip install -r requirements.txt
python document_to_pdf.py
```

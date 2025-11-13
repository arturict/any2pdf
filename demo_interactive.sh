#!/bin/bash
# Demo script for interactive mode

echo "=================================================="
echo "  any2pdf Interactive Mode Demo"
echo "=================================================="
echo ""

# Check if in venv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment active: $VIRTUAL_ENV"
else
    echo "⚠  Virtual environment not active"
    echo ""
    echo "Activate with:"
    echo "  source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Check questionary
python3 -c "import questionary" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ questionary installed"
else
    echo "✗ questionary not installed"
    echo ""
    echo "Install with:"
    echo "  pip install questionary rich"
    exit 1
fi

echo ""
echo "=================================================="
echo "  Starting Interactive Mode..."
echo "=================================================="
echo ""
echo "Note: Use Ctrl+C to cancel at any time"
echo ""
sleep 2

# Run interactive mode
python3 document_to_pdf.py

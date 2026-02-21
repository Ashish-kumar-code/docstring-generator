#!/bin/bash
# Setup script for Python Docstring Generator

set -e

echo "📚 Python Docstring Generator - Setup Script"
echo "=============================================="
echo ""

# Check Python version
echo "🐍 Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

if ! python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Python 3.11+ is required"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Install package in development mode
echo ""
echo "📦 Installing docstring_generator in development mode..."
pip install -e .
echo "✓ Development installation complete"

# Setup pre-commit hook
echo ""
echo "🔧 Setting up pre-commit hook..."

if [ -d ".git" ]; then
    HOOKS_DIR=".git/hooks"
    HOOK_FILE="$HOOKS_DIR/pre-commit"
    
    mkdir -p "$HOOKS_DIR"
    
    if [ -f "config/pre-commit" ]; then
        cp config/pre-commit "$HOOK_FILE"
        chmod +x "$HOOK_FILE"
        echo "✓ Pre-commit hook installed"
    else
        echo "⚠️  config/pre-commit not found, skipping pre-commit setup"
    fi
else
    echo "⚠️  Not a git repository, skipping pre-commit hook setup"
fi

# Run tests
echo ""
echo "🧪 Running tests..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short || echo "⚠️  Some tests failed"
else
    echo "⚠️  pytest not found, skipping tests"
fi

# Summary
echo ""
echo "=============================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Streamlit dashboard:"
echo "   streamlit run app.py"
echo ""
echo "2. Or use the CLI:"
echo "   python -m docstring_generator.cli analyze examples/sample_python_file.py"
echo ""
echo "3. Generate docstrings for a file:"
echo "   python -m docstring_generator.cli generate examples/sample_python_file.py -o examples/enhanced.py"
echo ""
echo "4. Run all commands:"
echo "   python -m docstring_generator.cli --help"
echo ""
echo "Happy coding! 🚀"

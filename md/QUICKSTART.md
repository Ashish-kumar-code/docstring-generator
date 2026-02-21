# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.11 or higher
- pip or conda

### Option 1: Windows (Quick Setup)

```batch
# 1. Navigate to project directory
cd docstring-generator

# 2. Run setup script
setup.bat

# 3. Start Streamlit dashboard
streamlit run app.py
```

Open http://localhost:8501 in your browser!

---

### Option 2: Linux/macOS (Quick Setup)

```bash
# 1. Navigate to project directory
cd docstring-generator

# 2. Run setup script
bash setup.sh

# 3. Start Streamlit dashboard
streamlit run app.py
```

Open http://localhost:8501 in your browser!

---

### Option 3: Manual Setup (Any OS)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install in development mode
pip install -e .

# 3. Choose one:

# Option A: Streamlit Dashboard
streamlit run app.py

# Option B: Command-line
python -m docstring_generator.cli analyze examples/sample_python_file.py

# Option C: Python API
python -c "from docstring_generator import parse_file; print(parse_file('examples/sample_python_file.py'))"
```

---

## 📘 Dashboard Workflow

1. **Upload File** (or scan directory)
2. **Analyze** to see functions/classes
3. **Generate** docstrings automatically
4. **Validate** for PEP 257 compliance
5. **Review** side-by-side comparison
6. **Export** in Python/Markdown/JSON

---

## 💻 CLI Quick Reference

```bash
# Analyze a file
docstring-gen analyze path/to/file.py

# Generate docstrings
docstring-gen generate path/to/file.py --style google -o enhanced.py

# Validate docstrings
docstring-gen validate path/to/file.py

# Check code issues
docstring-gen check path/to/file.py

# Batch process directory
docstring-gen batch src/ --recursive --style numpy
```

---

## 🧪 Test the Example

```bash
# Generate docstrings for example file
python -m docstring_generator.cli generate examples/sample_python_file.py \
    --style google \
    -o examples/sample_enhanced.py

# Validate the generated docstrings
python -m docstring_generator.cli validate examples/sample_enhanced.py

# Check for code issues
python -m docstring_generator.cli check examples/sample_python_file.py
```

---

## 🎯 What You Can Do

✅ **Parse Python Files**
- Extract functions, classes, parameters
- Detect type hints and decorators
- Analyze code structure

✅ **Generate Docstrings**
- Google, NumPy, or reStructuredText styles
- Automatic summary generation
- Quality scoring

✅ **Validate Code**
- PEP 257 compliance checks
- Code issue detection
- Quality metrics

✅ **Create Documentation**
- Side-by-side diff views
- Export to multiple formats
- Track code changes

---

## 📚 Learn More

- **README.md** - Full documentation
- **docs/ARCHITECTURE.md** - System design
- **docs/USAGE_GUIDE.md** - Detailed usage examples
- **examples/** - Example Python files
- **tests/** - Test suite

---

## 🆘 Troubleshooting

**Issue**: Streamlit not found
```bash
pip install streamlit
```

**Issue**: Python version error
```bash
python --version  # Must be 3.11+
```

**Issue**: Module not found
```bash
pip install -e .
```

**Issue**: Permission denied (Linux/macOS)
```bash
chmod +x setup.sh
bash setup.sh
```

---

## 🎓 Next Steps

1. **Explore the Dashboard**: `streamlit run app.py`
2. **Try CLI Commands**: `docstring-gen --help`
3. **Read USAGE_GUIDE.md**: Full API documentation
4. **Check ARCHITECTURE.md**: How it all works
5. **Review Examples**: See generated docstrings

---

**Questions?** Check the documentation or examples directory!

Happy coding! 🚀

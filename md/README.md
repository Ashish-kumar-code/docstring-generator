# 📚 Python Docstring Generator

An automated Python docstring generator with AST parsing, multiple style support (Google, NumPy, reStructuredText), validation, quality metrics, and a modern Streamlit dashboard with before/after analysis.

**Key Features:**
- 🔍 AST-based parsing to extract functions, classes, parameters, type hints, decorators
- ✨ Template-driven docstring generation in Google, NumPy, and reST styles
- 🎯 **Selective Generation** - Review and accept only the docstrings you want
- 📊 **Before/After Quality Analysis** - See exactly how much your code quality improves
- ✅ PEP 257 compliance validation with quality scoring (0-100 scale)
- 🐛 Code issue detection (syntax errors, missing type hints, unused imports)
- 💬 Inline comment generation for complex code constructs
- 📊 Streamlit dashboard with 7 interactive pages (Home, Analyze, Generate, Compare, Metrics, Validate, Export)
- 🖇️ Side-by-side diff viewer with statistics
- 📤 **Multi-format Export** - Python, Markdown, JSON, CSV, and HTML reports with preview
- 📈 **Metrics & Coverage Analysis** - Quality scores, docstring coverage, per-function analysis
- 🔌 CLI tool for batch processing
- 📝 Pre-commit hooks and CI/CD integration

## Installation

### Requirements
- Python 3.11+
- pip or poetry

### Setup

1. **Clone or download the project**
   ```bash
   cd docstring-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Install in development mode**
   ```bash
   pip install -e .
   ```

## Quick Start

### Option 1: Streamlit Dashboard (Recommended)

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser. The app features 7 interactive pages:

1. **🏠 Home** - Overview of features, quick start guide, and style showcase
2. **📂 Analyze** - Upload Python files, view code statistics (LOC, functions, classes)
3. **✨ Generate** - Choose docstring style, generate, and **selectively review & accept** docstrings
4. **👀 Compare** - Side-by-side comparison of original vs enhanced code with unified diff
5. **📊 Metrics** - Quality analysis and per-function documentation coverage table
6. **✅ Validate** - Check docstring quality and detect code issues
7. **📥 Export** - Download enhanced code and generate reports in multiple formats

**Selective Generation Workflow:**
1. Upload a Python file → Analyze structure
2. Select docstring style (Google/NumPy/reST)
3. Generate docstrings (calculates quality metrics BEFORE)
4. **Review & Select** - Checkboxes for each function/class docstring with preview expanders
5. **Apply Selected** - Only applies the docstrings you checked
6. **View Before/After Quality** - See impact on quality score and docstring coverage
7. Compare original vs enhanced code
8. Export in your preferred format

### Option 2: Command-Line Interface

#### Analyze a Python file
```bash
python -m docstring_generator.cli analyze path/to/file.py
```

#### Generate docstrings
```bash
python -m docstring_generator.cli generate path/to/file.py --style google -o enhanced.py
```

#### Validate docstrings
```bash
python -m docstring_generator.cli validate path/to/file.py
```

#### Check for code issues
```bash
python -m docstring_generator.cli check path/to/file.py
```

#### Batch process a directory
```bash
python -m docstring_generator.cli batch path/to/directory --recursive --style numpy
```

### Option 3: Python API

```python
from docstring_generator import parse_file, DocstringGenerator, DocstringInserter
from docstring_generator import BatchDocstringGenerator

# Parse a Python file
file_metadata = parse_file("example.py")

print(f"Functions: {len(file_metadata.functions)}")
print(f"Classes: {len(file_metadata.classes)}")

# Generate docstrings in Google style
generator = DocstringGenerator(style="google")
docstring = generator.generate_for_function(file_metadata.functions[0])
print(docstring.content)

# Batch generation
batch_gen = BatchDocstringGenerator(style="numpy")
docstrings = batch_gen.generate_all(file_metadata)

# Insert into source code
with open("example.py", "r") as f:
    original_code = f.read()

inserter = DocstringInserter(original_code)
enhanced_code = inserter.insert_docstrings(docstrings)

# Save enhanced code
with open("example_enhanced.py", "w") as f:
    f.write(enhanced_code)
```

## Project Structure

```
docstring-generator/
├── src/
│   └── docstring_generator/
│       ├── __init__.py              # Package exports
│       ├── parser.py                # AST-based Python parser
│       ├── generator.py             # Docstring generation engine
│       ├── validator.py             # PEP 257 validation
│       ├── error_detector.py        # Code issue detection
│       ├── comment_generator.py     # Inline comment generation
│       ├── inserter.py              # Docstring insertion & diff
│       ├── cli.py                   # Command-line interface
│       ├── models/
│       │   └── __init__.py          # Data models
│       └── templates/
│           └── __init__.py          # Docstring templates
├── examples/
│   └── sample_python_file.py        # Example for testing
├── tests/
│   └── test_*.py                    # Unit tests
├── config/                          # Configuration files
├── docs/                            # Documentation
├── app.py                           # Streamlit dashboard
├── requirements.txt                 # Dependencies
├── setup.py                         # Package setup
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## Modules Overview

### Parser (`parser.py`)
Extracts Python code metadata using AST:
- Functions and methods (including async)
- Classes and dataclasses
- Parameters with type hints
- Decorators
- Docstrings
- Return types and raises

```python
from docstring_generator import parse_file

file_metadata = parse_file("example.py")
# Access: file_metadata.functions, classes, imports, etc.
```

### Generator (`generator.py`)
Generates docstrings in multiple styles:
- **Google style**: `Args:`, `Returns:`, `Raises:`
- **NumPy style**: Formatted sections with dashes
- **reST style**: `:param:`, `:return:`, `:raises:`

```python
from docstring_generator import DocstringGenerator

gen = DocstringGenerator(style="google")
docstring = gen.generate_for_function(function_metadata)
```

### Validator (`validator.py`)
Validates docstrings for PEP 257 compliance:
- Summary line checks (length, capitalization, ending)
- Parameter documentation
- Return value documentation
- Exception documentation
- Quality scoring (0.0 to 1.0)

```python
from docstring_generator import DocstringValidator

validator = DocstringValidator()
result = validator.validate_function(metadata, docstring)
print(f"Valid: {result.is_valid}, Score: {result.score}")
```

### Error Detector (`error_detector.py`)
Detects code issues:
- Syntax errors
- Missing type hints
- Unused imports
- Complex code constructs

```python
from docstring_generator import ErrorDetector

detector = ErrorDetector(file_metadata)
issues = detector.detect_all()
```

### Comment Generator (`comment_generator.py`)
Generates inline comments for complex constructs:
- List/dict/set comprehensions
- Lambda functions
- Context managers (with statements)
- Try-except blocks

### Inserter (`inserter.py`)
Inserts generated docstrings into source code:
- Preserves original formatting and indentation
- Handles nested functions and methods
- Generates unified and HTML diffs
- Provides change statistics

## New Features (Enhanced Version)

### 🎯 Selective Generation
Review and accept **only the docstrings you want** before applying them to your code:
- **Checkbox-based review** - Each generated docstring has a checkbox
- **Preview expanders** - Expand to see full docstring content before accepting
- **Side-by-side layout** - Functions and classes organized in separate columns
- **Selection summary** - Shows total generated, selected, and to-skip counts
- **Selective insertion** - Only applies the docstrings you check

Perfect for:
- Reviewing auto-generated docstrings before committing
- Skipping docstrings that need manual refinement
- Ensuring quality standards are met
- Fine-tuning docstring generation

### 📊 Before/After Quality Analysis
See exactly how much your code quality **improves** after generating docstrings:

**Metrics Compared:**
- **Quality Score** (0-100) - Overall documentation and code quality
- **Docstring Coverage** (%) - Percentage of functions with docstrings

**Visual Comparison:**
```
📈 Before          |  ✨ After          |  📊 Improvement
Score: 35/100      |  Score: 78/100     |  🟢 +43 points
Coverage: 20%      |  Coverage: 85%     |  🟢 +65.0%
```

**Features:**
- Automatic calculation before and after docstring application
- Color-coded improvements (🟢 green for gains, 🔴 red for losses)
- Quantified metrics for presentation and motivation
- Helps justify using the tool to your team

### 📤 Multi-Format Export
Download your enhanced code and reports in multiple formats:

**Code Export:**
- Python (.py) - Your enhanced code with docstrings

**Reports:**
- **Markdown (.md)** - Professional report with metadata, statistics, and function coverage list
- **JSON (.json)** - Structured data including quality scores and coverage metrics
- **CSV (.csv)** - Function-by-function analysis (name, line, parameters, documentation status)
- **HTML (.html)** - Beautiful styled report with metrics dashboard and function status
- **Preview** - View HTML report inline before downloading

### 🎨 Professional UI
Modern Streamlit interface with:
- Rich emoji usage throughout for visual hierarchy
- Color-coded metrics (quality indicators: 🟢/🟡/🔴)
- Responsive grid layouts and columns
- Expandable sections for detailed information
- Progress spinners for long operations
- Professional color schemes and typography

## Docstring Styles

### Google Style
```python
def example(param1: str, param2: int) -> bool:
    """One-line summary.
    
    More detailed description of what the function does.
    
    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.
    
    Returns:
        bool: Description of return value.
    
    Raises:
        ValueError: When parameter is invalid.
    """
    pass
```

### NumPy Style
```python
def example(param1: str, param2: int) -> bool:
    """One-line summary.
    
    More detailed description.
    
    Parameters
    ----------
    param1 : str
        Description of param1.
    param2 : int
        Description of param2.
    
    Returns
    -------
    result : bool
        Description of return value.
    
    Raises
    ------
    ValueError
        When parameter is invalid.
    """
    pass
```

### reStructuredText (reST) Style
```python
def example(param1: str, param2: int) -> bool:
    """One-line summary.
    
    More detailed description.
    
    :param param1: Description of param1.
    :type param1: str
    :param param2: Description of param2.
    :type param2: int
    :return: Description of return value.
    :rtype: bool
    :raises ValueError: When parameter is invalid.
    """
    pass
```

## Configuration

### Environment Variables
```bash
# Optional: Configure API key for AI-based summaries
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Settings (in Streamlit)
- **Docstring Style**: google, numpy, rest
- **Generate Inline Comments**: Enable for complex code explanations
- **Validate PEP 257**: Check compliance with PEP 257 standard

## Advanced Usage

### Batch Processing with Progress Bar
```python
from docstring_generator import parse_directory, BatchDocstringGenerator
from rich.progress import Progress

files = parse_directory("src/", recursive=True)

with Progress() as progress:
    task = progress.add_task("[cyan]Processing...", total=len(files))
    
    for file_meta in files:
        gen = BatchDocstringGenerator(style="google")
        docstrings = gen.generate_all(file_meta)
        progress.update(task, advance=1)
```

### Validating Multiple Files
```python
from docstring_generator import parse_directory, BatchValidator

files = parse_directory("src/", recursive=True)
validator = BatchValidator()

for file_meta in files:
    results = validator.validate_all(file_meta)
    for name, validation in results.items():
        if not validation.is_valid:
            print(f"{name}: {validation.errors}")
```

### Generating Diff Reports
```python
from docstring_generator import DiffGenerator

original_code = open("original.py").read()
enhanced_code = open("enhanced.py").read()

diff = DiffGenerator(original_code, enhanced_code)
print(diff.get_unified_diff())

stats = diff.get_stats()
print(f"Added: {stats['lines_added']}, Removed: {stats['lines_removed']}")
```

## Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook: Check docstring coverage

python -m docstring_generator.cli check --changed-only
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "❌ Code quality checks failed. Run docstring generator to fix."
    exit 1
fi

echo "✅ Code quality checks passed."
exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/docstring-check.yml`:

```yaml
name: Docstring Quality Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: |
          python -m docstring_generator.cli batch src/ --recursive
          python -m docstring_generator.cli validate src/ --recursive
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
docstring-check:
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python -m docstring_generator.cli check src/
    - python -m docstring_generator.cli validate src/
```

## Testing

Run tests:
```bash
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/docstring_generator
```

Test example file:
```bash
python -m docstring_generator.cli analyze examples/sample_python_file.py
python -m docstring_generator.cli generate examples/sample_python_file.py --style google -o examples/sample_enhanced.py
python -m docstring_generator.cli validate examples/sample_enhanced.py
```

## Performance

- **Parsing**: ~10-50ms for typical files (100-1000 lines)
- **Generation**: ~1-5ms per function
- **Validation**: ~2-10ms per docstring
- **Batch Processing**: Process 100+ files in seconds

For large codebases:
```bash
# Use parallel processing
python -m docstring_generator.cli batch src/ --recursive --workers=4
```

## Troubleshooting

### Issue: "SyntaxError: File has syntax errors"
**Solution**: Ensure your Python file is syntactically valid:
```bash
python -m py_compile your_file.py
```

### Issue: Docstrings not inserted properly
**Solution**: Check for complex function signatures. The inserter handles:
- Regular functions and methods
- Async functions
- Nested functions
- Methods in classes

### Issue: Streamlit app not starting
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
streamlit run app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Changelog

### v0.2.0 (Enhanced Release - Current)
- ✨ **Selective Generation** - Review and accept only desired docstrings
- 📊 **Before/After Quality Analysis** - Compare metrics before and after docstring generation
- 🎨 **Professional UI Redesign** - Modern interface with emojis and better visual hierarchy
- 📤 **Multi-format Export** - Added CSV and improved HTML reports with preview
- 🔍 **Enhanced Metrics** - Per-function coverage analysis table
- 📱 **7-page Dashboard** - Home, Analyze, Generate, Compare, Metrics, Validate, Export

### v0.1.0 (Initial Release)
- AST-based Python parser
- Multi-style docstring generation
- PEP 257 validation
- Code issue detection
- Inline comment generation
- Streamlit dashboard
- CLI tool
- Batch processing

## Roadmap

- [x] Selective docstring generation
- [x] Before/After quality comparison
- [x] Multi-format export (Markdown, JSON, CSV, HTML)
- [x] Professional UI with emojis
- [ ] AI-powered summary generation (OpenAI/Anthropic)
- [ ] Advanced type hint inference
- [ ] Database-backed change tracking
- [ ] VS Code extension
- [ ] API server for remote processing
- [ ] Custom template support
- [ ] Multi-language support
- [ ] Dark mode theme

## Support

For issues, questions, or suggestions:
- Create a GitHub issue
- Check existing documentation
- Review example files in `/examples`

---


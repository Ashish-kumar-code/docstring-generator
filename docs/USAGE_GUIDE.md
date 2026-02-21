# Usage Guide

## Table of Contents

1. [Installation](#installation)
2. [Streamlit Dashboard](#streamlit-dashboard)
3. [Command-Line Interface](#command-line-interface)
4. [Python API](#python-api)
5. [Examples](#examples)
6. [Advanced Usage](#advanced-usage)

## Installation

### Step 1: Clone the Repository
```bash
cd docstring-generator
```

### Step 2: Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using poetry (if you have poetry installed)
poetry install
```

### Step 3: Install in Development Mode
```bash
pip install -e .
```

### Step 4: Run Setup Script (Optional)
```bash
# On Linux/macOS
bash setup.sh

# On Windows
setup.bat
```

---

## Streamlit Dashboard

### Starting the Dashboard

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

### Workflow Phases

#### Phase 1: File Selection
- **Option A**: Upload a Python file
  - Click "Upload File"
  - Select a `.py` file
  - File is automatically processed

- **Option B**: Scan Directory
  - Enter directory path (relative or absolute)
  - Optionally enable recursive scan
  - View all Python files found

#### Phase 2: Code Analysis
After file selection, the system performs analysis:
- **Function count**: Total functions and methods
- **Class count**: Total classes
- **Missing docstrings**: Count of items needing documentation

**Displayed information**:
- Function table: Name, type, parameters, docstring status
- Class table: Name, methods, attributes, docstring status

#### Phase 3: Generation
- Review items to be processed
- Select docstring style from sidebar (Google, NumPy, reST)
- Click "Generate" button
- Monitor progress bar
- See generation completion status

#### Phase 4: Validation
- View validation results for each generated docstring
- See PEP 257 compliance status
- Check quality scores
- Review detected code issues:
  - Missing type hints
  - Unused imports
  - Syntax issues

#### Phase 5: Review
- **Left panel**: Original code
- **Right panel**: Enhanced code with docstrings
- **Statistics**:
  - Lines added
  - Lines removed
  - Total changes
  - Original line count

- **Actions**:
  - ✓ Accept Changes (proceed to export)
  - ✗ Reject Changes (go back to generation)

#### Phase 6: Export
Download enhanced code in multiple formats:

**Python File** (`enhanced.py`)
- Direct Python file with docstrings

**Markdown** (`documentation.md`)
- Markdown document with code block

**JSON** (`metadata.json`)
- Metadata about modifications

### Sidebar Settings

**Docstring Style**
- `google`: Google-style docstrings (default)
- `numpy`: NumPy-style docstrings
- `rest`: reStructuredText style

**Options**
- ☐ Generate inline comments
  - Adds explanatory comments for complex constructs
- ☐ Validate PEP 257 compliance
  - Checks docstring format compliance

---

## Command-Line Interface

### Basic Syntax
```bash
python -m docstring_generator.cli <command> [options]
```

### Available Commands

#### 1. ANALYZE
Extract and display metadata from a Python file.

```bash
python -m docstring_generator.cli analyze path/to/file.py [options]
```

**Options**:
- `--style`: Docstring style (default: google)
- `-v, --verbose`: Verbose output

**Example**:
```bash
python -m docstring_generator.cli analyze examples/sample_python_file.py
```

**Output**:
```
Analyzing: examples/sample_python_file.py
✓ Syntax is valid

Module: sample_python_file
Functions: 8
Classes: 3

Functions:
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ Name           ┃ Parent  ┃ Docstr. ┃ Params┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│ calculate...   │ Module  │   ✓     │   1   │
│ parse_json...  │ Module  │   ✗     │   1   │
└────────────────┴─────────┴─────────┴───────┘
```

#### 2. GENERATE
Generate docstrings and optionally save enhanced code.

```bash
python -m docstring_generator.cli generate path/to/file.py [options]
```

**Options**:
- `--style`: Docstring style (default: google)
- `-o, --output`: Output file path (optional)
- `-v, --verbose`: Verbose output

**Example**:
```bash
# Generate and display
python -m docstring_generator.cli generate examples/sample_python_file.py --style google

# Generate and save
python -m docstring_generator.cli generate examples/sample_python_file.py \
    --style numpy \
    -o examples/enhanced.py
```

**Output**:
```
Processing: examples/sample_python_file.py
✓ Generated 5 docstring(s)

Changes:
  Lines added: 42
  Lines removed: 0
  Total changes: 42

Enhanced code preview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers to average.
    
    Returns:
        The average value.
    """
    ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Saved to: examples/enhanced.py
```

#### 3. VALIDATE
Validate docstrings for PEP 257 compliance.

```bash
python -m docstring_generator.cli validate path/to/file.py [options]
```

**Options**:
- `-v, --verbose`: Verbose output

**Example**:
```bash
python -m docstring_generator.cli validate examples/enhanced.py
```

**Output**:
```
Validating: examples/enhanced.py

Validation Results:
┏━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━┓
┃ Name         ┃ Status ┃Score ┃Issues ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━┩
│ calc_avg     │ ✓ Valid│ 95% │   0   │
│ DataProc...  │ ⚠ Warn │ 85% │   2   │
└──────────────┴────────┴──────┴───────┘
```

#### 4. CHECK
Detect code issues (syntax errors, missing type hints, etc.).

```bash
python -m docstring_generator.cli check path/to/file.py [options]
```

**Options**:
- `-v, --verbose`: Verbose output

**Example**:
```bash
python -m docstring_generator.cli check examples/sample_python_file.py
```

**Output**:
```
Checking: examples/sample_python_file.py

Code Issues:
┏━━━━━━━━━━━━┳━━━━━━━━┳───────────────────┳━━━━┓
┃ Severity   ┃ Type   ┃ Message           ┃Ln ┃
┡━━━━━━━━━━━━╇━━━━━━━━╇───────────────────╇━━━━┩
│ WARNING    │ hint   │Missing type hints │ 45 │
│ WARNING    │ import │ Unused: json      │ 12 │
└────────────┴────────┴───────────────────┴────┘

Errors: 0
Warnings: 2
Info: 0
```

#### 5. BATCH
Batch process multiple Python files in a directory.

```bash
python -m docstring_generator.cli batch path/to/directory [options]
```

**Options**:
- `--style`: Docstring style (default: google)
- `-r, --recursive`: Scan subdirectories (default: no)
- `-v, --verbose`: Verbose output

**Example**:
```bash
# Process single directory
python -m docstring_generator.cli batch src/ --style google

# Recursive scan with progress
python -m docstring_generator.cli batch . --recursive --style numpy
```

**Output**:
```
Batch processing: src/

✓ Found 23 Python file(s)

Total functions/methods: 156
Missing docstrings: 45

Processing... ████████████████████ 100%

✓ Batch processing complete
```

---

## Python API

### Basic Usage

#### Parse a File
```python
from docstring_generator import parse_file

# Parse Python file
file_metadata = parse_file("example.py")

# Access information
print(f"Functions: {len(file_metadata.functions)}")
print(f"Classes: {len(file_metadata.classes)}")

# Iterate over functions
for func in file_metadata.functions:
    print(f"  - {func.name} ({len(func.parameters)} params)")
    if func.docstring:
        print(f"    Docstring: {func.docstring[:50]}...")
```

#### Generate Docstrings
```python
from docstring_generator import DocstringGenerator

# Create generator
gen = DocstringGenerator(style="google")

# Generate for first function
func = file_metadata.functions[0]
docstring = gen.generate_for_function(func)

# Access generated content
print(f"Style: {docstring.style}")
print(f"Quality: {docstring.quality_score:.1%}")
print(docstring.content)
```

#### Validate Docstrings
```python
from docstring_generator import DocstringValidator

# Create validator
validator = DocstringValidator()

# Validate docstring
result = validator.validate_function(func, func.docstring)

if result.is_valid:
    print("✓ Valid docstring")
else:
    print(f"✗ Invalid: {result.errors}")
    print(f"Warnings: {result.warnings}")
    print(f"Score: {result.score:.1%}")
```

#### Insert Docstrings
```python
from docstring_generator import (
    BatchDocstringGenerator,
    DocstringInserter,
    DiffGenerator
)

# Generate docstrings for all items
batch_gen = BatchDocstringGenerator(style="google")
docstrings = batch_gen.generate_all(file_metadata)

# Read original code
with open("example.py", "r") as f:
    original_code = f.read()

# Insert docstrings
inserter = DocstringInserter(original_code)
enhanced_code = inserter.insert_docstrings(docstrings)

# Generate diff
diff_gen = DiffGenerator(original_code, enhanced_code)
print(diff_gen.get_unified_diff())

stats = diff_gen.get_stats()
print(f"Lines added: {stats['lines_added']}")
print(f"Lines removed: {stats['lines_removed']}")

# Save enhanced code
with open("example_enhanced.py", "w") as f:
    f.write(enhanced_code)
```

### Advanced API Examples

#### Batch Processing with Progress
```python
from docstring_generator import parse_directory, BatchDocstringGenerator
from rich.progress import Progress

files = parse_directory("src/", recursive=True)

with Progress() as progress:
    task = progress.add_task(
        "[cyan]Processing...",
        total=len(files),
    )
    
    for file_meta in files:
        gen = BatchDocstringGenerator(style="google")
        docstrings = gen.generate_all(file_meta)
        progress.update(task, advance=1)
```

#### Error Detection
```python
from docstring_generator import ErrorDetector

# Detect code issues
detector = ErrorDetector(file_metadata)
issues = detector.detect_all()

# Filter by severity
errors = [i for i in issues if i.severity == "error"]
warnings = [i for i in issues if i.severity == "warning"]

for error in errors:
    print(f"Line {error.line_number}: {error.message}")
```

#### Comments for Complex Code
```python
from docstring_generator import InlineCommentGenerator

# Generate comments for complex constructs
comment_gen = InlineCommentGenerator(original_code)
comments = comment_gen.generate_all()

for comment in comments:
    print(f"Line {comment.line_number}: {comment.comment}")
```

---

## Examples

### Example 1: Simple Function Documentation

**Input** (`math_utils.py`):
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Generated (Google style)**:
```python
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.
    
    Args:
        n (int): The position in the Fibonacci sequence.
    
    Returns:
        int: The Fibonacci number at position n.
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Generated (NumPy style)**:
```python
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.
    
    Parameters
    ----------
    n : int
        The position in the Fibonacci sequence.
    
    Returns
    -------
    int
        The Fibonacci number at position n.
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Example 2: Classes with Methods

**Input** (`person.py`):
```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"
```

**Generated Output**:
```python
class Person:
    """A person with basic information."""
    
    def __init__(self, name: str, age: int):
        """Initialize a person.
        
        Args:
            name (str): The person's name.
            age (int): The person's age.
        """
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        """Return a greeting message.
        
        Returns:
            str: A greeting message.
        """
        return f"Hello, I'm {self.name}"
```

### Example 3: Error Handling and Exceptions

**Input**:
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Generated**:
```python
def divide(a: float, b: float) -> float:
    """Divide two numbers.
    
    Args:
        a (float): The dividend.
        b (float): The divisor.
    
    Returns:
        float: The quotient.
    
    Raises:
        ValueError: If divisor is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

---

## Advanced Usage

### Custom Configuration

Create `.docstring-config.json`:
```json
{
    "docstring_style": "google",
    "validate_pep257": true,
    "generate_inline_comments": true,
    "max_line_length": 79,
    "skip_private": false,
    "summary_required": true
}
```

Load and use:
```python
from config.config import Config

config = Config(".docstring-config.json")
style = config.get("docstring_style")
```

### Parallel Processing

```python
from multiprocessing import Pool
from docstring_generator import parse_directory, BatchDocstringGenerator

def process_file(filepath):
    file_meta = parse_file(filepath)
    gen = BatchDocstringGenerator(style="google")
    return gen.generate_all(file_meta)

files = parse_directory("src/", recursive=True)
filepaths = [f.filepath for f in files]

with Pool(4) as pool:
    results = pool.map(process_file, filepaths)
```

### Integration with Pre-commit

See the pre-commit hook in `config/pre-commit` for automatic validation before commits.

---

For more examples, see the `/examples` directory and the main `README.md`.

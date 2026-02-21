# Architecture Documentation

## System Overview

The Python Docstring Generator is a modular system for automatic docstring generation, validation, and code enhancement. It follows a pipeline architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Dashboard                     │
│  (Phase 1-6: Selection → Analysis → Gen → Validation → Export)
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼────┐          ┌─────▼──────┐
   │   CLI   │          │ Python API │
   │ (Click) │          │  (Modules) │
   └────┬────┘          └─────▲──────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────────────────┐
        │    Docstring Generator Core     │
        └───────────────┬────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼───┐    ┌────▼──────┐
   │  Parser  │    │Generator│    │ Validator │
   │  (AST)   │    │(Template)│    │(PEP 257)  │
   └────┬────┘    └─────┬───┘    └────┬──────┘
        │               │             │
        │    ┌──────────┴─────────────┤
        │    │                        │
   ┌────▼────────────┐         ┌──────▼────────┐
   │   Error         │         │  Inserter &   │
   │   Detector      │         │  Diff Gen     │
   └────┬────────────┘         └──────┬────────┘
        │                             │
        │    ┌────────────┬───────────┘
        │    │            │
   ┌────▼────▼────┐   ┌───▼──────────┐
   │ Comment      │   │File/Export   │
   │ Generator    │   │Management    │
   └─────────────┘   └──────────────┘
```

## Module Architecture

### 1. Parser Module (`parser.py`)

**Purpose**: Extract metadata from Python source code using AST.

**Key Classes**:
- `PythonParser`: Main parser class
  - `parse()`: Parse file and return FileMetadata
  - `_parse_function()`: Extract function metadata
  - `_parse_class()`: Extract class metadata
  - `_parse_parameters()`: Parse function parameters
  - `_get_source_segment()`: Get source code for a node

**Input**: Python source code (file path)
**Output**: `FileMetadata` object with:
- Functions and methods
- Classes and dataclasses
- Parameters with type hints
- Decorators
- Docstrings
- Return and raise information

**Example**:
```python
parser = PythonParser("example.py")
file_metadata = parser.parse()
```

### 2. Generator Module (`generator.py`)

**Purpose**: Generate docstrings in multiple styles.

**Key Classes**:
- `DocstringGenerator`: Single file generator
  - `generate_for_function()`: Generate function docstring
  - `generate_for_class()`: Generate class docstring
  - `_generate_summary()`: Rule-based summary
  - `_calculate_quality_score()`: Quality scoring

- `BatchDocstringGenerator`: Multiple files
  - `generate_all()`: Batch generation

**Output**: `GeneratedDocstring` object with:
- Content (formatted docstring)
- Style (google, numpy, rest)
- Quality score (0.0-1.0)
- Sections generated (dict)

**Example**:
```python
gen = DocstringGenerator(style="google")
docstring = gen.generate_for_function(func_metadata)
```

### 3. Validator Module (`validator.py`)

**Purpose**: Validate docstrings for PEP 257 compliance.

**Key Classes**:
- `DocstringValidator`: Single docstring validation
  - `validate_function()`: Validate function docstring
  - `validate_class()`: Validate class docstring
  - `_check_summary_line()`: PEP 257 summary checks
  - `_check_parameter_documentation()`: Parameter docs
  - `_check_return_documentation()`: Return docs
  - `_check_raises_documentation()`: Exception docs

- `BatchValidator`: Multiple docstrings

**Output**: `ValidationResult` object with:
- `is_valid`: Boolean validity
- `pep257_status`: PEP257Status enum
- `errors` and `warnings`: Issue lists
- `score`: Quality score (0.0-1.0)

**Validation Rules**:
1. Summary line < 79 chars, ends with period, starts with capital
2. All parameters documented
3. Return value documented (except `__init__`)
4. Exceptions documented
5. No trailing whitespace
6. Proper format structure

**Example**:
```python
validator = DocstringValidator()
result = validator.validate_function(metadata, docstring_text)
```

### 4. Error Detector Module (`error_detector.py`)

**Purpose**: Detect code issues and complex constructs.

**Key Classes**:
- `ErrorDetector`: Detect various code issues
  - `detect_all()`: Detect all issues
  - `detect_syntax_errors()`: Syntax validation
  - `detect_missing_type_hints()`: Missing type hints
  - `detect_unused_imports()`: Unused imports

- `ComplexityAnalyzer`: Find complex constructs
  - `find_complex_constructs()`: Identify complex code

**Output**: List of `CodeIssue` objects with:
- `issue_type`: Type of issue
- `severity`: error, warning, info
- `message`: Description
- `line_number`: Location
- `suggestion`: How to fix

**Issues Detected**:
- Syntax errors
- Missing type hints (warning)
- Unused imports (warning)
- Complex constructs (info)

**Example**:
```python
detector = ErrorDetector(file_metadata)
issues = detector.detect_all()
```

### 5. Comment Generator Module (`comment_generator.py`)

**Purpose**: Generate inline comments for complex code constructs.

**Key Classes**:
- `InlineCommentGenerator`: Generate inline comments
  - `generate_all()`: Generate comments for all constructs
  - `_comment_comprehension()`: List/dict comprehensions
  - `_comment_lambda()`: Lambda functions
  - `_comment_context_manager()`: With statements
  - `_comment_try_except()`: Try-except blocks

**Output**: List of `InlineComment` objects with:
- `code_construct`: Type of construct
- `line_number`: Location
- `comment`: Generated comment
- `complexity_level`: 1-5 scale

**Example**:
```python
comment_gen = InlineCommentGenerator(source_code)
comments = comment_gen.generate_all()
```

### 6. Inserter Module (`inserter.py`)

**Purpose**: Insert generated docstrings into source code and generate diffs.

**Key Classes**:
- `DocstringInserter`: Insert docstrings into code
  - `insert_docstrings()`: Insert all docstrings
  - `_insert_at_node()`: Insert at specific node

- `DiffGenerator`: Generate diffs
  - `get_unified_diff()`: Unified diff format
  - `get_html_diff()`: HTML diff for display
  - `get_stats()`: Change statistics

**Output**: 
- Enhanced Python code (string)
- Diff information (unified, html)
- Statistics (added, removed, total lines)

**Example**:
```python
inserter = DocstringInserter(original_code)
enhanced = inserter.insert_docstrings(docstrings_map)

diff_gen = DiffGenerator(original_code, enhanced)
stats = diff_gen.get_stats()
```

### 7. Models Module (`models/__init__.py`)

**Purpose**: Define data structures used throughout the system.

**Key Classes**:
- `Parameter`: Function parameter
- `ReturnInfo`: Return type info
- `RaisesInfo`: Exception info
- `FunctionMetadata`: Function metadata
- `ClassMetadata`: Class metadata
- `FileMetadata`: Complete file metadata
- `GeneratedDocstring`: Generated docstring
- `ValidationResult`: Validation results
- `CodeIssue`: Code issue
- `ProcessingResult`: Overall processing result
- `DiffView`: Diff information

**Enums**:
- `DocstringStyle`: google, numpy, rest
- `PEP257Status`: compliant, warning, error

### 8. Templates Module (`templates/__init__.py`)

**Purpose**: Define docstring format templates.

**Key Classes**:
- `DocstringTemplate`: Abstract base class
- `GoogleDocstringTemplate`: Google format
- `NumpyDocstringTemplate`: NumPy format
- `ReSTDocstringTemplate`: reStructuredText format
- `TemplateFactory`: Factory for creating templates

**Template Structure**:
```
Summary line.

Extended description with more details.

Args/Parameters:
    param_name: Description

Returns/Return:
    Description

Raises/Raises:
    ExceptionType: Description
```

### 9. CLI Module (`cli.py`)

**Purpose**: Command-line interface using Click.

**Commands**:
- `analyze`: Parse and show metadata
- `generate`: Generate docstrings
- `validate`: Validate docstrings
- `check`: Detect code issues
- `batch`: Process entire directories

**Example**:
```bash
python -m docstring_generator.cli generate file.py --style google -o output.py
```

## Data Flow

### 1. File Selection → Analysis Flow
```
User Input (file)
    ↓
PythonParser.parse()
    ↓
FileMetadata
    ↓
Display in Streamlit
```

### 2. Generation Flow
```
FileMetadata
    ↓
BatchDocstringGenerator.generate_all()
    ├→ For each function:
    │  └→ DocstringGenerator.generate_for_function()
    │     ├→ _generate_summary()
    │     ├→ _generate_description()
    │     └→ template.function_docstring()
    │
    └→ Dict[name, GeneratedDocstring]
       ↓
    DocstringInserter.insert_docstrings()
       ↓
    Enhanced Code
```

### 3. Validation Flow
```
GeneratedDocstring
    ↓
DocstringValidator.validate_function()
    ├→ _check_summary_line()
    ├→ _check_parameter_documentation()
    ├→ _check_return_documentation()
    ├→ _check_raises_documentation()
    └→ _calculate_score()
       ↓
    ValidationResult
```

### 4. Complete Pipeline
```
Python File
    ↓
Parser (AST) → FileMetadata
    ↓                ↓
Error Detector    Generator
    ↓                ↓
Code Issues    GeneratedDocstring
    ↓                ↓
    └→ Validator → ValidationResult
            ↓
      Inserter → Enhanced Code
            ↓
      DiffGenerator → Diff + Stats
            ↓
      Streamlit UI (Review & Export)
            ↓
      Download/Save
```

## Key Design Patterns

### 1. Builder Pattern (Generator)
- `DocstringGenerator.generate_for_function()`
- Builds complex docstring using templates
- Returns immutable `GeneratedDocstring` object

### 2. Visitor Pattern (Parser)
- `ast.walk()` traverses AST nodes
- Different handlers for functions, classes, imports
- Extracts relevant metadata

### 3. Strategy Pattern (Templates)
- `DocstringTemplate` abstract class
- Different implementations (Google, NumPy, reST)
- `TemplateFactory` selects strategy

### 4. Factory Pattern (Config)
- `TemplateFactory.create(style)`
- `ErrorDetector` factory methods

### 5. Singleton Pattern (ConfigManager)
- Optional single configuration instance
- Shared across application

## Performance Considerations

### Parsing
- **O(n)** where n = file size
- ~10-50ms for typical files
- No external API calls

### Generation
- **O(m)** where m = number of functions
- ~1-5ms per function
- Template-based, no ML required

### Validation
- **O(d)** where d = docstring size
- ~2-10ms per docstring
- Simple rule-based checks

### Batch Processing
- Parallel processing ready
- Can process 100+ files in seconds
- Memory-efficient (stream processing)

## Extension Points

### 1. Custom Docstring Styles
Create new template class:
```python
class CustomTemplate(DocstringTemplate):
    def function_docstring(self, metadata, summary, description):
        # Custom implementation
        pass
```

### 2. Custom Validation Rules
Extend `DocstringValidator`:
```python
def _check_custom_rule(self, docstring):
    # Custom validation logic
    if not valid:
        self.errors.append("Custom error")
```

### 3. Custom Error Detection
Extend `ErrorDetector`:
```python
def detect_custom_issues(self):
    # Custom detection logic
    pass
```

## Dependencies

### Core
- `ast` (Python stdlib): AST parsing
- `logging` (Python stdlib): Logging
- `typing` (Python stdlib): Type hints
- `pathlib` (Python stdlib): File operations

### CLI
- `click`: Command-line framework
- `rich`: Rich terminal output

### Web UI
- `streamlit`: Web dashboard
- `streamlit-elements`: Custom components

### Quality Tools
- `pydocstyle`: PEP 257 validation
- `black`: Code formatting
- `pylint`: Code linting
- `mypy`: Type checking

### Testing
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting

## Thread Safety

- Parser: Thread-safe (read-only operations)
- Generator: Thread-safe (stateless)
- Validator: Thread-safe (stateless)
- Session state: Handled by Streamlit

## Error Handling

### Parse Errors
- Catch `SyntaxError` from `ast.parse()`
- Mark file as `syntax_valid=False`
- Continue processing where possible

### Insertion Errors
- Graceful fallback if insertion fails
- Return original code unchanged
- Log error for debugging

### Validation Errors
- Collect all errors/warnings
- Return comprehensive `ValidationResult`
- Provide actionable suggestions

## Security Considerations

1. **Code Execution**: Parser uses `ast` (safe), doesn't execute code
2. **File I/O**: Validates paths before reading
3. **Template Injection**: Templates are hardcoded, no user injection
4. **Input Validation**: Type hints and assertions throughout

## Future Enhancements

1. **AI Summaries**: Integration with OpenAI/Anthropic for intelligent summaries
2. **Database**: Track changes over time
3. **VS Code Extension**: Native integration
4. **Multi-language**: Extend to Java, TypeScript, etc.
5. **Custom Rules**: User-defined validation rules
6. **Performance**: Caching, parallelization
7. **IDE Integration**: PyCharm, IntelliJ plugins

---

This architecture ensures modularity, testability, and extensibility while maintaining high performance and code quality.

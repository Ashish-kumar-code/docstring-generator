"""Python Docstring Generator - Automated docstring generation and validation."""

__version__ = "0.1.0"
__author__ = "AI Assistant"
__license__ = "MIT"

from .parser import PythonParser, parse_file, parse_directory
from .generator import DocstringGenerator, BatchDocstringGenerator
from .validator import DocstringValidator, BatchValidator
from .error_detector import ErrorDetector, ComplexityAnalyzer
from .comment_generator import InlineCommentGenerator
from .inserter import DocstringInserter, DiffGenerator
from .models import (
    DocstringStyle,
    FunctionMetadata,
    ClassMetadata,
    FileMetadata,
    GeneratedDocstring,
    ValidationResult,
    CodeIssue,
    ProcessingResult,
    Parameter,
)


__all__ = [
    "PythonParser",
    "parse_file",
    "parse_directory",
    "DocstringGenerator",
    "BatchDocstringGenerator",
    "DocstringValidator",
    "BatchValidator",
    "ErrorDetector",
    "ComplexityAnalyzer",
    "InlineCommentGenerator",
    "DocstringInserter",
    "DiffGenerator",
    "DocstringStyle",
    "FunctionMetadata",
    "ClassMetadata",
    "FileMetadata",
    "GeneratedDocstring",
    "ValidationResult",
    "CodeIssue",
    "ProcessingResult",
    "Parameter",
]

"""Compact models module with essential dataclasses and enums.

This trimmed version keeps the shapes required by the rest of the package
but removes some convenience methods and verbose comments to stay
under the requested size limit.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class DocstringStyle(str, Enum):
    GOOGLE = "google"
    NUMPY = "numpy"
    REST = "rest"


class PEP257Status(str, Enum):
    COMPLIANT = "compliant"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Parameter:
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None
    def __post_init__(self):
        if not self.name:
            raise ValueError("Parameter name cannot be empty")


@dataclass
class ReturnInfo:
    type_hint: Optional[str] = None
    description: Optional[str] = None


@dataclass
class FunctionMetadata:
    name: str
    type: str
    lineno: int = 0
    parameters: List[Parameter] = field(default_factory=list)
    returns: Optional[ReturnInfo] = None
    docstring: Optional[str] = None
    def summary(self) -> str:
        params = ", ".join(p.name for p in self.parameters)
        return f"{self.name}({params})"


@dataclass
class ClassMetadata:
    name: str
    lineno: int = 0
    methods: List[FunctionMetadata] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class GeneratedDocstring:
    style: DocstringStyle
    content: str
    quality_score: float
    sections_generated: Dict[str, bool] = field(default_factory=dict)


@dataclass
class ValidationResult:
    is_valid: bool
    pep257_status: PEP257Status
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    score: float = 0.0


@dataclass
class CodeIssue:
    issue_type: str
    severity: str
    message: str
    line_number: Optional[int] = None
    column: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class InlineComment:
    code_construct: str
    line_number: Optional[int] = None
    comment: Optional[str] = None
    complexity_level: int = 0


@dataclass
class FileMetadata:
    filepath: str
    module_name: str
    functions: List[FunctionMetadata] = field(default_factory=list)
    classes: List[ClassMetadata] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    source_code: Optional[str] = None
    syntax_valid: bool = True


@dataclass
class ProcessingResult:
    filepath: str
    original_code: str
    enhanced_code: str
    file_metadata: FileMetadata
    generated_docstrings: Dict[str, GeneratedDocstring] = field(default_factory=dict)

"""docstring validator keeping public API."""

from typing import List, Dict
from .models import FunctionMetadata, ClassMetadata, ValidationResult, PEP257Status


class DocstringValidator:
    """Lightweight validator focusing on common checks."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_function(self, metadata: FunctionMetadata, docstring: str) -> ValidationResult:
        self.errors = []
        self.warnings = []
        if not docstring:
            self.errors.append("Missing docstring")
            return ValidationResult(is_valid=False, pep257_status=PEP257Status.ERROR, errors=self.errors, warnings=self.warnings, score=0.0)
        self._check_summary_line(docstring)
        self._check_params(metadata, docstring)
        self._check_returns(metadata, docstring)
        self._check_raises(metadata, docstring)
        self._check_format(docstring)
        score = self._calc_score(docstring, len(self.errors), len(self.warnings))
        status = PEP257Status.ERROR if self.errors else (PEP257Status.WARNING if self.warnings else PEP257Status.COMPLIANT)
        return ValidationResult(is_valid=status == PEP257Status.COMPLIANT, pep257_status=status, errors=self.errors, warnings=self.warnings, score=score)

    def validate_class(self, metadata: ClassMetadata, docstring: str) -> ValidationResult:
        self.errors = []
        self.warnings = []
        if not docstring:
            self.errors.append("Missing docstring")
            return ValidationResult(is_valid=False, pep257_status=PEP257Status.ERROR, errors=self.errors, warnings=self.warnings, score=0.0)
        self._check_summary_line(docstring)
        if getattr(metadata, "is_dataclass", False) and "attribute" not in docstring.lower():
            self.warnings.append("Class attributes not documented")
        self._check_format(docstring)
        score = self._calc_score(docstring, len(self.errors), len(self.warnings))
        status = PEP257Status.ERROR if self.errors else (PEP257Status.WARNING if self.warnings else PEP257Status.COMPLIANT)
        return ValidationResult(is_valid=status == PEP257Status.COMPLIANT, pep257_status=status, errors=self.errors, warnings=self.warnings, score=score)

    def _check_summary_line(self, docstring: str) -> None:
        lines = docstring.split("\n")
        if not lines or not lines[0].strip():
            self.errors.append("Empty or missing summary line")
            return
        summary = lines[0].strip()
        if len(summary) > 79:
            self.warnings.append("Summary line too long")
        if not summary.endswith("."):
            self.warnings.append("Summary should end with a period")
        if summary and not summary[0].isupper():
            self.warnings.append("Summary should start with a capital letter")

    def _check_params(self, metadata: FunctionMetadata, docstring: str) -> None:
        if not getattr(metadata, "parameters", None):
            return
        txt = docstring.lower()
        for p in metadata.parameters:
            name = p.name.replace("*", "").lower()
            if name not in txt:
                self.warnings.append(f"Parameter '{p.name}' not documented")

    def _check_returns(self, metadata: FunctionMetadata, docstring: str) -> None:
        if metadata.name == "__init__" or not getattr(metadata, "returns", None):
            return
        if "return" not in docstring.lower():
            self.warnings.append("Return value not documented")

    def _check_raises(self, metadata: FunctionMetadata, docstring: str) -> None:
        if not getattr(metadata, "raises", None):
            return
        if "raise" not in docstring.lower():
            self.warnings.append("Exceptions not documented")

    def _check_format(self, docstring: str) -> None:
        if not docstring.strip():
            self.errors.append("Docstring is empty or whitespace only")
            return
        for i, line in enumerate(docstring.split("\n")):
            if line != line.rstrip():
                self.warnings.append(f"Line {i+1} has trailing whitespace")

    def _calc_score(self, docstring: str, errors: int, warnings: int) -> float:
        if not docstring:
            return 0.0
        score = 1.0 - errors * 0.25 - warnings * 0.1
        words = len(docstring.split())
        if words > 40:
            score += 0.05
        return max(0.0, min(1.0, score))


class BatchValidator:
    """Batch validator for a file's metadata."""

    def __init__(self) -> None:
        self.validator = DocstringValidator()

    def validate_all(self, file_metadata) -> Dict[str, ValidationResult]:
        out: Dict[str, ValidationResult] = {}
        for fn in getattr(file_metadata, "functions", []) or []:
            if getattr(fn, "docstring", None):
                out[fn.name] = self.validator.validate_function(fn, fn.docstring)
        for cls in getattr(file_metadata, "classes", []) or []:
            if getattr(cls, "docstring", None):
                out[cls.name] = self.validator.validate_class(cls, cls.docstring)
            for m in getattr(cls, "methods", []) or []:
                if getattr(m, "docstring", None):
                    out[f"{cls.name}.{m.name}"] = self.validator.validate_function(m, m.docstring)
        return out


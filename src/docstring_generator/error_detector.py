""" code issue detection and complexity analysis."""

import ast
from typing import List, Dict
from .models import CodeIssue, FileMetadata


class ErrorDetector:
    """Detect a small set of common issues for a FileMetadata."""

    def __init__(self, file_metadata: FileMetadata) -> None:
        self.file_metadata = file_metadata
        self.issues: List[CodeIssue] = []

    def detect_all(self) -> List[CodeIssue]:
        self.issues = []
        if not getattr(self.file_metadata, "syntax_valid", True):
            self._syntax()
        self._missing_type_hints()
        self._unused_imports()
        return self.issues

    def _syntax(self) -> None:
        try:
            ast.parse(getattr(self.file_metadata, "source_code", "") or "")
        except SyntaxError as e:
            self.issues.append(CodeIssue(issue_type="syntax_error", severity="error", message=f"Syntax error: {e.msg}", line_number=e.lineno, column=e.offset, suggestion="Fix syntax"))

    def _missing_type_hints(self) -> None:
        for fn in getattr(self.file_metadata, "functions", []) or []:
            self._check_fn(fn)
        for cls in getattr(self.file_metadata, "classes", []) or []:
            for m in getattr(cls, "methods", []) or []:
                self._check_fn(m)

    def _check_fn(self, fn) -> None:
        if fn.name in ("__init__", "__str__", "__repr__"):
            return
        missing = [p.name for p in getattr(fn, "parameters", []) or [] if p.name not in ("self", "cls") and not getattr(p, "type_hint", None)]
        if missing:
            self.issues.append(CodeIssue(issue_type="missing_type_hint", severity="warning", message=f"Missing type hints: {', '.join(missing)}", line_number=getattr(fn, "lineno", None), suggestion="Add type hints"))
        if fn.name != "__init__" and not getattr(fn, "returns", None):
            self.issues.append(CodeIssue(issue_type="missing_return_type", severity="info", message="Missing return type", line_number=getattr(fn, "lineno", None)))

    def _unused_imports(self) -> None:
        imports = getattr(self.file_metadata, "imports", []) or []
        src = (getattr(self.file_metadata, "source_code", "") or "").lower()
        for stmt in imports:
            for name in self._parse_import_names(stmt):
                if name.lower() not in src:
                    self.issues.append(CodeIssue(issue_type="unused_import", severity="warning", message=f"Unused import '{name}'", suggestion=f"Remove {name}"))

    def _parse_import_names(self, stmt: str) -> List[str]:
        stmt = stmt.strip()
        if stmt.startswith("import "):
            parts = stmt[7:].split(",")
            return [p.strip().split()[0] for p in parts if p.strip()]
        if stmt.startswith("from ") and " import " in stmt:
            part = stmt.split(" import ", 1)[1]
            return [p.strip().split()[0] for p in part.split(",") if p.strip() and p.strip() != "*"]
        return []


class ComplexityAnalyzer:
    """Find simple complex constructs like comprehensions, lambdas, try/except."""

    def __init__(self, source_code: str) -> None:
        self.source_code = source_code or ""
        self.tree = ast.parse(self.source_code) if self.source_code else None

    def find_complex_constructs(self) -> Dict[str, List[Dict[str, int]]]:
        out = {"comprehensions": [], "lambdas": [], "with": [], "try": []}
        if not self.tree:
            return out
        for n in ast.walk(self.tree):
            if isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                out["comprehensions"].append({"line": getattr(n, "lineno", None)})
            elif isinstance(n, ast.Lambda):
                out["lambdas"].append({"line": getattr(n, "lineno", None)})
            elif isinstance(n, ast.With):
                out["with"].append({"line": getattr(n, "lineno", None)})
            elif isinstance(n, ast.Try):
                out["try"].append({"line": getattr(n, "lineno", None), "handlers": len(getattr(n, "handlers", []))})
        return out


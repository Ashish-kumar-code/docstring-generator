"""Insert generated docstrings into Python source code."""

import ast
from typing import Dict
from .models import GeneratedDocstring


class DocstringInserter:
    """Insert docstrings into Python code using AST positions."""

    def __init__(self, source_code: str) -> None:
        self.source_code = source_code or ""
        self.lines = self.source_code.split("\n")
        self.tree = ast.parse(self.source_code) if self.source_code else None

    def insert_docstrings(self, docstrings_map: Dict[str, GeneratedDocstring], _: Dict[str, object] = None) -> str:
        if not self.tree:
            return self.source_code
        inserts = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = node.name
                for key, obj in docstrings_map.items():
                    if key == name or key.endswith(f".{name}"):
                        if not ast.get_docstring(node):
                            inserts.append((node.lineno, node, obj.content))
                        break
        # insert from bottom to top
        for lineno, node, content in sorted(inserts, key=lambda x: x[0], reverse=True):
            self._insert_at_lineno(lineno, node, content)
        return "\n".join(self.lines)

    def _insert_at_lineno(self, lineno: int, node: ast.AST, docstring: str) -> None:
        # Find insertion index after the def/class header
        idx = lineno
        while idx < len(self.lines) and not self.lines[idx - 1].rstrip().endswith(":"):
            idx += 1
        # compute indent
        header = self.lines[lineno - 1]
        indent = len(header) - len(header.lstrip()) + 4
        pad = " " * indent
        block = [pad + '"""'] + [pad + l if l.strip() else "" for l in docstring.split("\n")] + [pad + '"""']
        insert_at = min(idx, len(self.lines))
        for i, line in enumerate(block):
            self.lines.insert(insert_at + i, line)


class DiffGenerator:
    """Compact diff utility for original vs enhanced code."""

    def __init__(self, original: str, enhanced: str) -> None:
        self.original = original or ""
        self.enhanced = enhanced or ""

    def get_unified_diff(self) -> str:
        import difflib

        return "\n".join(difflib.unified_diff(self.original.split("\n"), self.enhanced.split("\n"), fromfile="original.py", tofile="enhanced.py", lineterm=""))

    def get_html_diff(self) -> str:
        import difflib

        return difflib.HtmlDiff().make_file(self.original.split("\n"), self.enhanced.split("\n"), fromdesc="Original", todesc="Enhanced")

    def get_stats(self) -> Dict[str, int]:
        import difflib

        o = self.original.split("\n")
        e = self.enhanced.split("\n")
        matcher = difflib.SequenceMatcher(None, o, e)
        added = removed = 0
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "insert":
                added += j2 - j1
            elif tag == "delete":
                removed += i2 - i1
            elif tag == "replace":
                removed += i2 - i1
                added += j2 - j1
        return {"lines_added": added, "lines_removed": removed, "total_changes": added + removed}


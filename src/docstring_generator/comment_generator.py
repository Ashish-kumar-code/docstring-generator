"""inline comment generator for simple constructs."""

import ast
from typing import List
from .models import InlineComment


class InlineCommentGenerator:
    """Detect a few constructs and return InlineComment instances."""

    def __init__(self, source_code: str) -> None:
        self.tree = ast.parse(source_code) if source_code else None

    def generate_all(self) -> List[InlineComment]:
        out: List[InlineComment] = []
        if not self.tree:
            return out
        for n in ast.walk(self.tree):
            if isinstance(n, (ast.ListComp, ast.DictComp, ast.SetComp)):
                out.append(InlineComment(code_construct="comprehension", line_number=getattr(n, "lineno", None), comment="Comprehension: compact iteration.", complexity_level=2))
            elif isinstance(n, ast.Lambda):
                out.append(InlineComment(code_construct="lambda", line_number=getattr(n, "lineno", None), comment="Lambda: anonymous inline function.", complexity_level=2))
            elif isinstance(n, ast.With):
                out.append(InlineComment(code_construct="with", line_number=getattr(n, "lineno", None), comment="With: context manager for resource cleanup.", complexity_level=1))
            elif isinstance(n, ast.Try):
                out.append(InlineComment(code_construct="try", line_number=getattr(n, "lineno", None), comment="Try/except: handles exceptions.", complexity_level=2))
        return out


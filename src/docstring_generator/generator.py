"""docstring generation engine (keeps public API)."""

from typing import Dict
from .models import (
    FunctionMetadata,
    ClassMetadata,
    GeneratedDocstring,
    DocstringStyle,
)
from .templates import TemplateFactory


class DocstringGenerator:
    """Minimal generator that produces docstrings using templates."""

    def __init__(self, style: str = "google") -> None:
        self.style = DocstringStyle(style.lower())
        self.template = TemplateFactory.create(style)

    def generate_for_function(self, metadata: FunctionMetadata, summary: str = "") -> GeneratedDocstring:
        if not summary:
            summary = self._summary_from_name(metadata.name)
        description = self._brief_description(metadata)
        content = self.template.function_docstring(metadata, summary=summary, description=description)
        score = self._score(metadata, content, is_function=True)
        return GeneratedDocstring(style=self.style, content=content, quality_score=score, sections_generated=self._sections_fn(metadata))

    def generate_for_class(self, metadata: ClassMetadata, summary: str = "") -> GeneratedDocstring:
        if not summary:
            summary = f"{metadata.name} class."
        description = self._brief_description_class(metadata)
        content = self.template.class_docstring(metadata, summary=summary, description=description)
        score = self._score(metadata, content, is_function=False)
        return GeneratedDocstring(style=self.style, content=content, quality_score=score, sections_generated=self._sections_cls(metadata))

    def _summary_from_name(self, name: str) -> str:
        if name.startswith("get_"):
            return f"Get {name[4:].replace('_', ' ')}."
        if name.startswith("set_"):
            return f"Set {name[4:].replace('_', ' ')}."
        return name.replace("_", " ").capitalize() + "."

    def _brief_description(self, metadata: FunctionMetadata) -> str:
        parts = []
        if getattr(metadata, "is_async", False):
            parts.append("Asynchronous.")
        if getattr(metadata, "decorators", None):
            parts.append("Decorated.")
        return " ".join(parts)

    def _brief_description_class(self, metadata: ClassMetadata) -> str:
        parts = []
        if getattr(metadata, "bases", None):
            parts.append("Inherits.")
        if getattr(metadata, "decorators", None):
            parts.append("Decorated.")
        return " ".join(parts)

    def _score(self, metadata, content: str, is_function: bool = True) -> float:
        if not content:
            return 0.0
        score = 0.4
        words = len(content.split())
        if words > 15:
            score += 0.3
        elif words > 6:
            score += 0.15
        if is_function and getattr(metadata, "parameters", None):
            score += 0.1
        return min(score, 1.0)

    def _sections_fn(self, metadata: FunctionMetadata) -> Dict[str, bool]:
        return {"summary": True, "description": bool(self._brief_description(metadata)), "args": bool(getattr(metadata, "parameters", None))}

    def _sections_cls(self, metadata: ClassMetadata) -> Dict[str, bool]:
        return {"summary": True, "description": bool(self._brief_description_class(metadata)), "attributes": bool(getattr(metadata, "attributes", None))}


class BatchDocstringGenerator:
    """Batch generator for a file's metadata."""

    def __init__(self, style: str = "google") -> None:
        self.generator = DocstringGenerator(style)

    def generate_all(self, file_metadata) -> Dict[str, GeneratedDocstring]:
        out: Dict[str, GeneratedDocstring] = {}
        for fn in getattr(file_metadata, "functions", []) or []:
            if not getattr(fn, "docstring", None):
                out[fn.name] = self.generator.generate_for_function(fn)
        for cls in getattr(file_metadata, "classes", []) or []:
            if not getattr(cls, "docstring", None):
                out[cls.name] = self.generator.generate_for_class(cls)
            for m in getattr(cls, "methods", []) or []:
                if not getattr(m, "docstring", None) and m.name != "__init__":
                    out[f"{cls.name}.{m.name}"] = self.generator.generate_for_function(m)
        return out


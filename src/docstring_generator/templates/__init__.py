"""Minimal docstring template utilities kept concise for the project.

This module exposes a small `TemplateFactory.create(style)` which returns a
callable object with `function_docstring(metadata, ...)` and
`class_docstring(metadata, ...)`. Implementations are intentionally compact
and conservative to keep the codebase small while preserving behavior.
"""

from typing import Any


class _BaseTemplate:
    def function_docstring(self, metadata: Any, summary: str = "", description: str = "") -> str:
        parts = []
        if summary:
            parts.append(summary)
        else:
            parts.append(f"{getattr(metadata, 'name', 'function')}()")
        if description:
            parts.append("")
            parts.append(description)
        # Simple args/returns rendering if available
        params = getattr(metadata, 'parameters', None)
        if params:
            parts.append("")
            parts.append("Args:")
            for p in params:
                parts.append(f"    {getattr(p,'name','arg')}: Description.")
        returns = getattr(metadata, 'returns', None)
        if returns:
            parts.append("")
            parts.append("Returns:")
            parts.append("    Description.")
        return "\n".join(parts)

    def class_docstring(self, metadata: Any, summary: str = "", description: str = "") -> str:
        parts = []
        if summary:
            parts.append(summary)
        else:
            parts.append(f"{getattr(metadata, 'name', 'Class')} class.")
        if description:
            parts.append("")
            parts.append(description)
        attrs = getattr(metadata, 'attributes', None)
        if attrs:
            parts.append("")
            parts.append("Attributes:")
            for a in attrs:
                parts.append(f"    {a}: Description.")
        return "\n".join(parts)


class _Google(_BaseTemplate):
    pass


class _Numpy(_BaseTemplate):
    def function_docstring(self, metadata: Any, summary: str = "", description: str = "") -> str:
        parts = []
        if summary:
            parts.append(summary)
        else:
            parts.append(f"{getattr(metadata, 'name', 'function')}()")
        if description:
            parts.append("")
            parts.append(description)
        params = getattr(metadata, 'parameters', None)
        if params:
            parts.append("")
            parts.append("Parameters")
            for p in params:
                parts.append(f"    {getattr(p,'name','arg')} : {getattr(p,'type_hint', '')}")
        returns = getattr(metadata, 'returns', None)
        if returns:
            parts.append("")
            parts.append("Returns")
            parts.append(f"    {getattr(returns, 'type_hint', '')}")
        return "\n".join(parts)


class _ReST(_BaseTemplate):
    def function_docstring(self, metadata: Any, summary: str = "", description: str = "") -> str:
        parts = []
        if summary:
            parts.append(summary)
        else:
            parts.append(f"{getattr(metadata, 'name', 'function')}()")
        if description:
            parts.append("")
            parts.append(description)
        params = getattr(metadata, 'parameters', None)
        if params:
            parts.append("")
            for p in params:
                parts.append(f":param {getattr(p,'type_hint','')}: {getattr(p,'name','arg')}" )
        returns = getattr(metadata, 'returns', None)
        if returns:
            parts.append("")
            parts.append(f":return: {getattr(returns,'type_hint','')}" )
        return "\n".join(parts)


class TemplateFactory:
    _map = {"google": _Google, "numpy": _Numpy, "rest": _ReST}

    @classmethod
    def create(cls, style: str):
        key = (style or "google").lower()
        impl = cls._map.get(key)
        if not impl:
            raise ValueError(f"Unsupported style: {style}")
        return impl()

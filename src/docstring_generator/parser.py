"""AST parser: provides `parse_file` and `parse_directory`."""

import ast
from pathlib import Path
from typing import List, Optional
from .models import FunctionMetadata, ClassMetadata, FileMetadata, Parameter, ReturnInfo


def _from_arg(arg) -> Parameter:
    return Parameter(name=getattr(arg, 'arg', 'arg'), type_hint=(ast.unparse(arg.annotation) if getattr(arg, 'annotation', None) else None))


def _parse_function(node: ast.AST, parent: Optional[str] = None) -> FunctionMetadata:
    name = getattr(node, 'name', 'func')
    lineno = getattr(node, 'lineno', 0)
    params = []
    args = getattr(node, 'args', None)
    if args:
        for a in (getattr(args, 'posonlyargs', []) + getattr(args, 'args', [])):
            params.append(_from_arg(a))
        if getattr(args, 'vararg', None):
            params.append(Parameter(name='*' + args.vararg.arg))
        for a in getattr(args, 'kwonlyargs', []):
            params.append(_from_arg(a))
        if getattr(args, 'kwarg', None):
            params.append(Parameter(name='**' + args.kwarg.arg))
    returns = None
    if getattr(node, 'returns', None):
        returns = ReturnInfo(type_hint=ast.unparse(node.returns))
    return FunctionMetadata(name=name, type='method' if parent else 'function', lineno=lineno, parameters=params, returns=returns, docstring=ast.get_docstring(node))


def _parse_class(node: ast.ClassDef) -> ClassMetadata:
    cm = ClassMetadata(name=node.name, lineno=getattr(node, 'lineno', 0), docstring=ast.get_docstring(node))
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            cm.methods.append(_parse_function(item, parent=node.name))
        elif isinstance(item, ast.Assign):
            for t in item.targets:
                if isinstance(t, ast.Name):
                    cm.attributes.append(t.id)
    return cm


def parse_file(filepath: str) -> FileMetadata:
    p = Path(filepath)
    src = p.read_text(encoding='utf-8')
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return FileMetadata(filepath=str(p), module_name=p.stem, source_code=src, syntax_valid=False)
    fm = FileMetadata(filepath=str(p), module_name=p.stem, source_code=src, syntax_valid=True)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fm.functions.append(_parse_function(node))
        elif isinstance(node, ast.ClassDef):
            fm.classes.append(_parse_class(node))
    return fm


def parse_directory(directory: str, recursive: bool = True) -> List[FileMetadata]:
    p = Path(directory)
    pattern = '**/*.py' if recursive else '*.py'
    files = list(p.glob(pattern))
    out = []
    for f in files:
        try:
            out.append(parse_file(str(f)))
        except Exception:
            continue
    return out


class PythonParser:
    """Compatibility wrapper providing parser as a class.

    Tests and older API import `PythonParser` from the package; provide
    a small wrapper that delegates to the module-level functions.
    """

    @staticmethod
    def parse_file(path: str) -> FileMetadata:
        return parse_file(path)

    @staticmethod
    def parse_directory(path: str, recursive: bool = True) -> List[FileMetadata]:
        return parse_directory(path, recursive)

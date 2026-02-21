"""Unit tests for docstring generator."""

import pytest
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from docstring_generator import (
    parse_file,
    DocstringGenerator,
    DocstringValidator,
    ErrorDetector,
    DocstringStyle,
    FunctionMetadata,
    Parameter,
)


@pytest.fixture
def sample_python_file():
    """Create a sample Python file for testing."""
    code = '''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def incomplete_function(x, y):
    return x * y


class Calculator:
    """A simple calculator."""
    
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        return f.name


class TestParser:
    """Tests for the parser module."""
    
    def test_parse_file_basic(self, sample_python_file):
        """Test basic file parsing."""
        file_metadata = parse_file(sample_python_file)
        
        assert file_metadata.syntax_valid
        assert len(file_metadata.functions) == 2
        assert len(file_metadata.classes) == 1
    
    def test_parse_function_metadata(self, sample_python_file):
        """Test function metadata extraction."""
        file_metadata = parse_file(sample_python_file)
        
        add_func = next(f for f in file_metadata.functions if f.name == "add")
        assert add_func.name == "add"
        assert len(add_func.parameters) == 2
        assert add_func.parameters[0].name == "a"
        assert add_func.parameters[0].type_hint == "int"
        assert add_func.returns is not None
        assert add_func.returns.type_hint == "int"
    
    def test_parse_class_metadata(self, sample_python_file):
        """Test class metadata extraction."""
        file_metadata = parse_file(sample_python_file)
        
        calc_class = next(c for c in file_metadata.classes if c.name == "Calculator")
        assert calc_class.name == "Calculator"
        assert len(calc_class.methods) == 2
        assert any(m.name == "multiply" for m in calc_class.methods)


class TestDocstringGenerator:
    """Tests for the generator module."""
    
    def test_generate_google_style(self, sample_python_file):
        """Test Google style generation."""
        file_metadata = parse_file(sample_python_file)
        func = file_metadata.functions[0]
        
        gen = DocstringGenerator(style="google")
        docstring = gen.generate_for_function(func)
        
        assert docstring.style == DocstringStyle.GOOGLE
        assert "Args:" in docstring.content
        assert "Returns:" in docstring.content
        assert docstring.quality_score > 0.0
    
    def test_generate_numpy_style(self, sample_python_file):
        """Test NumPy style generation."""
        file_metadata = parse_file(sample_python_file)
        func = file_metadata.functions[0]
        
        gen = DocstringGenerator(style="numpy")
        docstring = gen.generate_for_function(func)
        
        assert docstring.style == DocstringStyle.NUMPY
        assert "Parameters" in docstring.content
        assert "Returns" in docstring.content
    
    def test_generate_rest_style(self, sample_python_file):
        """Test reStructuredText style generation."""
        file_metadata = parse_file(sample_python_file)
        func = file_metadata.functions[0]
        
        gen = DocstringGenerator(style="rest")
        docstring = gen.generate_for_function(func)
        
        assert docstring.style == DocstringStyle.REST
        assert ":param" in docstring.content
        assert ":return" in docstring.content
    
    def test_quality_score(self, sample_python_file):
        """Test quality score calculation."""
        file_metadata = parse_file(sample_python_file)
        func = file_metadata.functions[0]
        
        gen = DocstringGenerator(style="google")
        docstring = gen.generate_for_function(func)
        
        assert 0.0 <= docstring.quality_score <= 1.0


class TestValidator:
    """Tests for the validator module."""
    
    def test_validate_valid_docstring(self):
        """Test validation of a valid docstring."""
        func_meta = FunctionMetadata(
            name="test_func",
            type="function",
            parameters=[Parameter(name="x", type_hint="int")],
        )
        docstring = """Test function.
        
        A longer description here.
        
        Args:
            x (int): Input value.
        
        Returns:
            int: The result.
        """
        
        validator = DocstringValidator()
        result = validator.validate_function(func_meta, docstring)
        
        # Should have some validation results
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'score')
    
    def test_validate_missing_docstring(self):
        """Test validation of missing docstring."""
        func_meta = FunctionMetadata(
            name="test_func",
            type="function",
        )
        
        validator = DocstringValidator()
        result = validator.validate_function(func_meta, "")
        
        assert not result.is_valid
        assert len(result.errors) > 0
    
    def test_quality_score_calculation(self):
        """Test docstring quality score."""
        func_meta = FunctionMetadata(
            name="test_func",
            type="function",
            parameters=[Parameter(name="x", type_hint="int")],
        )
        docstring = "Test." * 20  # Make it longer
        
        validator = DocstringValidator()
        result = validator.validate_function(func_meta, docstring)
        
        assert result.score >= 0.0
        assert result.score <= 1.0


class TestErrorDetector:
    """Tests for the error detector module."""
    
    def test_missing_type_hints(self, sample_python_file):
        """Test detection of missing type hints."""
        file_metadata = parse_file(sample_python_file)
        
        detector = ErrorDetector(file_metadata)
        issues = detector.detect_all()
        
        # Should detect missing type hints in 'incomplete_function'
        type_hint_issues = [i for i in issues if i.issue_type == "missing_type_hint"]
        assert len(type_hint_issues) > 0
    
    def test_syntax_error_detection(self):
        """Test syntax error detection."""
        code = "def broken(\n    x: int\n"  # Incomplete function
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            
            try:
                file_metadata = parse_file(f.name)
                assert not file_metadata.syntax_valid
            finally:
                # Close the file first on Windows so unlink succeeds
                try:
                    f.close()
                except Exception:
                    pass
                Path(f.name).unlink(missing_ok=True)


class TestParameterModel:
    """Tests for Parameter model."""
    
    def test_parameter_creation(self):
        """Test parameter creation."""
        param = Parameter(
            name="test_param",
            type_hint="str",
            default_value="default",
        )
        
        assert param.name == "test_param"
        assert param.type_hint == "str"
        assert param.default_value == "default"
    
    def test_parameter_validation(self):
        """Test parameter validation."""
        with pytest.raises(ValueError):
            Parameter(name="")


class TestFunctionMetadataModel:
    """Tests for FunctionMetadata model."""
    
    def test_function_metadata_creation(self):
        """Test function metadata creation."""
        func = FunctionMetadata(
            name="test_func",
            type="function",
            parameters=[
                Parameter(name="x", type_hint="int"),
                Parameter(name="y", type_hint="int"),
            ],
        )
        
        assert func.name == "test_func"
        assert len(func.parameters) == 2
    
    def test_function_summary(self):
        """Test function summary generation."""
        func = FunctionMetadata(
            name="test_func",
            type="function",
        )
        
        summary = func.summary()
        assert "test_func" in summary


class TestIntegration:
    """Integration tests."""
    
    def test_full_pipeline(self, sample_python_file):
        """Test complete pipeline: parse -> generate -> validate."""
        # Parse
        file_metadata = parse_file(sample_python_file)
        assert file_metadata.syntax_valid
        
        # Generate
        gen = DocstringGenerator(style="google")
        
        for func in file_metadata.functions:
            docstring = gen.generate_for_function(func)
            assert docstring.content
            assert docstring.quality_score >= 0.0
            
            # Validate
            validator = DocstringValidator()
            result = validator.validate_function(func, docstring.content)
            assert hasattr(result, 'is_valid')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

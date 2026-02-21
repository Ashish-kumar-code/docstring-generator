"""Configuration template for docstring generator."""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration management for docstring generator."""
    
    # Default configuration
    DEFAULTS: Dict[str, Any] = {
        "docstring_style": "google",
        "validate_pep257": True,
        "generate_inline_comments": False,
        "include_type_hints": True,
        "max_line_length": 79,
        "include_examples": True,
        "skip_private": False,
        "skip_special": False,
        "summary_required": True,
        "log_level": "INFO",
        "output_format": "python",  # python, markdown, html, json
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to JSON config file (optional)
        """
        self.config = self.DEFAULTS.copy()
        
        if config_file and Path(config_file).exists():
            self.load_from_file(config_file)
    
    def load_from_file(self, filepath: str) -> None:
        """Load configuration from JSON file."""
        try:
            with open(filepath, 'r') as f:
                user_config = json.load(f)
                self.config.update(user_config)
        except Exception as e:
            raise ValueError(f"Error loading config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
    
    def save_to_file(self, filepath: str) -> None:
        """Save configuration to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def __repr__(self) -> str:
        """Configuration string representation."""
        return f"Config({json.dumps(self.config, indent=2)})"


# Example configuration files
EXAMPLE_CONFIG_GOOGLE = {
    "docstring_style": "google",
    "validate_pep257": True,
    "generate_inline_comments": True,
    "include_type_hints": True,
    "max_line_length": 79,
    "summary_required": True,
}

EXAMPLE_CONFIG_NUMPY = {
    "docstring_style": "numpy",
    "validate_pep257": True,
    "generate_inline_comments": False,
    "include_type_hints": True,
    "max_line_length": 88,
}

EXAMPLE_CONFIG_REST = {
    "docstring_style": "rest",
    "validate_pep257": True,
    "generate_inline_comments": False,
    "include_type_hints": True,
}


def create_config_template(style: str = "google", output_file: str = ".docstring-config.json") -> None:
    """
    Create a configuration template.
    
    Args:
        style: Docstring style (google, numpy, rest)
        output_file: Output file path
    """
    if style == "numpy":
        config = EXAMPLE_CONFIG_NUMPY
    elif style == "rest":
        config = EXAMPLE_CONFIG_REST
    else:
        config = EXAMPLE_CONFIG_GOOGLE
    
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Configuration template created: {output_file}")


if __name__ == "__main__":
    # Example: Create configs
    create_config_template("google", "config/google-config.json")
    create_config_template("numpy", "config/numpy-config.json")
    create_config_template("rest", "config/rest-config.json")

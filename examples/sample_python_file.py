"""Example Python module for docstring generator testing."""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class Person:
    """A person with basic information."""
    
    name: str
    age: int
    email: Optional[str] = None


def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def parse_json_file(filepath: str) -> Dict[str, Any]:
    """Parse a JSON file and return the data."""
    with open(filepath, 'r') as f:
        return json.load(f)


class DataProcessor:
    """Process and transform data from various sources."""
    
    def __init__(self, source: str) -> None:
        """Initialize the processor with a data source."""
        self.source = source
        self.data = None
    
    def load_data(self) -> None:
        """Load data from the configured source."""
        self.data = parse_json_file(self.source)
    
    def filter_data(self, key: str, value: Any) -> List[Dict[str, Any]]:
        """Filter data by a key-value pair."""
        if not self.data:
            return []
        
        results = [item for item in self.data if item.get(key) == value]
        return results
    
    def transform_data(self, transformer) -> List[Dict[str, Any]]:
        """Apply a transformation function to the data."""
        if not self.data:
            return []
        
        return [transformer(item) for item in self.data]
    
    @property
    def shape(self) -> tuple:
        """Get the shape of the data (rows, columns)."""
        if not self.data:
            return (0, 0)
        
        if isinstance(self.data, list) and self.data:
            return (len(self.data), len(self.data[0]))
        
        return (0, 0)


class ConfigManager:
    """Manage application configuration."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
        return cls._instance
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def load_from_file(self, filepath: str) -> None:
        """Load configuration from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {filepath}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {filepath}")


def process_items(items: List[str]) -> None:
    """Process a list of items with error handling."""
    for item in items:
        try:
            # Simulate processing
            result = item.upper()
            print(f"Processed: {result}")
        except AttributeError as e:
            print(f"Error processing item: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def nested_comprehension(matrix: List[List[int]]) -> List[int]:
    """Flatten a 2D matrix using nested comprehension."""
    return [num for row in matrix for num in row]


def filtered_dict_comprehension(data: Dict[str, int], threshold: int) -> Dict[str, int]:
    """Filter a dictionary by value using comprehension."""
    return {k: v for k, v in data.items() if v > threshold}


def apply_operation(items: List[int], operation) -> List[int]:
    """Apply an operation to each item using lambda."""
    return list(map(operation, items))


def sort_persons(persons: List[Person]) -> List[Person]:
    """Sort persons by age using lambda."""
    return sorted(persons, key=lambda p: p.age)


class ResourceManager:
    """Manage resources using context managers."""
    
    def __init__(self, resource_name: str) -> None:
        """Initialize with a resource name."""
        self.resource_name = resource_name
        self.is_open = False
    
    def __enter__(self):
        """Enter context manager."""
        print(f"Opening resource: {self.resource_name}")
        self.is_open = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and cleanup."""
        print(f"Closing resource: {self.resource_name}")
        self.is_open = False
        return False
    
    def read(self) -> str:
        """Read from the resource."""
        if not self.is_open:
            raise RuntimeError("Resource is not open")
        return f"Data from {self.resource_name}"


def retry_operation(max_retries: int = 3):
    """Decorator to retry a function on failure."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
            return None
        return wrapper
    return decorator


@retry_operation(max_retries=2)
def unstable_operation():
    """An operation that might fail."""
    import random
    if random.random() < 0.5:
        raise RuntimeError("Operation failed")
    return "Success"

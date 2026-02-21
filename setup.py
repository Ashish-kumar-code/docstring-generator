"""Setup configuration for docstring_generator package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docstring-generator",
    version="0.1.0",
    author="Ashish Kumar",
    description="Automated Python docstring generator with AST parsing and multiple style support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ashish-kumar-code/docstring-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "docstring-gen=docstring_generator.cli:main",
        ],
    },
)

"""Command-line interface for docstring generator."""

import click
import logging
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.panel import Panel

from . import (
    parse_file,
    parse_directory,
    DocstringGenerator,
    BatchDocstringGenerator,
    DocstringValidator,
    ErrorDetector,
    DocstringInserter,
    DiffGenerator,
)

logger = logging.getLogger(__name__)
console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
def cli(verbose: bool) -> None:
    """Python Docstring Generator - Generate and validate docstrings."""
    setup_logging(verbose)


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "--style",
    default="google",
    type=click.Choice(["google", "numpy", "rest"]),
    help="Docstring style",
)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def analyze(filepath: str, style: str, verbose: bool) -> None:
    """Analyze a Python file and extract metadata."""
    try:
        console.print(f"\n[bold cyan]Analyzing: {filepath}[/bold cyan]")
        
        file_metadata = parse_file(filepath)
        
        if not file_metadata.syntax_valid:
            console.print("[bold red]✗ File has syntax errors[/bold red]")
            return
        
        # Display results
        console.print(f"\n[bold green]Module:[/bold green] {file_metadata.module_name}")
        console.print(f"[bold green]Functions:[/bold green] {len(file_metadata.functions)}")
        console.print(f"[bold green]Classes:[/bold green] {len(file_metadata.classes)}")
        
        # Functions table
        if file_metadata.functions:
            console.print("\n[bold]Functions:[/bold]")
            table = Table(title="Functions")
            table.add_column("Name", style="cyan")
            table.add_column("Parents", style="magenta")
            table.add_column("Has Docstring", style="green")
            table.add_column("Parameters", style="yellow")
            
            for func in file_metadata.functions:
                table.add_row(
                    func.name,
                    "Top-level",
                    "✓" if func.docstring else "✗",
                    str(len(func.parameters)),
                )
            console.print(table)
        
        # Classes table
        if file_metadata.classes:
            console.print("\n[bold]Classes:[/bold]")
            table = Table(title="Classes")
            table.add_column("Name", style="cyan")
            table.add_column("Has Docstring", style="green")
            table.add_column("Methods", style="yellow")
            table.add_column("Attributes", style="magenta")
            
            for cls in file_metadata.classes:
                table.add_row(
                    cls.name,
                    "✓" if cls.docstring else "✗",
                    str(len(cls.methods)),
                    str(len(cls.attributes)),
                )
            console.print(table)
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if verbose:
            raise


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "--style",
    default="google",
    type=click.Choice(["google", "numpy", "rest"]),
    help="Docstring style",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (optional)",
)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def generate(filepath: str, style: str, output: Optional[str], verbose: bool) -> None:
    """Generate docstrings for a Python file."""
    try:
        console.print(f"\n[bold cyan]Processing: {filepath}[/bold cyan]")
        
        file_metadata = parse_file(filepath)
        
        if not file_metadata.syntax_valid:
            console.print("[bold red]✗ File has syntax errors[/bold red]")
            return
        
        # Generate docstrings
        batch_generator = BatchDocstringGenerator(style)
        docstrings = batch_generator.generate_all(file_metadata)
        
        console.print(f"[green]✓ Generated {len(docstrings)} docstring(s)[/green]")
        
        # Read original file
        with open(filepath, "r") as f:
            original_code = f.read()
        
        # Insert docstrings
        inserter = DocstringInserter(original_code)
        enhanced_code = inserter.insert_docstrings(docstrings)
        
        # Generate diff
        diff_gen = DiffGenerator(original_code, enhanced_code)
        stats = diff_gen.get_stats()
        
        console.print(f"\n[bold]Changes:[/bold]")
        console.print(f"  Lines added: {stats['lines_added']}")
        console.print(f"  Lines removed: {stats['lines_removed']}")
        console.print(f"  Total changes: {stats['total_changes']}")
        
        # Save output if specified
        if output:
            with open(output, "w") as f:
                f.write(enhanced_code)
            console.print(f"\n[green]✓ Saved to: {output}[/green]")
        else:
            console.print("\n[bold]Enhanced code preview:[/bold]")
            console.print(Panel(enhanced_code[:500] + "..." if len(enhanced_code) > 500 else enhanced_code))
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if verbose:
            raise


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def validate(filepath: str, verbose: bool) -> None:
    """Validate docstrings in a Python file."""
    try:
        console.print(f"\n[bold cyan]Validating: {filepath}[/bold cyan]")
        
        file_metadata = parse_file(filepath)
        
        if not file_metadata.syntax_valid:
            console.print("[bold red]✗ File has syntax errors[/bold red]")
            return
        
        validator = DocstringValidator()
        
        # Validate functions and classes
        table = Table(title="Validation Results")
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Score", style="yellow")
        table.add_column("Issues", style="red")
        
        for func in file_metadata.functions:
            if func.docstring:
                result = validator.validate_function(func, func.docstring)
                status = "✓ Valid" if result.is_valid else "✗ Invalid"
                issues = len(result.errors) + len(result.warnings)
                table.add_row(
                    func.name,
                    status,
                    f"{result.score:.1%}",
                    str(issues),
                )
        
        for cls in file_metadata.classes:
            if cls.docstring:
                result = validator.validate_class(cls, cls.docstring)
                status = "✓ Valid" if result.is_valid else "✗ Invalid"
                issues = len(result.errors) + len(result.warnings)
                table.add_row(
                    cls.name,
                    status,
                    f"{result.score:.1%}",
                    str(issues),
                )
        
        console.print(table)
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if verbose:
            raise


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def check(filepath: str, verbose: bool) -> None:
    """Check for code issues (syntax errors, missing type hints, unused imports)."""
    try:
        console.print(f"\n[bold cyan]Checking: {filepath}[/bold cyan]")
        
        file_metadata = parse_file(filepath)
        
        error_detector = ErrorDetector(file_metadata)
        issues = error_detector.detect_all()
        
        if not issues:
            console.print("[green]✓ No issues detected[/green]")
            return
        
        # Group by severity
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]
        info = [i for i in issues if i.severity == "info"]
        
        table = Table(title="Code Issues")
        table.add_column("Severity", style="magenta")
        table.add_column("Issue Type", style="cyan")
        table.add_column("Message", style="yellow")
        table.add_column("Line", style="green")
        
        for issue in errors + warnings + info:
            severity_style = "red" if issue.severity == "error" else "yellow"
            table.add_row(
                f"[{severity_style}]{issue.severity.upper()}[/{severity_style}]",
                issue.issue_type,
                issue.message,
                str(issue.line_number) if issue.line_number else "-",
            )
        
        console.print(table)
        console.print(f"\n[red]Errors: {len(errors)}[/red]")
        console.print(f"[yellow]Warnings: {len(warnings)}[/yellow]")
        console.print(f"[blue]Info: {len(info)}[/blue]")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if verbose:
            raise


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option(
    "--style",
    default="google",
    type=click.Choice(["google", "numpy", "rest"]),
    help="Docstring style",
)
@click.option("--recursive", "-r", is_flag=True, help="Recursive directory scan")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def batch(directory: str, style: str, recursive: bool, verbose: bool) -> None:
    """Batch process multiple Python files in a directory."""
    try:
        console.print(f"\n[bold cyan]Batch processing: {directory}[/bold cyan]")
        
        files = parse_directory(directory, recursive=recursive)
        
        console.print(f"[green]✓ Found {len(files)} Python file(s)[/green]")
        
        total_functions = sum(f.total_functions() for f in files)
        total_missing = sum(f.missing_docstrings() for f in files)
        
        console.print(f"Total functions/methods: {total_functions}")
        console.print(f"Missing docstrings: {total_missing}")
        
        # Process each file
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Processing...",
                total=len(files),
            )
            
            for file_meta in files:
                generator = BatchDocstringGenerator(style)
                docstrings = generator.generate_all(file_meta)
                progress.update(task, advance=1)
        
        console.print(f"\n[green]✓ Batch processing complete[/green]")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if verbose:
            raise


def main() -> None:
    """Entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()

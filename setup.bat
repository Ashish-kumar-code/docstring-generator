@echo off
REM Setup script for Python Docstring Generator (Windows)

echo 📚 Python Docstring Generator - Setup Script
echo ================================================
echo.

REM Check Python version
echo 🐍 Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" || (
    echo ❌ Python 3.11+ is required
    exit /b 1
)

REM Install dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed

REM Install package in development mode
echo.
echo 📦 Installing docstring_generator in development mode...
pip install -e .
if errorlevel 1 (
    echo ❌ Failed to install package
    exit /b 1
)
echo ✓ Development installation complete

REM Setup pre-commit hook (Git)
echo.
echo 🔧 Setting up pre-commit hook...

if exist ".git" (
    if not exist ".git\hooks" mkdir ".git\hooks"
    
    if exist "config\pre-commit" (
        copy /Y "config\pre-commit" ".git\hooks\pre-commit"
        echo ✓ Pre-commit hook installed
    ) else (
        echo ⚠️  config\pre-commit not found, skipping pre-commit setup
    )
) else (
    echo ⚠️  Not a git repository, skipping pre-commit hook setup
)

REM Run tests
echo.
echo 🧪 Running tests...
pytest tests/ -v --tb=short 2>nul
if errorlevel 1 (
    echo ⚠️  Some tests failed or pytest not found
)

REM Summary
echo.
echo ================================================
echo ✅ Setup complete!
echo.
echo Next steps:
echo.
echo 1. Start Streamlit dashboard:
echo    streamlit run app.py
echo.
echo 2. Or use the CLI:
echo    python -m docstring_generator.cli analyze examples\sample_python_file.py
echo.
echo 3. Generate docstrings for a file:
echo    python -m docstring_generator.cli generate examples\sample_python_file.py -o examples\enhanced.py
echo.
echo 4. View all commands:
echo    python -m docstring_generator.cli --help
echo.
echo Happy coding! 🚀

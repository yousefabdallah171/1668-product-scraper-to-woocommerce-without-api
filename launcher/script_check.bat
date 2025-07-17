@echo off
title 1688 Product Scraper - Smart Launcher
echo.
echo ========================================
echo   1688 Product Scraper - Smart Launcher
echo   Developed by Rakmyat
echo ========================================
echo.
echo 🚀 Smart Features:
echo • Automatic system check on first run
echo • Dependency installation
echo • File validation
echo • Fast launch on subsequent runs
echo • Professional GUI with all features
echo.
echo Starting Smart Launcher...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Launch the smart launcher
python "Smart_Launcher.py"

if errorlevel 1 (
    echo.
    echo An error occurred while running the smart launcher.
    echo Please check the error messages above.
    pause
)

echo.
echo Thank you for using 1688 Product Scraper!
pause 
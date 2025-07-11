@echo off
title 1688 Product Scraper - Professional Launcher
echo.
echo ========================================
echo   1688 Product Scraper - Professional
echo   Developed by Rakmyat
echo ========================================
echo.
echo 🚀 Professional Features:
echo • Advanced Settings Panel
echo • Real-time Progress Tracking
echo • Live CSV Results Preview
echo • Multi-language Support
echo • Product Image Preview
echo • Comprehensive Logging
echo • URL Validation & Error Handling
echo • Organized Output with Timestamps
echo • WooCommerce Ready CSV Export
echo.
echo Starting Professional GUI...
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

REM Check if required files exist
if not exist "professional_gui.py" (
    echo ERROR: professional_gui.py not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

REM Install required packages if needed
echo Checking dependencies...
pip install -r requirements.txt >nul 2>&1

REM Launch the professional GUI
echo Launching Professional GUI...
python professional_gui.py

REM If GUI exits with error, show message
if errorlevel 1 (
    echo.
    echo An error occurred while running the scraper.
    echo Please check the logs for more information.
    pause
)

echo.
echo Thank you for using 1688 Product Scraper Professional!
pause 
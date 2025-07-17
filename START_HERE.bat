@echo off
cd /d "%~dp0"
title 1688 Product Scraper - Main Launcher
echo.
echo ========================================
echo   1688 Product Scraper - Main Launcher
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Run system check first (fast mode)
echo.
echo 🔍 Running system check...
python src/system_check.py
if errorlevel 1 (
    echo.
    echo ⚠️ System check found issues. Attempting to fix...
    echo.
    python src/system_check.py
)

echo.
echo 🚀 Starting main launcher...
python START_HERE.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    echo Please check the error messages above
    pause
) 
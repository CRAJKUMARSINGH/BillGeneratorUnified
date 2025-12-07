@echo off
title Customize Title from Input Files

echo ==========================================
echo   CUSTOMIZE TITLE FROM INPUT FILES
echo ==========================================

echo.
echo This script will extract title data from your Excel input files
echo and update the title configuration for document generation.
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install pandas openpyxl
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo Running title customization script...
python customize_title_from_input.py

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Title data extracted and configuration updated!
    echo Check the OUTPUT_FILES folder for extracted title data.
    echo The title_config.json file has been updated with data from your input files.
) else (
    echo.
    echo ERROR: Failed to customize title from input files
)

echo.
pause
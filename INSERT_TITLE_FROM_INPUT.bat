@echo off
setlocal enabledelayedexpansion
title Insert Title Data from Input Files

echo ==========================================
echo   INSERT TITLE DATA FROM INPUT FILES
echo ==========================================

echo.
echo This script will insert title data from Excel input files into the title.jpeg image.
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
    pip install pandas openpyxl Pillow
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo Running title insertion script...
python insert_title_from_input.py

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Title data inserted from input files!
    echo Check the ATTACHED_ASSETS folder for the generated images.
) else (
    echo.
    echo ERROR: Failed to insert title data from input files
)

echo.
pause
@echo off
setlocal enabledelayedexpansion
title Process All Titles from Input Files

echo ==========================================
echo   PROCESS ALL TITLES FROM INPUT FILES
echo ==========================================

echo.
echo This script will process all Excel files in the TEST_INPUT_FILES folder
echo and generate customized title images for each one.
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

echo Processing all Excel files in TEST_INPUT_FILES folder...

REM Process each Excel file
set count=0
for %%f in (TEST_INPUT_FILES\*.xlsx) do (
    echo.
    echo Processing: %%~nxf
    python insert_title_into_image.py "%%f"
    if !errorlevel! equ 0 (
        set /a count+=1
    )
)

echo.
echo ==========================================
echo Process completed!
echo Successfully processed !count! files.
echo Check the current directory for the generated title images.
echo ==========================================
echo.

pause
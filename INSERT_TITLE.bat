@echo off
title Insert Title Data into Image

echo ==========================================
echo   INSERT TITLE DATA INTO IMAGE
echo ==========================================

echo.
echo This script will insert title data from your bill data into the title.jpeg image.
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
python -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install Pillow
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Pillow package
        pause
        exit /b 1
    )
)

echo Running title insertion script...
python insert_title_into_image.py

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Title data inserted into image!
    echo Check the ATTACHED_ASSETS folder for the modified image.
) else (
    echo.
    echo ERROR: Failed to insert title data into image
)

echo.
pause
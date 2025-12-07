@echo off
title Enhanced Download Center
color 0A

echo ======================================================
echo    Enhanced Download Center Application
echo ======================================================
echo.
echo This script will start the enhanced download center application
echo using Streamlit.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

REM Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Streamlit...
    pip install streamlit
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Streamlit
        pause
        exit /b 1
    )
)

echo Starting Enhanced Download Center...
echo.
echo Open your browser to http://localhost:8501 if it doesn't open automatically
echo.
echo Press CTRL+C to stop the application
echo.

REM Run the main application
streamlit run app_enhanced_download.py

pause
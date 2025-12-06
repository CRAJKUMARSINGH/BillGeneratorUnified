@echo off
REM Batch script to add macro to workbook with copied sheets
REM This ensures the macro works on any sheet, including copied ones

echo ======================================================================
echo ADD MACRO TO WORKBOOK - FOR COPIED SHEETS
echo ======================================================================
echo.

REM Check if file path is provided
if "%~1"=="" (
    echo Using default workbook: ATTACHED_ASSETS\english Note FINAL BILL NOTE SHEET_UPDATED.xlsm
    echo.
    echo You can also specify a file path:
    echo   ADD_MACRO_TO_COPIED_SHEETS.bat "path\to\your\file.xlsm"
    echo.
    python add_macro_to_any_workbook.py
) else (
    echo Processing file: %~1
    echo.
    python add_macro_to_any_workbook.py "%~1"
)

echo.
echo ======================================================================
pause


@echo off
title Fix Excel Macros
color 0A

echo.
echo ========================================
echo   EXCEL MACRO PRESERVATION UTILITY
echo ========================================
echo.

echo 📋 This utility helps preserve macros when copying Excel files
echo.

echo 🔧 Solutions for macro preservation:
echo.
echo 1. Ensure files are saved in .xlsm format (macro-enabled)
echo 2. Use Excel's built-in copy functionality
echo 3. Check macro security settings
echo 4. Verify VBA project references
echo.

echo 📁 Checking current directory structure:
echo.
dir *.xl* 2>nul
echo.

echo 🛠️  Recommended workflow:
echo.
echo Step 1: Save your template as .xlsm (macro-enabled)
echo Step 2: Use Excel's "Move or Copy Sheet" feature
echo Step 3: Check Developer tab ^> Macros for functionality
echo Step 4: Test all macro buttons and functions
echo.

echo 💡 Tips for preserving macros:
echo.
echo • Always enable macros when opening workbooks
echo • Check File ^> Info ^> Protect Workbook settings
echo • Verify macro security level in Trust Center
echo • Use absolute references in macros when possible
echo • Test macros after copying sheets
echo.

echo 📞 For advanced macro transfer, run:
echo    python fix_macro_transfer.py
echo.

echo Press any key to continue...
pause >nul
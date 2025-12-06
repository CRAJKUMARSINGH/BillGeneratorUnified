EXCEL MACRO PRESERVATION SOLUTIONS
===============================

PROBLEM:
When copying sheets between Excel workbooks, macros may be lost or stop functioning properly.

SOLUTIONS PROVIDED:

1. FIX_MACROS.bat
   - Simple batch script with instructions for preserving macros
   - Lists best practices and troubleshooting tips
   - Easy to run on Windows systems

2. check_macros.ps1
   - PowerShell script for diagnosing macro issues
   - Checks for Excel installation and file formats
   - Provides detailed recommendations

3. fix_macro_transfer.py
   - Advanced Python solution using COM interface
   - Preserves macros when copying sheets between workbooks
   - Handles complex macro transfers programmatically

BEST PRACTICES:

1. Always save macro-containing workbooks as .xlsm (macro-enabled)
2. Use Excel's built-in "Move or Copy Sheet" feature rather than manual copying
3. Enable Developer tab to access macro tools
4. Test all macros after copying sheets
5. Check macro security settings in Trust Center

USAGE:

1. For simple guidance:
   Run FIX_MACROS.bat

2. For diagnostic information:
   Run check_macros.ps1 (in PowerShell)

3. For automated macro transfer:
   Run: python fix_macro_transfer.py

TROUBLESHOOTING:

Issue: Macros disappear after copying sheets
Solution: Use .xlsm format and Excel's native copy feature

Issue: Macro buttons don't work
Solution: Check macro security settings and reassign macros to buttons

Issue: Macro references broken
Solution: Update cell references and workbook paths in VBA code

CONTACT:
For additional help, consult Excel's Developer documentation or seek assistance from your IT department.
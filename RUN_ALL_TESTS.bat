@echo off
cls
echo ===============================================================================
echo    BILL GENERATOR UNIFIED - COMPREHENSIVE TEST SUITE
echo ===============================================================================
echo.
echo This script will run all tests for the BillGeneratorUnified application.
echo.
echo Tests include:
echo   - Enhanced PDF generation
echo   - Chrome headless PDF generation
echo   - Batch processing with Excel files
echo   - Launcher scripts
echo   - Dependency checks
echo.
echo Output will be saved to OUTPUT_FILES/ and test_output/ directories.
echo.
echo Press any key to continue...
pause >nul
echo.

python run_all_tests.py

echo.
echo ===============================================================================
echo    TEST EXECUTION COMPLETE
echo ===============================================================================
echo.
echo Check the console output above for detailed results.
echo Generated files can be found in:
echo   - OUTPUT_FILES/
echo   - test_output/
echo.
echo Press any key to exit...
pause >nul
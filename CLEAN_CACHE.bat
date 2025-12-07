@echo off
cls
echo ===============================================================================
echo    BILL GENERATOR UNIFIED - CACHE AND TEMPORARY FILES CLEANUP
echo ===============================================================================
echo.

REM Clean Python cache directories
echo Cleaning Python cache directories...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo ✅ Python cache directories cleaned

REM Clean .zip_cache directory
echo Cleaning .zip_cache directory...
if exist ".zip_cache" (
    rd /s /q ".zip_cache"
    echo ✅ .zip_cache directory cleaned
) else (
    echo ℹ️  .zip_cache directory not found
)

REM Clean Python compiled files
echo Cleaning Python compiled files...
del /s /q "*.pyc" >nul 2>&1
del /s /q "*.pyo" >nul 2>&1
del /s /q "*.pyd" >nul 2>&1
echo ✅ Python compiled files cleaned

REM Clean temporary files
echo Cleaning temporary files...
del /s /q "*.tmp" >nul 2>&1
del /s /q "*.temp" >nul 2>&1
del /s /q "~*" >nul 2>&1
del /s /q "*.bak" >nul 2>&1
echo ✅ Temporary files cleaned

REM Clean log files
echo Cleaning log files...
del /s /q "*.log" >nul 2>&1
echo ✅ Log files cleaned

REM Clean OS-specific files
echo Cleaning OS-specific files...
del /s /q ".DS_Store" >nul 2>&1
del /s /q "Thumbs.db" >nul 2>&1
del /s /q "desktop.ini" >nul 2>&1
echo ✅ OS-specific files cleaned

echo.
echo ===============================================================================
echo    CACHE AND TEMPORARY FILES CLEANUP COMPLETE
echo ===============================================================================
echo.
echo All cache directories and temporary files have been removed.
echo.
pause
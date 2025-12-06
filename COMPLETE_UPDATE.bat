@echo off
echo ====================================================================
echo COMPLETING XLSM FILE UPDATE
echo ====================================================================
echo.
echo Step 1: Closing any open Excel instances...
taskkill /F /IM excel.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo Step 2: Updating VBA macro...
python enable_vba_and_update.py

echo.
echo ====================================================================
echo UPDATE PROCESS COMPLETE
echo ====================================================================
echo.
echo Your files:
echo   - Updated file: ATTACHED_ASSETS\english Note FINAL BILL NOTE SHEET_UPDATED.xlsm
echo   - Backup file: ATTACHED_ASSETS\english Note FINAL BILL NOTE SHEET_backup_*.xlsm
echo   - VBA code: updated_macro.vba
echo   - Instructions: MANUAL_VBA_UPDATE_INSTRUCTIONS.md
echo.
echo If the macro was not updated automatically, please follow the
echo instructions in MANUAL_VBA_UPDATE_INSTRUCTIONS.md
echo.
pause

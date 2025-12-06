# Excel Macro Checker and Fixer
# PowerShell script to help diagnose and fix macro issues

Write-Host "========================================" -ForegroundColor Green
Write-Host "  EXCEL MACRO DIAGNOSTIC TOOL" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if Excel is installed
try {
    $excel = New-Object -ComObject Excel.Application
    Write-Host "[OK] Excel is installed (Version: $($excel.Version))" -ForegroundColor Green
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
} catch {
    Write-Host "[ERROR] Excel is not installed or not accessible" -ForegroundColor Red
    exit
}

# Check current directory for Excel files
Write-Host "`nChecking for Excel files..." -ForegroundColor Cyan
$excelFiles = Get-ChildItem -Path "." -Include "*.xls*", "*.xlsm" -Recurse

if ($excelFiles.Count -eq 0) {
    Write-Host "[INFO] No Excel files found in current directory" -ForegroundColor Yellow
} else {
    Write-Host "Found $($excelFiles.Count) Excel file(s):" -ForegroundColor Cyan
    foreach ($file in $excelFiles) {
        Write-Host "   - $($file.Name)" -ForegroundColor White
        # Check if file is macro-enabled
        if ($file.Extension -eq ".xlsm") {
            Write-Host "     [MACRO] Macro-enabled workbook" -ForegroundColor Green
        } elseif ($file.Extension -eq ".xlsx") {
            Write-Host "     [STANDARD] Standard workbook (no macros)" -ForegroundColor Yellow
        }
    }
}

# Check macro security settings
Write-Host "`nMacro security recommendations:" -ForegroundColor Cyan
Write-Host "   1. Enable macros when opening workbooks" -ForegroundColor White
Write-Host "   2. Set macro security to 'Disable all macros with notification'" -ForegroundColor White
Write-Host "   3. Add trusted locations in Excel Trust Center" -ForegroundColor White
Write-Host "   4. Check Developer tab is enabled" -ForegroundColor White

# Provide solutions
Write-Host "`nSolutions for macro preservation:" -ForegroundColor Cyan
Write-Host "   - Save templates as .xlsm (macro-enabled)" -ForegroundColor White
Write-Host "   - Use Excel's built-in 'Move or Copy Sheet' feature" -ForegroundColor White
Write-Host "   - Check macro references after copying sheets" -ForegroundColor White
Write-Host "   - Test all macro buttons and functions after transfer" -ForegroundColor White

Write-Host "`nFor automated macro transfer, run:" -ForegroundColor Cyan
Write-Host "   python fix_macro_transfer.py" -ForegroundColor White

Write-Host "`nDiagnostic complete!" -ForegroundColor Green
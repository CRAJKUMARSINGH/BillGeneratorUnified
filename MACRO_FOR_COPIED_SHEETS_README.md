# Macro Solution for Copied Sheets

## Problem
When you copy a sheet from the workbook to a new workbook, the VBA macro doesn't get copied with it. The macro is lost and doesn't function on the copied sheet.

## Solution
This tool automatically adds the `GenerateBillNotes` macro to any workbook, ensuring it works on **any sheet** (including copied sheets).

## Key Features
✅ **Works on ActiveSheet** - No hardcoded sheet names  
✅ **Works on copied sheets** - Each sheet can use the macro independently  
✅ **Automatic detection** - Updates existing macro or creates new one  
✅ **Easy to use** - Just run the script on any workbook  

## How to Use

### Method 1: Using Batch File (Easiest)
1. Double-click `ADD_MACRO_TO_COPIED_SHEETS.bat`
2. It will process the default workbook automatically
3. Or drag and drop your workbook file onto the batch file

### Method 2: Using Python Script
```bash
# For default workbook
python add_macro_to_any_workbook.py

# For specific workbook
python add_macro_to_any_workbook.py "path\to\your\file.xlsm"
```

### Method 3: For New Workbooks with Copied Sheets
1. Copy your sheet to a new workbook
2. Save the new workbook as `.xlsm` format (macro-enabled)
3. Run the script on the new workbook:
   ```bash
   python add_macro_to_any_workbook.py "new_workbook.xlsm"
   ```
4. The macro will now work on all sheets in that workbook!

## Using the Macro

After adding the macro to your workbook:

1. **Open the workbook** (enable macros if prompted)
2. **Click on any sheet** (including copied sheets)
3. **Press Alt+F8** to open the Macro dialog
4. **Select 'GenerateBillNotes'**
5. **Click 'Run'**
6. The macro will generate bill notes in **cell A42** of the active sheet

## Important Notes

### Excel Security Settings
If you get an error about "Trust access to VBA project object model":
1. Open Excel
2. Go to **File → Options → Trust Center**
3. Click **Trust Center Settings**
4. Go to **Macro Settings**
5. Check **"Trust access to the VBA project object model"**
6. Click OK and restart Excel
7. Run the script again

### File Format
- The macro requires `.xlsm` format (macro-enabled workbook)
- If your file is `.xlsx`, the script will automatically convert it to `.xlsm`

### Multiple Sheets
- Each sheet in the workbook can use the macro independently
- The macro always works on the **currently active sheet**
- Output goes to cell A42 of the active sheet

## Troubleshooting

### Macro not appearing after running script
- Make sure Excel is closed when running the script
- Check that the file is saved as `.xlsm` format
- Verify VBA access is trusted (see above)

### Macro runs but doesn't work on copied sheet
- The macro uses `ActiveSheet`, so it should work on any sheet
- Make sure you click on the sheet before running the macro
- Check that the sheet has the correct structure (cells C5, C13-C15, C18-C21, C29-C33)

### Error: "No active sheet found"
- Click on a sheet tab to make it active
- Don't run the macro when no sheet is selected

## Technical Details

The macro:
- Uses `ActiveSheet` instead of hardcoded sheet names
- Works on any worksheet in the workbook
- Generates bill notes based on data in specific cells
- Outputs to cell A42 with proper formatting
- Configures page setup for A4 portrait printing

## Files Included

- `add_macro_to_any_workbook.py` - Main Python script
- `ADD_MACRO_TO_COPIED_SHEETS.bat` - Easy-to-use batch file
- `updated_macro_corrected.vba` - VBA source code (for reference)

## Support

If you encounter issues:
1. Check the error messages in the console
2. Verify Excel security settings
3. Ensure the workbook structure matches expected format
4. Try running the script on a backup copy first


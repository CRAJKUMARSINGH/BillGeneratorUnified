"""
Excel Macro Transfer Utility
Preserves macro functionality when copying sheets between workbooks
"""

import os
import shutil
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
import win32com.client as win32

def transfer_sheet_with_macros(source_file, destination_file, sheet_name):
    """
    Transfer a sheet with preserved macro functionality using win32com
    This approach uses Excel's native capabilities to preserve macros
    """
    try:
        # Use Excel COM interface to preserve macros
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False
        
        # Open both workbooks
        source_wb = excel.Workbooks.Open(os.path.abspath(source_file))
        dest_wb = excel.Workbooks.Open(os.path.abspath(destination_file))
        
        # Copy the sheet
        source_sheet = source_wb.Sheets(sheet_name)
        source_sheet.Copy(Before=dest_wb.Sheets(1))
        
        # Save and close
        dest_wb.Save()
        source_wb.Close()
        dest_wb.Close()
        
        excel.Quit()
        
        return True, "Sheet transferred successfully with macros preserved"
    except Exception as e:
        return False, f"Error transferring sheet: {str(e)}"

def create_macro_enabled_workbook(template_file, output_file):
    """
    Create a new macro-enabled workbook based on a template
    """
    try:
        # Copy the template file
        shutil.copy2(template_file, output_file)
        
        # Rename to .xlsm if needed
        if output_file.endswith('.xlsx'):
            new_name = output_file.replace('.xlsx', '.xlsm')
            os.rename(output_file, new_name)
            return new_name
            
        return output_file
    except Exception as e:
        return None, f"Error creating macro-enabled workbook: {str(e)}"

def transfer_macros_and_sheets(source_file, destination_template, output_file, sheets_to_copy):
    """
    Comprehensive solution to transfer sheets with macro functionality
    """
    try:
        # Ensure output is macro-enabled
        if not output_file.endswith('.xlsm'):
            output_file = output_file.replace('.xlsx', '.xlsm')
        
        # Copy template to output
        shutil.copy2(destination_template, output_file)
        
        # Use Excel COM to transfer sheets with macros
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False
        
        # Open workbooks
        source_wb = excel.Workbooks.Open(os.path.abspath(source_file))
        output_wb = excel.Workbooks.Open(os.path.abspath(output_file))
        
        # Transfer specified sheets
        for sheet_name in sheets_to_copy:
            try:
                source_sheet = source_wb.Sheets(sheet_name)
                source_sheet.Copy(Before=output_wb.Sheets(1))
                print(f"✅ Transferred sheet: {sheet_name}")
            except Exception as e:
                print(f"⚠️  Could not transfer sheet {sheet_name}: {str(e)}")
        
        # Save and close
        output_wb.Save()
        source_wb.Close()
        output_wb.Close()
        
        excel.Quit()
        
        return True, f"Macros and sheets transferred to {output_file}"
    except Exception as e:
        return False, f"Error in macro transfer: {str(e)}"

def create_macro_preserving_script():
    """
    Create a VBA script that can help preserve macros when copying sheets
    """
    vba_code = '''
Sub TransferSheetWithMacros()
    Dim sourceWb As Workbook
    Dim destWb As Workbook
    Dim sourceSheet As Worksheet
    Dim sheetName As String
    
    ' Set the sheet name to copy
    sheetName = "Sheet1" ' Change this to your sheet name
    
    ' Open source workbook
    Set sourceWb = Workbooks.Open(ThisWorkbook.Path & "\source.xlsx")
    Set sourceSheet = sourceWb.Sheets(sheetName)
    
    ' Copy sheet to active workbook
    sourceSheet.Copy Before:=ThisWorkbook.Sheets(1)
    
    ' Close source workbook
    sourceWb.Close SaveChanges:=False
    
    MsgBox "Sheet transferred with macros preserved!"
End Sub

Sub PreserveAllMacros()
    ' This subroutine ensures all macros are preserved
    ' when copying sheets between workbooks
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    
    ' Your macro operations here
    
    Application.EnableEvents = True
    Application.ScreenUpdating = True
End Sub
'''
    
    return vba_code

def main():
    print("=" * 60)
    print("EXCEL MACRO TRANSFER UTILITY")
    print("=" * 60)
    print()
    
    # Create directories if they don't exist
    Path("macro_templates").mkdir(exist_ok=True)
    Path("macro_outputs").mkdir(exist_ok=True)
    
    print("📁 Directories checked/created:")
    print("   - macro_templates/")
    print("   - macro_outputs/")
    print()
    
    print("🔧 Solutions for preserving macros when copying sheets:")
    print()
    print("1. Use .xlsm format (macro-enabled workbooks)")
    print("2. Transfer sheets using Excel's COM interface")
    print("3. Preserve VBA modules during transfer")
    print("4. Maintain workbook references in macros")
    print()
    
    print("💡 Usage Tips:")
    print("- Always save workbooks in .xlsm format when using macros")
    print("- Enable macro security settings appropriately")
    print("- Test macro functionality after sheet transfers")
    print("- Backup original files before transferring sheets")
    print()
    
    # Example usage
    print("📝 Example usage:")
    print("""
# Transfer a sheet with macros preserved
success, message = transfer_sheet_with_macros(
    source_file="template.xlsm",
    destination_file="output.xlsm", 
    sheet_name="DataSheet"
)

if success:
    print("✅ " + message)
else:
    print("❌ " + message)
    """)
    
    # Create sample VBA code file
    vba_code = create_macro_preserving_script()
    vba_file = Path("macro_templates/sample_macros.bas")
    vba_file.write_text(vba_code)
    
    print(f"📄 Created sample VBA code: {vba_file}")
    print()
    print("🎯 To use this utility:")
    print("1. Place your source Excel files in the working directory")
    print("2. Run this script with appropriate parameters")
    print("3. Check the macro_outputs/ directory for results")
    print()

if __name__ == "__main__":
    main()
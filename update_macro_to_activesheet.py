"""
Update the VBA macro to work on ActiveSheet instead of hardcoded sheet name
"""
import win32com.client
import os
import shutil
from datetime import datetime

source_file = 'ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET.xlsm'
backup_file = f'ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_backup_activesheet_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsm'

print("="*70)
print("UPDATING MACRO TO WORK ON ANY SHEET")
print("="*70)

# Create backup
shutil.copy2(source_file, backup_file)
print(f"\n✓ Backup created: {backup_file}")

try:
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    
    # Open the file
    wb = xl.Workbooks.Open(os.path.abspath(source_file))
    
    # Read the updated VBA code
    with open('updated_macro_corrected.vba', 'r', encoding='utf-8') as f:
        vba_code = f.read()
    
    print("✓ Loaded updated VBA code")
    
    # Find and update the module
    module_found = False
    for component in wb.VBProject.VBComponents:
        if component.Type == 1:  # vbext_ct_StdModule
            code = component.CodeModule.Lines(1, component.CodeModule.CountOfLines)
            if "GenerateBillNotes" in code:
                print(f"✓ Found macro in module: {component.Name}")
                # Clear existing code
                component.CodeModule.DeleteLines(1, component.CodeModule.CountOfLines)
                # Add updated code
                component.CodeModule.AddFromString(vba_code)
                print(f"✓ Updated VBA code in module: {component.Name}")
                module_found = True
                break
    
    if not module_found:
        print("⚠ Module not found, creating new one")
        new_module = wb.VBProject.VBComponents.Add(1)
        new_module.Name = "BillNotesGenerator"
        new_module.CodeModule.AddFromString(vba_code)
        print(f"✓ Created new VBA module: BillNotesGenerator")
    
    # Save the file
    wb.Save()
    wb.Close(False)
    xl.Quit()
    
    print("\n" + "="*70)
    print("✅ MACRO UPDATE SUCCESSFUL!")
    print("="*70)
    print(f"\n✓ File updated: {source_file}")
    print(f"✓ Backup saved: {backup_file}")
    print("\n📋 Changes:")
    print("  ✓ Macro now works on ActiveSheet (any sheet)")
    print("  ✓ No longer hardcoded to 'BillChecklist'")
    print("\n📝 Usage:")
    print("  1. Copy the sheet to create multiple sheets")
    print("  2. Click on any sheet to make it active")
    print("  3. Press Alt+F8, select 'GenerateBillNotes', Run")
    print("  4. Macro will work on the currently active sheet")
    print("  5. Each sheet will have its own output in cell A42")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nPlease manually update the VBA code:")
    print("  1. Open the XLSM file")
    print("  2. Press Alt+F11")
    print("  3. Find the module with GenerateBillNotes")
    print("  4. Replace 'Set ws = ThisWorkbook.Sheets(SHEET_NAME)'")
    print("     with 'Set ws = ActiveSheet'")
    print("  5. Remove the 'Const SHEET_NAME' line")
    try:
        xl.Quit()
    except:
        pass

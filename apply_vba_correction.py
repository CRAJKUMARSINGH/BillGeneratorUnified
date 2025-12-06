"""
Apply VBA macro correction to the corrected XLSM file
"""
import win32com.client
import os
import time

print("="*70)
print("APPLYING VBA MACRO CORRECTION")
print("="*70)

try:
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    
    # Open the corrected file
    file_path = os.path.abspath('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_CORRECTED.xlsm')
    wb = xl.Workbooks.Open(file_path)
    
    # Read the corrected VBA code
    with open('updated_macro_corrected.vba', 'r', encoding='utf-8') as f:
        vba_code = f.read()
    
    print("\n✓ Loaded corrected VBA code")
    
    # Find the module containing GenerateBillNotes
    module_found = False
    for component in wb.VBProject.VBComponents:
        if component.Type == 1:  # vbext_ct_StdModule
            # Check if this module contains GenerateBillNotes
            code = component.CodeModule.Lines(1, component.CodeModule.CountOfLines)
            if "GenerateBillNotes" in code:
                print(f"✓ Found macro in module: {component.Name}")
                # Clear existing code
                component.CodeModule.DeleteLines(1, component.CodeModule.CountOfLines)
                # Add corrected code
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
    print("VBA MACRO CORRECTION COMPLETE")
    print("="*70)
    print("✓ Output cell updated: B44 → B43")
    print("✓ Extra item amount now reads from D23")
    print("✓ Row references updated (C24→C24, C25→C25 for shifted rows)")
    print(f"✓ File saved: {file_path}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nPlease manually update the VBA code using:")
    print("  1. Open the XLSM file")
    print("  2. Press Alt+F11")
    print("  3. Copy code from 'updated_macro_corrected.vba'")
    print("  4. Paste into the module")
    try:
        xl.Quit()
    except:
        pass

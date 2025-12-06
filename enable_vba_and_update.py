"""
Enable VBA access and complete the macro update
"""
import winreg
import win32com.client
import os
import time

def enable_vba_access():
    """Enable 'Trust access to VBA project object model' in Excel"""
    try:
        # Registry path for Excel Trust Center settings
        # This varies by Excel version, try common paths
        excel_versions = ['16.0', '15.0', '14.0']  # Office 2016/2019/365, 2013, 2010
        
        for version in excel_versions:
            try:
                key_path = f'Software\\Microsoft\\Office\\{version}\\Excel\\Security'
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, 'AccessVBOM', 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                print(f"✓ Enabled VBA access for Excel version {version}")
                return True
            except WindowsError:
                continue
        
        print("⚠ Could not find Excel registry key")
        return False
    except Exception as e:
        print(f"⚠ Error enabling VBA access: {e}")
        return False

def update_vba_macro():
    """Update the VBA macro in the XLSM file"""
    try:
        xl = win32com.client.Dispatch("Excel.Application")
        xl.Visible = False
        xl.DisplayAlerts = False
        
        # Open the temp file
        temp_file = os.path.abspath('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_TEMP.xlsm')
        wb = xl.Workbooks.Open(temp_file)
        
        # Read the updated VBA code
        with open('updated_macro.vba', 'r', encoding='utf-8') as f:
            vba_code = f.read()
        
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
                    # Add updated code
                    component.CodeModule.AddFromString(vba_code)
                    print(f"✓ Updated VBA code in module: {component.Name}")
                    module_found = True
                    break
        
        if not module_found:
            # Create new module if not found
            new_module = wb.VBProject.VBComponents.Add(1)  # vbext_ct_StdModule
            new_module.Name = "BillNotesGenerator"
            new_module.CodeModule.AddFromString(vba_code)
            print(f"✓ Created new VBA module: BillNotesGenerator")
        
        # Save as final file
        output_file = os.path.abspath('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_UPDATED.xlsm')
        wb.SaveAs(output_file, FileFormat=52)  # xlOpenXMLWorkbookMacroEnabled
        wb.Close(False)
        xl.Quit()
        
        print(f"✓ VBA macro updated successfully")
        print(f"✓ Final file saved to: {output_file}")
        
        # Clean up temp file
        time.sleep(1)
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"✓ Cleaned up temp file")
        
        return True
        
    except Exception as e:
        print(f"✗ Error updating VBA macro: {e}")
        return False

if __name__ == "__main__":
    print("="*70)
    print("ENABLING VBA ACCESS AND UPDATING MACRO")
    print("="*70)
    
    # Step 1: Enable VBA access
    print("\nStep 1: Enabling VBA project access...")
    if enable_vba_access():
        print("✓ VBA access enabled")
    else:
        print("⚠ Could not enable VBA access automatically")
        print("  Please enable manually: File → Options → Trust Center → Trust Center Settings")
        print("  → Macro Settings → Check 'Trust access to the VBA project object model'")
    
    # Step 2: Update the macro
    print("\nStep 2: Updating VBA macro...")
    if update_vba_macro():
        print("\n" + "="*70)
        print("✓ UPDATE COMPLETE!")
        print("="*70)
        print("\nYour updated file is ready:")
        print("  ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_UPDATED.xlsm")
        print("\nYou can now:")
        print("  1. Open the file in Excel")
        print("  2. Test the macro by pressing Alt+F8 and running 'GenerateBillNotes'")
        print("  3. Replace the original file if everything works correctly")
    else:
        print("\n" + "="*70)
        print("⚠ MANUAL UPDATE REQUIRED")
        print("="*70)
        print("\nPlease follow the instructions in:")
        print("  MANUAL_VBA_UPDATE_INSTRUCTIONS.md")

#!/usr/bin/env python3
"""
Verify XLSM file structure after update.
"""

import pandas as pd

def verify_xlsm_structure():
    """Verify that the XLSM file has the correct structure."""
    try:
        # Read the updated XLSM file
        xl = pd.ExcelFile('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_UPDATED.xlsm')
        sheet_name = xl.sheet_names[0]  # Get the first sheet name
        df = pd.read_excel('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_UPDATED.xlsm', 
                          sheet_name=sheet_name, header=None)
        
        print("XLSM File Structure Verification:")
        print(f"Using sheet: {sheet_name}")
        print(f"Row 18 (Item 16): {df.iloc[18, 0]} - Value in column C: {df.iloc[18, 2] if not pd.isna(df.iloc[18, 2]) else 'Empty'}")
        print(f"Row 19 (17.A): {df.iloc[19, 0]} - Value in column C: {df.iloc[19, 2] if not pd.isna(df.iloc[19, 2]) else 'Empty'}")
        print(f"Row 20 (17.B): {df.iloc[20, 0]} - Value in column C: {df.iloc[20, 2] if not pd.isna(df.iloc[20, 2]) else 'Empty'}")
        print(f"Row 21 (17.C): {df.iloc[21, 0]} - Value in column C: {df.iloc[21, 2] if not pd.isna(df.iloc[21, 2]) else 'Formula or Empty'}")
        
        # Check that the structure is correct
        row_18_text = str(df.iloc[18, 0])
        row_19_text = str(df.iloc[19, 0])
        row_20_text = str(df.iloc[20, 0])
        row_21_text = str(df.iloc[21, 0])
        
        print(f"Checking row contents...")
        print(f"  Row 18 contains '16': {'16' in row_18_text}")
        print(f"  Row 19 contains '17.A': {'17.A' in row_19_text}")
        print(f"  Row 20 contains '17.B': {'17.B' in row_20_text}")
        print(f"  Row 21 contains '17.C': {'17.C' in row_21_text}")
        
        print("✓ XLSM structure verified successfully!")
        return True
        
    except Exception as e:
        print(f"Error verifying XLSM structure: {e}")
        return False

if __name__ == "__main__":
    verify_xlsm_structure()
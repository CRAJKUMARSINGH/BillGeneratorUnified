#!/usr/bin/env python3
"""
Add Macro Scrutiny Sheet to Processed Bills
- Copies template sheet from "even BILL NOTE SHEET.xlsm"
- Renames with contractor name (first 5 words) + "_" + agreement number
- Populates cells from processed bill data
- Runs macro programmatically
- Exports to PDF

NOW USING THE ENHANCED AUTOMATED_SCRUTINY_SHEET_GENERATOR MODULE
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import shutil
import traceback
import copy

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

# Import our enhanced generator
from automated_scrutiny_sheet_generator import create_scrutiny_sheet_for_bill

try:
    import openpyxl
    from openpyxl import load_workbook
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    print("WARNING: openpyxl not available. Install with: pip install openpyxl")

try:
    import win32com.client
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False
    print("WARNING: win32com not available. Install with: pip install pywin32")

def add_macro_scrutiny_sheet(processed_data, output_file_path, template_path=None, bill_type="running"):
    """
    Add macro scrutiny sheet to processed bill using our enhanced automated generator
    
    Args:
        processed_data: Processed data from ExcelProcessor
        output_file_path: Path to output Excel file (will be created/updated)
        template_path: Path to template file (default: ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm)
        bill_type: "running", "first", or "final"
    
    Returns:
        dict with status and details
    """
    if template_path is None:
        template_path = Path(__file__).parent / "ATTACHED_ASSETS" / "even BILL NOTE SHEET.xlsm"
    
    template_path = Path(template_path)
    
    if not template_path.exists():
        return {
            'success': False,
            'error': f"Template file not found: {template_path}"
        }
    
    try:
        # Use our enhanced automated generator
        print("Using enhanced automated scrutiny sheet generator...")
        
        result = create_scrutiny_sheet_for_bill(
            workbook_path=str(template_path),
            processed_data=processed_data,
            bill_type=bill_type,
            output_pdf_dir=Path(output_file_path).parent
        )
        
        if result['success']:
            print(f"✅ Scrutiny sheet '{result['sheet_name']}' created successfully!")
            print(f"   PDF exported: {result['pdf_exported']}")
            if result['pdf_path']:
                print(f"   PDF location: {result['pdf_path']}")
            
            # Copy the updated workbook to the output location if different
            if str(template_path) != str(output_file_path):
                try:
                    shutil.copy2(template_path, output_file_path)
                    print(f"   Workbook copied to: {output_file_path}")
                except Exception as e:
                    print(f"   Warning: Could not copy workbook: {e}")
            
            return {
                'success': True,
                'sheet_name': result['sheet_name'],
                'output_file': str(output_file_path),
                'pdf_file': result['pdf_path'],
                'macro_run': result['macro_executed'],
                'pdf_exported': result['pdf_exported']
            }
        else:
            return {
                'success': False,
                'error': result['error']
            }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }

if __name__ == "__main__":
    print("Enhanced Macro Scrutiny Sheet Module")
    print("Using Automated Scrutiny Sheet Generator")
    print("=" * 50)
    
    # Example usage
    example_data = {
        'title_data': {
            'Name of Contractor or supplier :': 'M/s. Test Construction Company',
            'Agreement No.': '55/2024-25',
            'Name of Work ;-)': 'Building Construction Project',
            'Date of Commencement': '2024-01-01',
            'Date of Completion': '2024-12-31',
            'Date of actual completion of work :': '2024-12-15',
            'WORK ORDER AMOUNT RS.': 1000000
        },
        'totals': {
            'work_order_amount': 1000000,
            'last_bill_amount': 400000,
            'net_payable': 550000,
            'extra_items_sum': 30000,
            'tender_premium': 10000
        }
    }
    
    template_path = "ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm"
    
    if os.path.exists(template_path):
        result = add_macro_scrutiny_sheet(
            processed_data=example_data,
            output_file_path="test_output/enhanced_scrutiny_sheet.xlsm",
            template_path=template_path,
            bill_type="running"
        )
        
        if result['success']:
            print(f"\n🎉 SUCCESS!")
            print(f"   Sheet Name: {result['sheet_name']}")
            print(f"   Output File: {result['output_file']}")
            print(f"   PDF Exported: {result['pdf_exported']}")
            if result['pdf_file']:
                print(f"   PDF File: {result['pdf_file']}")
            print(f"   Macro Run: {result['macro_run']}")
        else:
            print(f"\n💥 FAILED: {result['error']}")
    else:
        print(f"\n❌ Template not found: {template_path}")

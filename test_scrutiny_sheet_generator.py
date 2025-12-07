#!/usr/bin/env python3
"""
Test script for the Automated Scrutiny Sheet Generator
"""

import os
from pathlib import Path
from automated_scrutiny_sheet_generator import create_scrutiny_sheet_for_bill

def test_scrutiny_sheet_generation():
    """Test the scrutiny sheet generation functionality"""
    
    # Test data similar to what would come from bill processing
    test_processed_data = {
        'title_data': {
            'Name of Contractor or supplier :': 'M/s. Shree Krishna Builders Jaipur',
            'Agreement No.': '48/2024-25',
            'Name of Work ;-)': 'Plumbing Installation and MTC work at Govt. Nehru hostel Mansarovar, Sanganer, Jaipur',
            'Date of Commencement': '2024-01-15',
            'Date of Completion': '2024-12-15',
            'Date of actual completion of work :': '2024-12-10',
            'WORK ORDER AMOUNT RS.': 500000,
            'St. date of Start :': '2024-01-15',
            'St. date of completion :': '2024-12-15'
        },
        'totals': {
            'work_order_amount': 500000,
            'last_bill_amount': 200000,
            'net_payable': 250000,
            'extra_items_sum': 15000,
            'tender_premium': 5000
        }
    }
    
    # Path to template workbook
    workbook_path = "ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm"
    
    # Check if template exists
    if not os.path.exists(workbook_path):
        print(f"❌ Template workbook not found: {workbook_path}")
        print("Please ensure the template workbook exists in the ATTACHED_ASSETS folder.")
        return False
    
    # Create output directory
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    # Test different bill types
    bill_types = ["running", "first", "final"]
    
    for bill_type in bill_types:
        print(f"\nTesting {bill_type.upper()} bill type...")
        
        # Generate scrutiny sheet
        result = create_scrutiny_sheet_for_bill(
            workbook_path=workbook_path,
            processed_data=test_processed_data,
            bill_type=bill_type,
            output_pdf_dir=output_dir
        )
        
        if result['success']:
            print(f"✅ SUCCESS for {bill_type} bill!")
            print(f"   Sheet Name: {result['sheet_name']}")
            print(f"   Workbook: {result['workbook_path']}")
            print(f"   PDF Exported: {result['pdf_exported']}")
            if result['pdf_path']:
                print(f"   PDF Path: {result['pdf_path']}")
            print(f"   Macro Executed: {result['macro_executed']}")
        else:
            print(f"❌ FAILED for {bill_type} bill: {result['error']}")
    
    return True

if __name__ == "__main__":
    print("Testing Automated Scrutiny Sheet Generator")
    print("=" * 50)
    
    try:
        success = test_scrutiny_sheet_generation()
        if success:
            print("\n🎉 All tests completed!")
        else:
            print("\n💥 Tests failed!")
    except Exception as e:
        print(f"\n💥 Test execution failed with error: {e}")
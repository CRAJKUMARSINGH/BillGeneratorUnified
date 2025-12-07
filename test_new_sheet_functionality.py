import sys
import os
sys.path.append('.')

from core.processors.batch_processor import add_bill_summary_sheet
from core.processors.excel_processor import ExcelProcessor
import json

# Test the new functionality
def test_sheet_creation():
    # Use one of the test files
    test_file = "TEST_INPUT_FILES/0511-N-extra.xlsx"
    
    if not os.path.exists(test_file):
        print(f"Test file {test_file} not found")
        return
    
    # Process the file to get processed_data
    excel_processor = ExcelProcessor()
    
    # Open the file
    with open(test_file, 'rb') as f:
        processed_data = excel_processor.process_excel(f)
    
    # Print some info about the processed data
    print("Processed data keys:", list(processed_data.keys()))
    print("Title data keys:", list(processed_data.get('title_data', {}).keys()))
    
    # Test adding the summary sheet
    print("\nTesting sheet creation...")
    success = add_bill_summary_sheet(test_file, processed_data)
    
    if success:
        print("Sheet creation successful!")
    else:
        print("Sheet creation failed!")

if __name__ == "__main__":
    test_sheet_creation()
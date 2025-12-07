import sys
import os
sys.path.append('.')

from core.processors.excel_processor import ExcelProcessor

# Debug the title data
def debug_title_data():
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
    
    # Print the title data
    title_data = processed_data.get('title_data', {})
    print("Title data:")
    for key, value in title_data.items():
        print(f"  '{key}': '{value}'")

if __name__ == "__main__":
    debug_title_data()
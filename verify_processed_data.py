#!/usr/bin/env python3
"""
Verify processed data from Excel files
"""

from core.processors.excel_processor import ExcelProcessor
import json

def verify_data():
    """Verify data from a test file"""
    processor = ExcelProcessor()
    
    # Test with one file
    with open('TEST_INPUT_FILES/0511-N-extra.xlsx', 'rb') as f:
        data = processor.process_excel(f)
    
    print("=== TITLE DATA ===")
    title_data = data.get('title_data', {})
    for key, value in title_data.items():
        print(f"{key}: {value}")
    
    print("\n=== WORK ORDER DATA ===")
    work_order_data = data.get('work_order_data', [])
    print(f"Type: {type(work_order_data)}")
    if hasattr(work_order_data, '__len__'):
        print(f"Length: {len(work_order_data)}")
        if len(work_order_data) > 0:
            print("First item:", work_order_data[0] if isinstance(work_order_data, list) else "Not a list")
    
    print("\n=== EXTRA ITEMS DATA ===")
    extra_items_data = data.get('extra_items_data', [])
    print(f"Type: {type(extra_items_data)}")
    if hasattr(extra_items_data, '__len__'):
        print(f"Length: {len(extra_items_data)}")
        if len(extra_items_data) > 0:
            print("First item:", extra_items_data[0] if isinstance(extra_items_data, list) else "Not a list")

if __name__ == "__main__":
    verify_data()
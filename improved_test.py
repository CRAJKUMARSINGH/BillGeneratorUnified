import pandas as pd
from core.processors.excel_processor import ExcelProcessor
from core.processors.batch_processor import add_bill_summary_sheet, create_bill_summary_data
import shutil
from pathlib import Path

# Process a test file
processor = ExcelProcessor()
with open('TEST_INPUT_FILES/0511-N-extra.xlsx', 'rb') as f:
    processed_data = processor.process_excel(f)

print("Work order data info:")
work_order_data = processed_data.get('work_order_data', pd.DataFrame())
print(f"Type: {type(work_order_data)}")
print(f"Shape: {work_order_data.shape}")
print(f"Columns: {list(work_order_data.columns)}")
print("First few rows:")
print(work_order_data.head())

print("\nCreating summary data...")
summary_df = create_bill_summary_data(processed_data)
print("Summary data:")
print(summary_df)

# Test the sheet addition
test_file = 'test_output/0511-N-extra_test_improved.xlsx'
Path('test_output').mkdir(exist_ok=True)
shutil.copy2('TEST_INPUT_FILES/0511-N-extra.xlsx', test_file)

print("\nAdding summary sheet...")
result = add_bill_summary_sheet(test_file, processed_data)
print(f"Result: {result}")
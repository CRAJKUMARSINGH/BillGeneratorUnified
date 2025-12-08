import pandas as pd
from core.processors.excel_processor import ExcelProcessor

# Test the actual processor method
processor = ExcelProcessor()

excel_file = 'TEST_INPUT_FILES/FirstFINALnoExtra.xlsx'
excel_data = pd.ExcelFile(excel_file)

sheet_name = 'Work Order'
required_cols = ['Item No.', 'Description', 'Unit', 'Quantity', 'Rate']
column_mapping = processor.column_mappings[sheet_name]

print("Testing _read_sheet_with_flexible_columns method:")
try:
    result_df = processor._read_sheet_with_flexible_columns(
        excel_data, sheet_name, required_cols, column_mapping
    )
    print("Success!")
    print("DataFrame columns:", list(result_df.columns))
    print("First few rows:")
    print(result_df.head())
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
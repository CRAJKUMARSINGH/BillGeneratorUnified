import pandas as pd
from core.processors.excel_processor import ExcelProcessor

# Create a test to see what's happening with column mapping
processor = ExcelProcessor()

# Let's manually test the column mapping logic
excel_file = 'TEST_INPUT_FILES/FirstFINALnoExtra.xlsx'
excel_data = pd.ExcelFile(excel_file)

sheet_name = 'Work Order'
required_cols = ['Item No.', 'Description', 'Unit', 'Quantity', 'Rate']
column_mapping = processor.column_mappings[sheet_name]

print("Required columns:", required_cols)
print("Column mapping:", column_mapping)

# Read sample to see available columns
df_sample = pd.read_excel(excel_data, sheet_name, nrows=1)
available_columns = list(df_sample.columns)
print("Available columns:", available_columns)

# Test the mapping logic
actual_cols = []
for expected_col in required_cols:
    print(f"\nProcessing expected column: '{expected_col}'")
    if expected_col in column_mapping:
        actual_col_name = column_mapping[expected_col]
        print(f"  Found in mapping: '{expected_col}' -> '{actual_col_name}'")
        # Check if the actual column exists in the sheet
        if actual_col_name in available_columns:
            print(f"  Actual column '{actual_col_name}' found in available columns")
            actual_cols.append(actual_col_name)
        else:
            print(f"  Actual column '{actual_col_name}' NOT found in available columns")
            # Try to find a column that might match (case-insensitive partial match)
            found = False
            for col in available_columns:
                if expected_col.lower() in col.lower() or col.lower() in expected_col.lower():
                    print(f"    Found partial match: '{col}'")
                    actual_cols.append(col)
                    found = True
                    break
            if not found:
                print(f"    No match found, using expected column name")
                actual_cols.append(expected_col)
    else:
        print(f"  Not found in mapping, using as-is")
        actual_cols.append(expected_col)

print(f"\nFinal actual columns to use: {actual_cols}")

# Try to read with these columns
try:
    df = pd.read_excel(excel_data, sheet_name, usecols=actual_cols)
    print("Success! DataFrame columns:", list(df.columns))
except Exception as e:
    print(f"Error: {e}")
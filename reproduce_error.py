import pandas as pd

# Reproduce the exact error by directly using pandas with wrong column names
print("Reproducing the exact error...")

try:
    # This should fail because the file has 'Item' column, not 'Item No.'
    df = pd.read_excel('TEST_INPUT_FILES/FirstFINALnoExtra.xlsx', 'Work Order', usecols=['Item No.', 'Description', 'Unit', 'Quantity', 'Rate'])
    print("Unexpected success!")
except ValueError as e:
    print(f"Error reproduced: {e}")
    print("This is the exact error mentioned in the issue!")

print("\nNow showing what the file actually has:")
excel_data = pd.ExcelFile('TEST_INPUT_FILES/FirstFINALnoExtra.xlsx')
df_sample = pd.read_excel(excel_data, 'Work Order', nrows=1)
print("Available columns:", list(df_sample.columns))

print("\nThe issue is that someone is trying to use 'Item No.' directly instead of 'Item'")
import pandas as pd
import os

files = os.listdir('TEST_INPUT_FILES')
print('Checking all Excel files for column names...')

for file in files:
    if file.endswith('.xlsx') or file.endswith('.xls'):
        full_path = os.path.join('TEST_INPUT_FILES', file)
        try:
            df = pd.read_excel(full_path, 'Work Order')
            print(f'{file}: {list(df.columns)}')
        except Exception as e:
            print(f'{file}: Error - {e}')
from core.processors.excel_processor import ExcelProcessor

# Process the Excel file
processor = ExcelProcessor()
data = processor.process_excel('TEST_INPUT_FILES/0511-N-extra.xlsx')
title_data = data.get('title_data', {})

# Print all keys with their values
print('All title data keys and values:')
print('=' * 50)
for k, v in title_data.items():
    if k not in ['_first_20_rows_processed', '_first_20_rows_count']:
        print(f'"{k}": {v}')

print('\nChecking specific template keys:')
print('=' * 30)
template_keys = [
    'Agreement No.',
    'A&F Sanction',
    'Technical Section', 
    'Measurement Book No',
    'Measurement Book Page',
    'Sub Division',
    'Name of Work ;-',
    'Name of Contractor or supplier :',
    'Original/Deposit',
    'Budget Provision',
    'Date of Commencement',
    'Date of Completion',
    'Actual Date of Completion',
    'Delay Extension',
    'Notice Issued',
    'Measurement Date',
    'Repair Work',
    'Excess Quantity',
    'Delay Comment'
]

for key in template_keys:
    found = key in title_data
    value = title_data.get(key, 'NOT FOUND')
    print(f'"{key}": {"✓" if found else "✗"} ({value})')
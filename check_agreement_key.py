from core.processors.excel_processor import ExcelProcessor

# Process the Excel file
processor = ExcelProcessor()
data = processor.process_excel('TEST_INPUT_FILES/0511-N-extra.xlsx')
title_data = data.get('title_data', {})

print('Keys containing Agreement:')
for k in title_data.keys():
    if 'Agreement' in k:
        print(f'  "{k}"')
        
print()
print('Exact key check:')
print('"Agreement No." in title_data:', "Agreement No." in title_data)
print('"Agreement No" in title_data:', "Agreement No" in title_data)
print('Value for "Agreement No.":', title_data.get("Agreement No.", "NOT FOUND"))
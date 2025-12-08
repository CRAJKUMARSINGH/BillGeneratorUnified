import os
from core.processors.excel_processor import ExcelProcessor

processor = ExcelProcessor()
files = [f for f in os.listdir('TEST_INPUT_FILES') if f.endswith(('.xlsx', '.xls'))]
print(f'Testing with {len(files)} Excel files...')
success_count = 0

for file in files:
    try:
        processed_data = processor.process_excel(f'TEST_INPUT_FILES/{file}')
        print(f'✅ {file}: OK')
        success_count += 1
    except Exception as e:
        print(f'❌ {file}: {str(e)[:50]}...')

print(f'\nResult: {success_count}/{len(files)} files processed successfully')
import os
from core.processors.excel_processor import ExcelProcessor

processor = ExcelProcessor()
files = [f for f in os.listdir('TEST_INPUT_FILES') if f.endswith('.xlsx')][:3]
print(f'Testing with {len(files)} files...')
success_count = 0

for file in files:
    try:
        processed_data = processor.process_excel(f'TEST_INPUT_FILES/{file}')
        print(f'✅ {file}: OK')
        success_count += 1
    except Exception as e:
        print(f'❌ {file}: {e}')

print(f'\nResult: {success_count}/{len(files)} files processed successfully')
import traceback
from core.processors.excel_processor import ExcelProcessor

processor = ExcelProcessor()
with open('TEST_INPUT_FILES/FirstFINALnoExtra.xlsx', 'rb') as f:
    try:
        data = processor.process_excel(f)
        print('Success!')
        print('Work order columns:', list(data['work_order_data'].columns))
    except Exception as e:
        print('Error occurred:')
        traceback.print_exc()
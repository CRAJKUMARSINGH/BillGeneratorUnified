from core.processors.excel_processor import ExcelProcessor

# Test the Excel processor with one of the files
processor = ExcelProcessor()

with open('TEST_INPUT_FILES/FirstFINALnoExtra.xlsx', 'rb') as f:
    data = processor.process_excel(f)
    print('Work order columns:', list(data['work_order_data'].columns))
    print(data['work_order_data'].head())
    print('\nBill quantity columns:', list(data['bill_quantity_data'].columns))
    print(data['bill_quantity_data'].head())
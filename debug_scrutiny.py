from core.processors.excel_processor import ExcelProcessor
from core.generators.document_generator import DocumentGenerator

# Process the Excel file
processor = ExcelProcessor()
data = processor.process_excel('TEST_INPUT_FILES/0511-N-extra.xlsx')

# Print first 20 rows info
title_data = data.get('title_data', {})
print("First 20 rows processing info:")
print(f"  First 20 rows processed: {title_data.get('_first_20_rows_processed', False)}")
print(f"  First 20 rows count: {title_data.get('_first_20_rows_count', 0)}")

# Generate documents
generator = DocumentGenerator(data)
documents = generator.generate_all_documents()

# Get the scrutiny sheet
scrutiny_sheet = documents['BILL SCRUTINY SHEET']

# Write to file
with open('debug_scrutiny.html', 'w', encoding='utf-8') as f:
    f.write(scrutiny_sheet)
    
print("HTML written to debug_scrutiny.html")

# Also print some key parts
print("\nHeader section:")
start = scrutiny_sheet.find('<div class="header">')
end = scrutiny_sheet.find('</div>', start) + 6
print(scrutiny_sheet[start:end])

print("\nFirst few table rows:")
start = scrutiny_sheet.find('<table class="specific-table">')
end = scrutiny_sheet.find('</table>', start) + 8
table_content = scrutiny_sheet[start:end]
lines = table_content.split('\n')
for i, line in enumerate(lines[:30]):  # Print first 30 lines
    if line.strip():
        print(f"{i+1:2d}: {line}")
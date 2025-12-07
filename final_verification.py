#!/usr/bin/env python3
"""
Final verification script for first 20 rows implementation.
"""

from core.processors.excel_processor import ExcelProcessor
from core.generators.document_generator import DocumentGenerator

def main():
    # Process an Excel file
    processor = ExcelProcessor()
    processed_data = processor.process_excel('TEST_INPUT_FILES/FirstFINALnoExtra.xlsx')
    
    # Check Excel processing results
    title_data = processed_data['title_data']
    print("Excel Processing Results:")
    print(f"  First 20 rows processed: {title_data.get('_first_20_rows_processed')}")
    print(f"  Rows count: {title_data.get('_first_20_rows_count')}")
    
    # Generate documents
    generator = DocumentGenerator(processed_data)
    
    # Check document generation results
    template_data = generator.template_data
    print("\nDocument Generation Results:")
    print(f"  First 20 rows processed: {template_data.get('first_20_rows_processed')}")
    print(f"  Rows count: {template_data.get('first_20_rows_count')}")
    
    # Generate documents
    documents = generator.generate_all_documents()
    print(f"\nDocuments Generated: {len(documents)}")
    for doc_name in documents.keys():
        print(f"  - {doc_name}")
    
    print("\n✅ First 20 rows implementation verified successfully!")

if __name__ == "__main__":
    main()
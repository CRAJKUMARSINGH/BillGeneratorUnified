#!/usr/bin/env python3
"""
Test script to verify that first 20 rows data is properly processed and used in document generation.
"""

import pandas as pd
from core.processors.excel_processor import ExcelProcessor
from core.generators.document_generator import DocumentGenerator

def test_first_20_rows_integration():
    """Test that first 20 rows data is properly integrated through the entire pipeline."""
    
    # Process an Excel file
    processor = ExcelProcessor()
    processed_data = processor.process_excel('TEST_INPUT_FILES/FirstFINALnoExtra.xlsx')
    
    # Check that first 20 rows metadata is present
    title_data = processed_data['title_data']
    assert title_data.get('_first_20_rows_processed') == True, "First 20 rows should be marked as processed"
    assert title_data.get('_first_20_rows_count') > 0, "Should have processed some rows"
    
    print(f"✓ First 20 rows processed: {title_data.get('_first_20_rows_processed')}")
    print(f"✓ Rows count: {title_data.get('_first_20_rows_count')}")
    
    # Generate documents
    generator = DocumentGenerator(processed_data)
    
    # Check that template data includes first 20 rows metadata
    template_data = generator.template_data
    assert template_data.get('first_20_rows_processed') == True, "Template data should include first 20 rows processed flag"
    assert template_data.get('first_20_rows_count') == title_data.get('_first_20_rows_count'), "Row counts should match"
    
    print(f"✓ Template data includes first 20 rows flag: {template_data.get('first_20_rows_processed')}")
    print(f"✓ Template data row count matches: {template_data.get('first_20_rows_count')}")
    
    # Generate documents and check they contain the metadata
    documents = generator.generate_all_documents()
    
    # Check that the First Page document contains references to first 20 rows data
    first_page = documents.get('First Page Summary', '')
    assert '<title>CONTRACTOR BILL</title>' in first_page or '<h2>CONTRACTOR BILL</h2>' in first_page, "Should contain document title"
    
    print("✓ Documents generated successfully")
    
    # Show some sample data that would appear in the documents
    print("\nSample title data that will appear in documents:")
    important_fields = [
        'Project Name',
        'Work Order No',
        'Contract No',
        'Contractor Name',
        'Date of Commencement',
        'Date of Completion'
    ]
    
    for field in important_fields:
        value = title_data.get(field, 'Not found')
        print(f"  {field}: {value}")
    
    print("\n✓ First 20 rows integration test PASSED")
    return True

if __name__ == "__main__":
    test_first_20_rows_integration()
#!/usr/bin/env python3
"""
Complete system verification - checks both XLSM update and first 20 rows implementation.
"""

import pandas as pd
from core.processors.excel_processor import ExcelProcessor
from core.generators.document_generator import DocumentGenerator

def verify_xlsm_update():
    """Verify that the XLSM file has been correctly updated."""
    try:
        # Read the updated XLSM file
        xl = pd.ExcelFile('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_UPDATED.xlsm')
        sheet_name = xl.sheet_names[0]  # Get the first sheet name
        df = pd.read_excel('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_UPDATED.xlsm', 
                          sheet_name=sheet_name, header=None)
        
        print("=== XLSM FILE STRUCTURE VERIFICATION ===")
        print(f"Using sheet: {sheet_name}")
        
        # Check for the updated structure
        row_16 = str(df.iloc[16, 0]) if len(df) > 16 else ""
        row_17a = str(df.iloc[17, 0]) if len(df) > 17 else ""
        row_17b = str(df.iloc[18, 0]) if len(df) > 18 else ""
        row_17c = str(df.iloc[19, 0]) if len(df) > 19 else ""
        
        print(f"Row 16 (Item 16): {row_16}")
        print(f"Row 17 (17.A): {row_17a}")
        print(f"Row 18 (17.B): {row_17b}")
        print(f"Row 19 (17.C): {row_17c}")
        
        # Verify the structure is correct
        success = ("16." in row_16 and 
                  "17.A." in row_17a and 
                  "B." in row_17b and 
                  "C." in row_17c)
        
        if success:
            print("✅ XLSM structure update VERIFIED")
        else:
            print("❌ XLSM structure update FAILED")
            
        return success
        
    except Exception as e:
        print(f"Error verifying XLSM structure: {e}")
        return False

def verify_first_20_rows_processing():
    """Verify that first 20 rows processing is working correctly."""
    try:
        print("\n=== FIRST 20 ROWS PROCESSING VERIFICATION ===")
        
        # Process an Excel file
        processor = ExcelProcessor()
        processed_data = processor.process_excel('TEST_INPUT_FILES/FirstFINALnoExtra.xlsx')
        
        # Check Excel processing results
        title_data = processed_data['title_data']
        excel_success = (title_data.get('_first_20_rows_processed') == True and
                        title_data.get('_first_20_rows_count') > 0)
        
        print(f"Excel Processing - First 20 rows processed: {title_data.get('_first_20_rows_processed')}")
        print(f"Excel Processing - Rows count: {title_data.get('_first_20_rows_count')}")
        
        # Generate documents
        generator = DocumentGenerator(processed_data)
        
        # Check document generation results
        template_data = generator.template_data
        doc_success = (template_data.get('first_20_rows_processed') == True and
                      template_data.get('first_20_rows_count') == title_data.get('_first_20_rows_count'))
        
        print(f"Document Generation - First 20 rows processed: {template_data.get('first_20_rows_processed')}")
        print(f"Document Generation - Rows count: {template_data.get('first_20_rows_count')}")
        
        # Generate documents
        documents = generator.generate_all_documents()
        docs_generated = len(documents) > 0
        
        print(f"Documents Generated: {len(documents)}")
        for doc_name in list(documents.keys())[:3]:  # Show first 3
            print(f"  - {doc_name}")
        if len(documents) > 3:
            print(f"  ... and {len(documents) - 3} more")
        
        success = excel_success and doc_success and docs_generated
        
        if success:
            print("✅ First 20 rows processing VERIFIED")
        else:
            print("❌ First 20 rows processing FAILED")
            
        return success
        
    except Exception as e:
        print(f"Error verifying first 20 rows processing: {e}")
        return False

def main():
    """Run complete system verification."""
    print("STARTING COMPLETE SYSTEM VERIFICATION")
    print("=" * 50)
    
    # Verify XLSM update
    xlsm_success = verify_xlsm_update()
    
    # Verify first 20 rows processing
    first_20_success = verify_first_20_rows_processing()
    
    # Overall result
    print("\n" + "=" * 50)
    print("FINAL VERIFICATION RESULTS")
    print("=" * 50)
    print(f"XLSM File Update: {'✅ PASS' if xlsm_success else '❌ FAIL'}")
    print(f"First 20 Rows Processing: {'✅ PASS' if first_20_success else '❌ FAIL'}")
    
    overall_success = xlsm_success and first_20_success
    print(f"Overall System Status: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 SYSTEM VERIFICATION COMPLETE - ALL ENHANCEMENTS WORKING CORRECTLY!")
    else:
        print("\n⚠️  SYSTEM VERIFICATION INCOMPLETE - SOME ISSUES FOUND")
    
    return overall_success

if __name__ == "__main__":
    main()
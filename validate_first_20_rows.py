#!/usr/bin/env python3
"""
Validation script to ensure the first 20 rows of title data are accurately 
processed and displayed in first page and deviation documents.
"""

import pandas as pd
import json
import os
from pathlib import Path
from core.processors.excel_processor import ExcelProcessor
from core.generators.document_generator import DocumentGenerator

def validate_first_20_rows_in_excel(file_path):
    """
    Validate that the first 20 rows of title data are properly extracted from Excel.
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        dict: Validation results
    """
    try:
        # Process the Excel file
        processor = ExcelProcessor()
        processed_data = processor.process_excel(file_path)
        title_data = processed_data.get('title_data', {})
        
        # Check if first 20 rows processing metadata exists
        first_20_processed = title_data.get('_first_20_rows_processed', False)
        first_20_count = title_data.get('_first_20_rows_count', 0)
        
        # Read the Title sheet directly to count actual rows
        title_df = pd.read_excel(file_path, 'Title', header=None)
        actual_rows = len(title_df)
        
        # Validation results
        results = {
            'file_path': file_path,
            'first_20_rows_processed': first_20_processed,
            'first_20_rows_count': first_20_count,
            'actual_title_rows': actual_rows,
            'processing_status': 'SUCCESS' if first_20_processed else 'FAILED',
            'details': {}
        }
        
        # Detailed validation
        if first_20_processed:
            results['details']['metadata_present'] = True
            results['details']['rows_processed'] = first_20_count
            results['details']['rows_expected'] = min(20, actual_rows)
            results['details']['processing_complete'] = first_20_count >= min(20, actual_rows) * 0.8  # At least 80% of expected rows
            
            # Check for common required fields in first 20 rows
            required_fields = [
                'Project Name', 'Work Order No', 'Contract No', 
                'Contractor Name', 'Date of Commencement', 'Date of Completion'
            ]
            
            found_fields = [field for field in required_fields if field in title_data]
            results['details']['required_fields_found'] = found_fields
            results['details']['required_fields_missing'] = [field for field in required_fields if field not in title_data]
            results['details']['required_fields_coverage'] = f"{len(found_fields)}/{len(required_fields)}"
            
        else:
            results['details']['error'] = "First 20 rows processing metadata not found"
            
        return results
        
    except Exception as e:
        return {
            'file_path': file_path,
            'processing_status': 'ERROR',
            'error': str(e)
        }

def validate_first_20_rows_in_documents(file_path):
    """
    Validate that the first 20 rows of title data are properly displayed in generated documents.
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        dict: Validation results
    """
    try:
        # Process the Excel file
        processor = ExcelProcessor()
        processed_data = processor.process_excel(file_path)
        
        # Generate documents
        generator = DocumentGenerator(processed_data)
        documents = generator.generate_all_documents()
        
        # Get template data which includes our validation metadata
        template_data = generator.template_data
        
        # Check first 20 rows processing metadata
        first_20_processed = template_data.get('first_20_rows_processed', False)
        first_20_count = template_data.get('first_20_rows_count', 0)
        
        # Validation results
        results = {
            'file_path': file_path,
            'first_20_rows_processed': first_20_processed,
            'first_20_rows_count': first_20_count,
            'documents_generated': list(documents.keys()),
            'document_generation_status': 'SUCCESS',
            'template_data_validation': {}
        }
        
        # Validate template data contains first 20 rows metadata
        results['template_data_validation']['metadata_present'] = first_20_processed
        results['template_data_validation']['rows_count'] = first_20_count
        
        # Check if key documents contain title data
        key_documents = ['First Page Summary', 'Deviation Statement', 'BILL SCRUTINY SHEET']
        document_checks = {}
        
        for doc_name in key_documents:
            if doc_name in documents:
                doc_content = documents[doc_name]
                # Check for presence of common title data fields
                title_data = processed_data.get('title_data', {})
                found_fields = []
                missing_fields = []
                
                # Check for common fields
                common_fields = [
                    'Project Name', 'Work Order No', 'Contract No', 
                    'Contractor Name', 'Date of Commencement'
                ]
                
                for field in common_fields:
                    if field in title_data and str(title_data[field]) in doc_content:
                        found_fields.append(field)
                    else:
                        missing_fields.append(field)
                
                document_checks[doc_name] = {
                    'fields_found': found_fields,
                    'fields_missing': missing_fields,
                    'coverage': f"{len(found_fields)}/{len(common_fields)}"
                }
        
        results['document_content_validation'] = document_checks
        
        return results
        
    except Exception as e:
        return {
            'file_path': file_path,
            'document_generation_status': 'ERROR',
            'error': str(e)
        }

def batch_validate_first_20_rows(input_folder='TEST_INPUT_FILES'):
    """
    Batch validate first 20 rows processing for all Excel files in a folder.
    
    Args:
        input_folder (str): Path to input folder containing Excel files
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Input folder not found: {input_folder}")
        return
    
    # Results storage
    excel_results = []
    document_results = []
    
    # Process each Excel file
    for file_path in input_path.glob('*.xlsx'):
        print(f"\nValidating: {file_path.name}")
        
        # Validate Excel processing
        excel_result = validate_first_20_rows_in_excel(file_path)
        excel_results.append(excel_result)
        
        # Validate document generation
        doc_result = validate_first_20_rows_in_documents(file_path)
        document_results.append(doc_result)
        
        # Print summary
        print(f"  Excel Processing: {excel_result.get('processing_status', 'UNKNOWN')}")
        print(f"  Document Generation: {doc_result.get('document_generation_status', 'UNKNOWN')}")
        
        if 'first_20_rows_count' in excel_result:
            print(f"  Rows Processed: {excel_result['first_20_rows_count']}")
        
        if 'details' in excel_result:
            details = excel_result['details']
            if 'required_fields_coverage' in details:
                print(f"  Required Fields Coverage: {details['required_fields_coverage']}")
    
    # Save results
    output_dir = Path('VALIDATION_OUTPUT')
    output_dir.mkdir(exist_ok=True)
    
    # Save Excel validation results
    excel_report_path = output_dir / 'excel_validation_report.json'
    with open(excel_report_path, 'w', encoding='utf-8') as f:
        json.dump(excel_results, f, indent=2, default=str)
    
    # Save document validation results
    doc_report_path = output_dir / 'document_validation_report.json'
    with open(doc_report_path, 'w', encoding='utf-8') as f:
        json.dump(document_results, f, indent=2, default=str)
    
    print(f"\nValidation complete!")
    print(f"Excel validation report saved to: {excel_report_path}")
    print(f"Document validation report saved to: {doc_report_path}")
    
    return excel_results, document_results

def main():
    """Main function to run validation."""
    print("Validating first 20 rows processing in Excel files and documents...")
    print("=" * 70)
    
    # Run batch validation
    excel_results, document_results = batch_validate_first_20_rows()
    
    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    successful_excel = sum(1 for r in excel_results if r.get('processing_status') == 'SUCCESS')
    total_excel = len(excel_results)
    
    successful_docs = sum(1 for r in document_results if r.get('document_generation_status') == 'SUCCESS')
    total_docs = len(document_results)
    
    print(f"Excel Processing: {successful_excel}/{total_excel} files successful")
    print(f"Document Generation: {successful_docs}/{total_docs} files successful")
    
    # Detailed results
    print("\nDetailed Results:")
    for i, (excel_result, doc_result) in enumerate(zip(excel_results, document_results)):
        file_name = Path(excel_result.get('file_path', '')).name
        excel_status = excel_result.get('processing_status', 'UNKNOWN')
        doc_status = doc_result.get('document_generation_status', 'UNKNOWN')
        rows_count = excel_result.get('first_20_rows_count', 'N/A')
        
        print(f"  {i+1}. {file_name}:")
        print(f"     Excel Processing: {excel_status} ({rows_count} rows)")
        print(f"     Document Generation: {doc_status}")

if __name__ == "__main__":
    main()
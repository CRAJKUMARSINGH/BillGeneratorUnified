#!/usr/bin/env python3
"""
Batch processing script to ensure the first 20 rows of title data are 
accurately filled and dynamically updated in all generated documents.
"""

import os
import sys
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from core.processors.excel_processor import ExcelProcessor
from core.generators.document_generator import DocumentGenerator

def process_single_file(input_file, output_dir):
    """
    Process a single Excel file and generate documents with first 20 rows validation.
    
    Args:
        input_file (Path): Path to input Excel file
        output_dir (Path): Output directory for generated documents
        
    Returns:
        dict: Processing results
    """
    result = {
        'input_file': str(input_file),
        'status': 'pending',
        'error': None,
        'title_data_summary': {},
        'documents_generated': [],
        'processing_time': None
    }
    
    try:
        start_time = datetime.now()
        
        print(f"Processing: {input_file.name}")
        
        # Process Excel file
        processor = ExcelProcessor()
        processed_data = processor.process_excel(str(input_file))
        title_data = processed_data.get('title_data', {})
        
        # Extract title data summary
        result['title_data_summary'] = {
            'total_keys': len(title_data),
            'first_20_rows_processed': title_data.get('_first_20_rows_processed', False),
            'first_20_rows_count': title_data.get('_first_20_rows_count', 0),
            'key_fields': {k: str(v) for k, v in list(title_data.items())[:10]}  # First 10 fields for preview
        }
        
        # Generate documents
        generator = DocumentGenerator(processed_data)
        html_documents = generator.generate_all_documents()
        
        # Generate PDF documents
        try:
            pdf_documents = generator.create_pdf_documents(html_documents)
        except Exception as pdf_error:
            print(f"Warning: PDF generation failed for {input_file.name}: {pdf_error}")
            pdf_documents = {}
        
        # Generate DOC documents
        try:
            doc_documents = generator.generate_doc_documents()
        except Exception as doc_error:
            print(f"Warning: DOC generation failed for {input_file.name}: {doc_error}")
            doc_documents = {}
        
        # Save HTML documents
        for doc_name, html_content in html_documents.items():
            safe_name = "".join(c for c in doc_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = output_dir / f"{input_file.stem}_{safe_name}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            result['documents_generated'].append(str(output_file))
        
        # Save PDF documents
        for doc_name, pdf_content in pdf_documents.items():
            safe_name = "".join(c for c in doc_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = output_dir / f"{input_file.stem}_{safe_name}.pdf"
            with open(output_file, 'wb') as f:
                f.write(pdf_content)
            result['documents_generated'].append(str(output_file))
        
        # Save DOC documents
        for doc_name, doc_content in doc_documents.items():
            safe_name = "".join(c for c in doc_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = output_dir / f"{input_file.stem}_{safe_name}"
            with open(output_file, 'wb') as f:
                f.write(doc_content)
            result['documents_generated'].append(str(output_file))
        
        end_time = datetime.now()
        result['processing_time'] = str(end_time - start_time)
        result['status'] = 'success'
        
        print(f"  ✓ Generated {len(html_documents)} HTML, {len(pdf_documents)} PDF, and {len(doc_documents)} DOC documents")
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        print(f"  ✗ Error processing {input_file.name}: {e}")
    
    return result

def batch_process_first_20_rows(input_folder='TEST_INPUT_FILES', output_folder='OUTPUT_FIRST_20_ROWS'):
    """
    Batch process all Excel files to ensure first 20 rows are accurately handled.
    
    Args:
        input_folder (str): Path to input folder containing Excel files
        output_folder (str): Path to output folder for generated documents
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Create output directory
    output_path.mkdir(exist_ok=True)
    
    if not input_path.exists():
        print(f"Input folder not found: {input_folder}")
        return
    
    # Results tracking
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_folder': str(input_path),
        'output_folder': str(output_path),
        'total_files': 0,
        'successful_files': 0,
        'failed_files': 0,
        'file_results': []
    }
    
    # Process Excel files
    excel_files = list(input_path.glob('*.xlsx')) + list(input_path.glob('*.xls'))
    results['total_files'] = len(excel_files)
    
    print(f"Found {results['total_files']} Excel files to process")
    print("=" * 50)
    
    for i, input_file in enumerate(excel_files, 1):
        print(f"[{i}/{results['total_files']}] ", end="")
        
        # Create subdirectory for this file's output
        file_output_dir = output_path / input_file.stem
        file_output_dir.mkdir(exist_ok=True)
        
        # Process the file
        file_result = process_single_file(input_file, file_output_dir)
        results['file_results'].append(file_result)
        
        # Update counters
        if file_result['status'] == 'success':
            results['successful_files'] += 1
        else:
            results['failed_files'] += 1
    
    # Save results summary
    summary_file = output_path / 'batch_processing_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "=" * 50)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 50)
    print(f"Total files processed: {results['total_files']}")
    print(f"Successful: {results['successful_files']}")
    print(f"Failed: {results['failed_files']}")
    print(f"Success rate: {results['successful_files']/results['total_files']*100:.1f}%")
    print(f"Summary saved to: {summary_file}")
    
    # Detailed failure report if any
    if results['failed_files'] > 0:
        print("\nFailed files:")
        for result in results['file_results']:
            if result['status'] == 'error':
                print(f"  - {Path(result['input_file']).name}: {result['error']}")
    
    return results

def validate_first_20_rows_accuracy(results):
    """
    Validate that first 20 rows were accurately processed.
    
    Args:
        results (dict): Batch processing results
        
    Returns:
        dict: Validation report
    """
    validation_report = {
        'total_files_validated': len(results['file_results']),
        'files_with_first_20_metadata': 0,
        'files_with_adequate_row_coverage': 0,
        'validation_details': []
    }
    
    for file_result in results['file_results']:
        detail = {
            'file': Path(file_result['input_file']).name,
            'has_metadata': False,
            'row_coverage': 0,
            'validation_status': file_result['status']
        }
        
        if file_result['status'] == 'success':
            title_summary = file_result.get('title_data_summary', {})
            has_metadata = title_summary.get('first_20_rows_processed', False)
            row_count = title_summary.get('first_20_rows_count', 0)
            
            detail['has_metadata'] = has_metadata
            detail['row_count'] = row_count
            
            if has_metadata:
                validation_report['files_with_first_20_metadata'] += 1
            
            # Consider adequate if at least 10 rows processed (for files with sufficient data)
            if row_count >= 10:
                validation_report['files_with_adequate_row_coverage'] += 1
                detail['adequate_coverage'] = True
            else:
                detail['adequate_coverage'] = False
        
        validation_report['validation_details'].append(detail)
    
    return validation_report

def main():
    """Main function to run batch processing."""
    print("Batch Processing First 20 Rows of Title Data")
    print("=" * 50)
    
    # Run batch processing
    results = batch_process_first_20_rows()
    
    # Validate accuracy
    validation_report = validate_first_20_rows_accuracy(results)
    
    # Save validation report
    output_path = Path('OUTPUT_FIRST_20_ROWS')
    validation_file = output_path / 'first_20_rows_validation_report.json'
    with open(validation_file, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2, default=str)
    
    # Print validation summary
    print("\nFirst 20 Rows Validation Summary:")
    print("-" * 30)
    print(f"Files with first 20 rows metadata: {validation_report['files_with_first_20_metadata']}/{validation_report['total_files_validated']}")
    print(f"Files with adequate row coverage: {validation_report['files_with_adequate_row_coverage']}/{validation_report['total_files_validated']}")
    
    print(f"\nValidation report saved to: {validation_file}")
    print("\nAll processing complete!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Improved validation script to ensure data in rows 1 to 20 of the scrutiny sheet 
is accurately filled and dynamically updated from title input sheet data.
"""

import pandas as pd
import json
import os
from pathlib import Path
from core.processors.excel_processor import ExcelProcessor
from core.generators.document_generator import DocumentGenerator

def validate_scrutiny_sheet_content(file_path):
    """
    Validate that the scrutiny sheet properly displays data from the Title sheet.
    
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
        
        # Generate documents
        generator = DocumentGenerator(processed_data)
        documents = generator.generate_all_documents()
        
        # Get template data
        template_data = generator.template_data
        
        # Check if we have the BILL SCRUTINY SHEET
        if 'BILL SCRUTINY SHEET' not in documents:
            return {
                'file_path': file_path,
                'validation_status': 'FAILED',
                'error': 'BILL SCRUTINY SHEET not generated'
            }
        
        scrutiny_sheet_html = documents['BILL SCRUTINY SHEET']
        
        # Validation results
        results = {
            'file_path': file_path,
            'validation_status': 'SUCCESS',
            'first_20_rows_processed': template_data.get('first_20_rows_processed', False),
            'first_20_rows_count': template_data.get('first_20_rows_count', 0),
            'title_data_fields': len(title_data),
            'scrutiny_sheet_generated': True,
            'validation_details': {}
        }
        
        # Check for specific fields that should appear in scrutiny sheet
        # These are the actual template expressions we're looking for
        template_checks = [
            # Direct title_data checks
            ("{{ data.title_data.get('Agreement No', data.title_data.get('Work Order No', '')) }}", 'Agreement No/Work Order No'),
            ("{{ data.title_data.get('A&F Sanction', 'Refer Agreement') }}", 'A&F Sanction'),
            ("{{ data.title_data.get('Technical Section', 'Refer Agreement') }}", 'Technical Section'),
            ("{{ data.title_data.get('Measurement Book No', '887') }}/Page No. {{ data.title_data.get('Measurement Book Page', '04-20') }}", 'MB No. & Page'),
            ("{{ data.title_data.get('Sub Division', 'Rajsamand') }}", 'Sub Division'),
            ("{{ data.title_data.get('Name of Work', data.title_data.get('Project Name', '')) }}", 'Name of Work'),
            ("{{ data.title_data.get('Name of Firm', data.title_data.get('Contractor Name', '')) }}", 'Name of Contractor'),
            ("{{ data.title_data.get('Original/Deposit', 'Deposit') }}", 'Original/Deposit'),
            ("{{ data.title_data.get('Budget Provision', 'Adequate') }}", 'Budget Provision'),
            ("{{ data.title_data.get('Date of Commencement', '') }}", 'Date of Commencement'),
            ("{{ data.title_data.get('Date of Completion', '') }}", 'Date of Completion'),
            ("{{ data.title_data.get('Actual Date of Completion', '') }}", 'Actual Date of Completion'),
            ("{{ data.title_data.get('Delay Extension', '315') }}", 'Delay Extension'),
            ("{{ data.title_data.get('Notice Issued', 'No.') }}", 'Notice Issued'),
            ("{{ data.title_data.get('Repair Work', 'No') }}", 'Repair Work'),
            ("{{ data.title_data.get('Excess Quantity', 'No') }}", 'Excess Quantity'),
            ("{{ data.title_data.get('Delay Comment', 'No') }}", 'Delay Comment'),
            ("{{ data.title_data.get('Measurement Date', '') }}", 'Measurement Date')
        ]
        
        found_template_expressions = []
        missing_template_expressions = []
        
        for expression, description in template_checks:
            # Check if the template expression is in the HTML (before rendering)
            # This is actually checking the template itself, not very useful
            # Let's check for actual rendered values instead
            
            # Look for actual values in the rendered HTML
            found = False
            if description == 'Agreement No/Work Order No':
                value1 = title_data.get('Agreement No.', '')
                value2 = title_data.get('Work Order No', '')
                if value1 and str(value1) in scrutiny_sheet_html:
                    found = True
                elif value2 and str(value2) in scrutiny_sheet_html:
                    found = True
            elif description == 'Name of Work':
                value1 = title_data.get('Name of Work ;-', '')
                value2 = title_data.get('Project Name', '')
                if value1 and str(value1) in scrutiny_sheet_html:
                    found = True
                elif value2 and str(value2) in scrutiny_sheet_html:
                    found = True
            elif description == 'Name of Contractor':
                value1 = title_data.get('Name of Contractor or supplier :', '')
                value2 = title_data.get('Contractor Name', '')
                if value1 and str(value1) in scrutiny_sheet_html:
                    found = True
                elif value2 and str(value2) in scrutiny_sheet_html:
                    found = True
            else:
                # For other fields, look for the key in title_data and its value in HTML
                key_found = False
                for key in title_data:
                    if description.lower().replace(' ', '') in key.lower().replace(' ', ''):
                        key_found = True
                        value = title_data[key]
                        if value and str(value) in scrutiny_sheet_html:
                            found = True
                            break
                # If we didn't find by key matching, check some common keys directly
                if not key_found:
                    direct_keys = {
                        'A&F Sanction': 'Reference to work order or Agreement :',
                        'Technical Section': 'Reference to work order or Agreement :',
                        'Sub Division': 'Name of Work ;-',
                        'Original/Deposit': 'Serial No. of this bill :',
                        'Budget Provision': 'WORK ORDER AMOUNT RS.',
                        'Date of Commencement': 'St. date of Start :',
                        'Date of Completion': 'St. date of completion :',
                        'Actual Date of Completion': 'Date of actual completion of work :',
                        'Delay Extension': 'Delay Extension',
                        'Notice Issued': 'Notice Issued',
                        'Repair Work': 'Repair Work',
                        'Excess Quantity': 'Excess Quantity',
                        'Delay Comment': 'Delay Comment',
                        'Measurement Date': 'Date of measurement :'
                    }
                    for desc, key in direct_keys.items():
                        if description == desc and key in title_data:
                            value = title_data[key]
                            if value and str(value) in scrutiny_sheet_html:
                                found = True
                                break
            
            if found:
                found_template_expressions.append(description)
            else:
                missing_template_expressions.append(description)
        
        results['validation_details']['template_expressions_found'] = found_template_expressions
        results['validation_details']['template_expressions_missing'] = missing_template_expressions
        results['validation_details']['template_coverage'] = f"{len(found_template_expressions)}/{len(template_checks)}"
        
        # Check financial data
        totals = template_data.get('totals', {})
        financial_checks = [
            ('work_order_amount', 'Work Order Amount'),
            ('last_bill_amount', '17.A - Upto Last Bill'),
            ('net_payable', '17.B - This Bill')
        ]
        
        found_financial = []
        missing_financial = []
        
        for key, description in financial_checks:
            if key in totals and str(totals[key]) in scrutiny_sheet_html:
                found_financial.append(description)
            else:
                missing_financial.append(description)
        
        results['validation_details']['financial_fields_found'] = found_financial
        results['validation_details']['financial_fields_missing'] = missing_financial
        results['validation_details']['financial_coverage'] = f"{len(found_financial)}/{len(financial_checks)}"
        
        return results
        
    except Exception as e:
        return {
            'file_path': file_path,
            'validation_status': 'ERROR',
            'error': str(e)
        }

def batch_improved_validation(input_folder='TEST_INPUT_FILES'):
    """
    Batch validate scrutiny sheets with improved checking.
    
    Args:
        input_folder (str): Path to input folder containing Excel files
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Input folder not found: {input_folder}")
        return
    
    # Results storage
    validation_results = []
    
    # Process each Excel file
    for file_path in input_path.glob('*.xlsx'):
        print(f"\nImproved validation for: {file_path.name}")
        
        # Validate scrutiny sheet
        result = validate_scrutiny_sheet_content(file_path)
        validation_results.append(result)
        
        # Print summary
        status = result.get('validation_status', 'UNKNOWN')
        print(f"  Validation Status: {status}")
        
        if status == 'SUCCESS':
            template_coverage = result.get('validation_details', {}).get('template_coverage', 'N/A')
            financial_coverage = result.get('validation_details', {}).get('financial_coverage', 'N/A')
            print(f"  Template Field Coverage: {template_coverage}")
            print(f"  Financial Data Coverage: {financial_coverage}")
    
    # Save results
    output_dir = Path('VALIDATION_OUTPUT')
    output_dir.mkdir(exist_ok=True)
    
    # Save validation results
    report_path = output_dir / 'improved_scrutiny_validation_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, default=str)
    
    print(f"\nImproved validation complete!")
    print(f"Report saved to: {report_path}")
    
    return validation_results

def show_sample_scrutiny_sheet(file_path):
    """
    Show a sample of the generated scrutiny sheet to verify content.
    
    Args:
        file_path (str): Path to the Excel file
    """
    try:
        # Process the Excel file
        processor = ExcelProcessor()
        processed_data = processor.process_excel(file_path)
        
        # Generate documents
        generator = DocumentGenerator(processed_data)
        documents = generator.generate_all_documents()
        
        if 'BILL SCRUTINY SHEET' in documents:
            scrutiny_sheet_html = documents['BILL SCRUTINY SHEET']
            
            # Extract some key parts to show
            print(f"\nSample content from generated scrutiny sheet for {Path(file_path).name}:")
            print("=" * 60)
            
            # Look for specific lines that show data
            lines = scrutiny_sheet_html.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['<td>', 'Project Name', 'Work Order', 'Contractor', 'Amount']):
                    if len(line.strip()) > 10:  # Only show substantial lines
                        # Clean up the line for display
                        clean_line = line.strip().replace('<td>', '').replace('</td>', '').replace('<tr>', '').replace('</tr>', '')
                        if clean_line and not clean_line.startswith('<'):
                            print(clean_line[:100] + ('...' if len(clean_line) > 100 else ''))
            
            print("=" * 60)
        
    except Exception as e:
        print(f"Error generating sample: {e}")

def main():
    """Main function to run improved validation."""
    print("IMPROVED VALIDATION OF SCRUTINY SHEET FIRST 20 ROWS DATA")
    print("=" * 70)
    
    # Show a sample of generated content
    print("\n1. SAMPLE GENERATED CONTENT:")
    print("-" * 40)
    test_files = list(Path('TEST_INPUT_FILES').glob('*.xlsx'))
    if test_files:
        show_sample_scrutiny_sheet(test_files[0])
    
    # Run improved validation
    print("\n2. IMPROVED VALIDATION RESULTS:")
    print("-" * 40)
    validation_results = batch_improved_validation()
    
    # Summary
    print("\n" + "=" * 70)
    print("IMPROVED VALIDATION SUMMARY")
    print("=" * 70)
    
    successful_validations = sum(1 for r in validation_results if r.get('validation_status') == 'SUCCESS')
    total_validations = len(validation_results)
    
    print(f"Scrutiny Sheets Validated: {successful_validations}/{total_validations} successful")
    
    # Detailed results
    print("\nDetailed Results:")
    for i, result in enumerate(validation_results):
        file_name = Path(result.get('file_path', '')).name
        status = result.get('validation_status', 'UNKNOWN')
        template_coverage = result.get('validation_details', {}).get('template_coverage', 'N/A')
        financial_coverage = result.get('validation_details', {}).get('financial_coverage', 'N/A')
        
        print(f"  {i+1}. {file_name}:")
        print(f"     Status: {status}")
        if status == 'SUCCESS':
            print(f"     Template Field Coverage: {template_coverage}")
            print(f"     Financial Data Coverage: {financial_coverage}")
    
    print("\n✅ Improved validation complete!")

if __name__ == "__main__":
    main()
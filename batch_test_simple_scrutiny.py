#!/usr/bin/env python3
"""
Batch Test Script for Simple Scrutiny Sheet Generation
Processes all test input files and generates scrutiny sheets
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.processors.excel_processor import ExcelProcessor
from simple_scrutiny_sheet_generator import create_scrutiny_sheet_simple

def determine_bill_type(filename):
    """Determine bill type from filename"""
    filename_lower = filename.lower()
    if 'final' in filename_lower:
        return "final"
    elif 'first' in filename_lower:
        return "first"
    elif 'running' in filename_lower:
        return "running"
    else:
        # Default to running for unknown types
        return "running"

def format_test_result(filename, result, duration):
    """Format test result for display"""
    status = "✅ PASS" if result['success'] else "❌ FAIL"
    duration_str = f"{duration:.2f}s"
    
    print(f"{status} | {filename:<30} | {duration_str:>8}")
    
    if not result['success']:
        print(f"         Error: {result.get('error', 'Unknown error')}")
    else:
        print(f"         Sheet: {result.get('sheet_name', 'N/A')}")
        if result.get('pdf_path'):
            print(f"         PDF: {Path(result['pdf_path']).name}")
        print(f"         Macro: {'✅' if result.get('macro_executed') else '⚠️'}")
        print(f"         Export: {'✅' if result.get('pdf_exported') else '⚠️'}")

def process_single_file(file_path, output_dir):
    """Process a single Excel file and generate scrutiny sheet"""
    start_time = datetime.now()
    
    try:
        print(f"\n📄 Processing: {file_path.name}")
        
        # Process the Excel file
        processor = ExcelProcessor()
        with open(file_path, 'rb') as f:
            processed_data = processor.process_excel(f)
        
        # Show basic info
        title_data = processed_data.get('title_data', {})
        print(f"   Contractor: {title_data.get('Name of Contractor or supplier :', 'N/A')}")
        print(f"   Agreement: {title_data.get('Agreement No.', 'N/A')}")
        print(f"   Work: {title_data.get('Name of Work ;-)', title_data.get('Name of Work', 'N/A'))}")
        
        # Determine bill type
        bill_type = determine_bill_type(file_path.name)
        print(f"   Bill Type: {bill_type}")
        
        # Generate scrutiny sheet
        template_path = "ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm"
        output_path = output_dir / f"{file_path.stem}_scrutiny.xlsm"
        pdf_path = output_dir / f"MACRO scrutiny SHEET IN PDF_{file_path.stem}.pdf"
        
        result = create_scrutiny_sheet_simple(
            template_path=template_path,
            output_path=str(output_path),
            processed_data=processed_data,
            bill_type=bill_type,
            output_pdf_path=str(pdf_path)
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        format_test_result(file_path.name, result, duration)
        
        return {
            'filename': file_path.name,
            'success': result['success'],
            'duration': duration,
            'result': result
        }
        
    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        error_result = {
            'success': False,
            'error': str(e)
        }
        
        format_test_result(file_path.name, error_result, duration)
        
        return {
            'filename': file_path.name,
            'success': False,
            'duration': duration,
            'result': error_result,
            'exception': traceback.format_exc()
        }

def batch_process_simple_scrutiny():
    """Batch process all test files for scrutiny sheet generation"""
    print("=" * 70)
    print("BATCH SIMPLE SCRUTINY SHEET GENERATION TEST")
    print("=" * 70)
    
    # Input and output directories
    input_dir = Path("TEST_INPUT_FILES")
    output_dir = Path("test_output") / "simple_scrutiny_sheets"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return
    
    # Find all Excel files
    excel_files = list(input_dir.glob("*.xlsx"))
    
    if not excel_files:
        print("❌ No Excel files found in TEST_INPUT_FILES directory")
        return
    
    print(f"📁 Found {len(excel_files)} test files")
    print(f"📂 Output directory: {output_dir}")
    print(f"📋 Files to process:")
    for file in excel_files:
        print(f"   - {file.name}")
    
    print("\n" + "=" * 70)
    print("PROCESSING FILES")
    print("=" * 70)
    print(f"{'Status':<8} | {'File Name':<30} | {'Duration':>8}")
    print("-" * 70)
    
    # Process each file
    results = []
    for file_path in excel_files:
        result = process_single_file(file_path, output_dir)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    total_files = len(results)
    successful = sum(1 for r in results if r['success'])
    failed = total_files - successful
    total_duration = sum(r['duration'] for r in results)
    
    print(f"📊 Total Files: {total_files}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Total Time: {total_duration:.2f}s")
    print(f"⚡ Average Time: {total_duration/total_files:.2f}s per file")
    
    # Success rate
    success_rate = (successful / total_files) * 100 if total_files > 0 else 0
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    # Detailed failure report
    if failed > 0:
        print(f"\n🔍 FAILURE DETAILS:")
        print("-" * 40)
        for result in results:
            if not result['success']:
                print(f"📄 {result['filename']}:")
                print(f"   Error: {result['result'].get('error', 'Unknown error')}")
    
    # Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = output_dir / f"batch_test_results_{timestamp}.json"
    
    # Convert results for JSON serialization
    json_results = []
    for result in results:
        json_result = result.copy()
        # Remove non-serializable items
        if 'exception' in json_result:
            del json_result['exception']
        json_results.append(json_result)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'total_files': total_files,
            'successful': successful,
            'failed': failed,
            'total_duration': total_duration,
            'success_rate': success_rate,
            'results': json_results
        }, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results

def show_sample_data_analysis():
    """Show sample data analysis from one of the test files"""
    print("\n" + "=" * 70)
    print("SAMPLE DATA ANALYSIS")
    print("=" * 70)
    
    # Process one file to show data structure
    test_file = Path("TEST_INPUT_FILES/0511-N-extra.xlsx")
    if test_file.exists():
        try:
            processor = ExcelProcessor()
            with open(test_file, 'rb') as f:
                processed_data = processor.process_excel(f)
            
            print(f"📄 Analyzing: {test_file.name}")
            
            # Title data
            title_data = processed_data.get('title_data', {})
            print(f"\n📋 Title Data ({len(title_data)} entries):")
            key_fields = [
                'Name of Contractor or supplier :',
                'Agreement No.',
                'Name of Work ;-)',
                'Date of Commencement',
                'Date of Completion',
                'WORK ORDER AMOUNT RS.'
            ]
            
            for key in key_fields:
                if key in title_data:
                    print(f"   {key}: {title_data[key]}")
            
            # Work order data
            work_order_data = processed_data.get('work_order_data', [])
            if work_order_data:
                print(f"\n📊 Work Order Data:")
                print(f"   Entries: {len(work_order_data)}")
                # Show first few items if it's a list
                if isinstance(work_order_data, list) and len(work_order_data) > 0:
                    print(f"   Sample items:")
                    for i, item in enumerate(work_order_data[:3]):
                        print(f"     {i+1}. {item}")
            
            # Extra items data
            extra_items_data = processed_data.get('extra_items_data', [])
            if extra_items_data:
                print(f"\n➕ Extra Items Data:")
                print(f"   Entries: {len(extra_items_data)}")
                if isinstance(extra_items_data, list) and len(extra_items_data) > 0:
                    print(f"   Sample items:")
                    for i, item in enumerate(extra_items_data[:3]):
                        print(f"     {i+1}. {item}")
            
        except Exception as e:
            print(f"❌ Error analyzing sample data: {e}")

if __name__ == "__main__":
    try:
        # Show sample data analysis
        show_sample_data_analysis()
        
        # Run batch processing
        results = batch_process_simple_scrutiny()
        
        print(f"\n🎉 Batch test completed!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()
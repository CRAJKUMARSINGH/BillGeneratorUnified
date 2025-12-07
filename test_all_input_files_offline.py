#!/usr/bin/env python3
"""
Comprehensive Offline Test - Process all input files from TEST_INPUT_FILES
Generates complete bill outputs (HTML and PDF) for all test files
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import traceback
import time

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

def process_file_complete(input_file, output_base_dir):
    """Process a single file completely - generate all documents"""
    print(f"\n{'='*70}")
    print(f"Processing: {input_file.name}")
    print(f"{'='*70}")
    
    result = {
        'input_file': str(input_file),
        'filename': input_file.name,
        'status': 'pending',
        'error': None,
        'processing_time': 0,
        'html_files': [],
        'pdf_files': [],
        'output_folder': None,
        'timestamp': datetime.now().isoformat()
    }
    
    start_time = time.time()
    
    try:
        from core.processors.excel_processor import ExcelProcessor
        from core.generators.document_generator import DocumentGenerator
        
        # Step 1: Process Excel file
        print("[1/4] Processing Excel file...")
        excel_processor = ExcelProcessor()
        processed_data = excel_processor.process_excel(str(input_file))
        print(f"     [OK] Excel processed successfully")
        
        # Step 2: Generate HTML documents
        print("[2/4] Generating HTML documents...")
        doc_generator = DocumentGenerator(processed_data)
        html_documents = doc_generator.generate_all_documents()
        print(f"     [OK] Generated {len(html_documents)} HTML document(s)")
        result['html_files'] = list(html_documents.keys())
        
        # Step 3: Generate PDF documents
        print("[3/4] Generating PDF documents...")
        try:
            from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator
            print("     Using Enhanced PDF Generator...")
            pdf_gen = EnhancedPDFGenerator()
            pdf_documents_bytes = pdf_gen.batch_convert(
                html_documents,
                zoom=1.0,
                disable_smart_shrinking=True
            )
            pdf_documents = {f"{name}.pdf": content for name, content in pdf_documents_bytes.items()}
        except Exception as e:
            print(f"     Enhanced PDF Generator not available, using fallback: {e}")
            pdf_documents = doc_generator.create_pdf_documents(html_documents)
        
        print(f"     [OK] Generated {len(pdf_documents)} PDF document(s)")
        result['pdf_files'] = list(pdf_documents.keys())
        
        # Step 4: Save all files to output folder
        print("[4/4] Saving output files...")
        
        # Create timestamped output folder for this file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_stem = input_file.stem
        output_folder = output_base_dir / f"{timestamp}_{file_stem}"
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Save HTML files
        html_folder = output_folder / "html"
        html_folder.mkdir(exist_ok=True)
        for doc_name, html_content in html_documents.items():
            html_file = html_folder / f"{doc_name}.html"
            html_file.write_text(html_content, encoding='utf-8')
        
        # Save PDF files
        pdf_folder = output_folder / "pdf"
        pdf_folder.mkdir(exist_ok=True)
        for doc_name, pdf_content in pdf_documents.items():
            pdf_file = pdf_folder / doc_name
            pdf_file.write_bytes(pdf_content)
        
        result['output_folder'] = str(output_folder)
        result['status'] = 'success'
        result['processing_time'] = time.time() - start_time
        
        print(f"     [OK] Files saved to: {output_folder}")
        print(f"     [OK] Processing complete in {result['processing_time']:.2f} seconds")
        
        # Show summary
        title_data = processed_data.get('title_data', {})
        totals = processed_data.get('totals', {})
        if title_data:
            print(f"\n     Summary:")
            if 'Project Name' in title_data:
                print(f"       Project: {title_data['Project Name']}")
            if 'Work Order No' in title_data:
                print(f"       Work Order: {title_data['Work Order No']}")
            if totals:
                net_payable = totals.get('net_payable', totals.get('grand_total', 0))
                print(f"       Net Payable: Rs. {net_payable:,.2f}")
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        result['traceback'] = traceback.format_exc()
        result['processing_time'] = time.time() - start_time
        print(f"[ERROR] {str(e)}")
        traceback.print_exc()
    
    return result

def main():
    """Main function to process all test files"""
    print("="*70)
    print("COMPREHENSIVE OFFLINE TEST - ALL INPUT FILES")
    print("="*70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Setup directories
    test_input_dir = Path('TEST_INPUT_FILES')
    output_base_dir = Path('test_output_complete')
    output_base_dir.mkdir(exist_ok=True)
    
    if not test_input_dir.exists():
        print(f"\n[ERROR] Test input directory not found: {test_input_dir}")
        print(f"Please ensure TEST_INPUT_FILES folder exists with test Excel files")
        return
    
    # Get all input files
    input_files = list(test_input_dir.glob('*.xlsx')) + list(test_input_dir.glob('*.xls'))
    
    if not input_files:
        print(f"\n[WARNING] No Excel files found in {test_input_dir}")
        return
    
    print(f"\nInput Directory: {test_input_dir}")
    print(f"Output Directory: {output_base_dir}")
    print(f"\nFound {len(input_files)} input file(s):")
    for i, file in enumerate(sorted(input_files), 1):
        size_kb = file.stat().st_size / 1024
        print(f"   {i}. {file.name} ({size_kb:.1f} KB)")
    
    print(f"\n{'='*70}")
    print("Starting batch processing...")
    print(f"{'='*70}\n")
    
    # Process each file
    results = []
    total_start_time = time.time()
    
    for i, input_file in enumerate(sorted(input_files), 1):
        print(f"\n[{i}/{len(input_files)}]")
        result = process_file_complete(input_file, output_base_dir)
        results.append(result)
    
    total_time = time.time() - total_start_time
    
    # Generate comprehensive report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = output_base_dir / f"test_report_{timestamp}.json"
    summary_file = output_base_dir / f"test_summary_{timestamp}.txt"
    
    # Calculate statistics
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] == 'error')
    total_html = sum(len(r.get('html_files', [])) for r in results if r['status'] == 'success')
    total_pdf = sum(len(r.get('pdf_files', [])) for r in results if r['status'] == 'success')
    avg_time = sum(r.get('processing_time', 0) for r in results) / len(results) if results else 0
    
    # Save JSON report
    report_data = {
        'test_info': {
            'timestamp': datetime.now().isoformat(),
            'input_directory': str(test_input_dir),
            'output_directory': str(output_base_dir),
            'total_files': len(input_files),
            'success_count': success_count,
            'error_count': error_count,
            'total_processing_time': total_time,
            'average_time_per_file': avg_time
        },
        'statistics': {
            'total_html_files': total_html,
            'total_pdf_files': total_pdf,
            'success_rate': (success_count / len(input_files) * 100) if input_files else 0
        },
        'results': results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    # Generate text summary
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("COMPREHENSIVE OFFLINE TEST - SUMMARY REPORT\n")
        f.write("="*70 + "\n\n")
        f.write(f"Test Run: {timestamp}\n")
        f.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Input Directory: {test_input_dir}\n")
        f.write(f"Output Directory: {output_base_dir}\n\n")
        
        f.write("-"*70 + "\n")
        f.write("OVERALL STATISTICS\n")
        f.write("-"*70 + "\n\n")
        f.write(f"Total Files Processed: {len(input_files)}\n")
        f.write(f"Success: {success_count}\n")
        f.write(f"Errors: {error_count}\n")
        f.write(f"Success Rate: {report_data['statistics']['success_rate']:.1f}%\n")
        f.write(f"Total Processing Time: {total_time:.2f} seconds\n")
        f.write(f"Average Time per File: {avg_time:.2f} seconds\n")
        f.write(f"Total HTML Files Generated: {total_html}\n")
        f.write(f"Total PDF Files Generated: {total_pdf}\n\n")
        
        f.write("-"*70 + "\n")
        f.write("DETAILED RESULTS\n")
        f.write("-"*70 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"{i}. {result['filename']}\n")
            f.write(f"   Status: {result['status'].upper()}\n")
            f.write(f"   Processing Time: {result.get('processing_time', 0):.2f} seconds\n")
            
            if result['status'] == 'success':
                f.write(f"   Output Folder: {Path(result['output_folder']).name}\n")
                f.write(f"   HTML Files ({len(result.get('html_files', []))}):\n")
                for html_file in result.get('html_files', []):
                    f.write(f"     - {html_file}.html\n")
                f.write(f"   PDF Files ({len(result.get('pdf_files', []))}):\n")
                for pdf_file in result.get('pdf_files', []):
                    f.write(f"     - {pdf_file}\n")
            else:
                f.write(f"   Error: {result.get('error', 'Unknown error')}\n")
            
            f.write("\n")
        
        if error_count > 0:
            f.write("-"*70 + "\n")
            f.write("ERROR DETAILS\n")
            f.write("-"*70 + "\n\n")
            for result in results:
                if result['status'] == 'error':
                    f.write(f"File: {result['filename']}\n")
                    f.write(f"Error: {result.get('error', 'Unknown')}\n")
                    if 'traceback' in result:
                        f.write(f"Traceback:\n{result['traceback']}\n")
                    f.write("\n")
    
    # Print summary to console
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print(f"\nTotal Files: {len(input_files)}")
    print(f"[SUCCESS] Success: {success_count}")
    print(f"[ERROR] Errors: {error_count}")
    print(f"Success Rate: {report_data['statistics']['success_rate']:.1f}%")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Average Time per File: {avg_time:.2f} seconds")
    print(f"Total HTML Files: {total_html}")
    print(f"Total PDF Files: {total_pdf}")
    print(f"\nOutput Directory: {output_base_dir}")
    print(f"JSON Report: {report_file.name}")
    print(f"Text Summary: {summary_file.name}")
    
    if success_count > 0:
        print(f"\n[SUCCESS] Successfully processed files:")
        for result in results:
            if result['status'] == 'success':
                print(f"   - {result['filename']} -> {Path(result['output_folder']).name}")
    
    if error_count > 0:
        print(f"\n[ERROR] Files with errors:")
        for result in results:
            if result['status'] == 'error':
                print(f"   - {result['filename']}: {result.get('error', 'Unknown error')}")
    
    print("="*70)

if __name__ == "__main__":
    main()


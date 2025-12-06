"""
Batch Test Script for Note Sheet Generation
Processes all test input files and generates note sheets with reports
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
from core.generators.document_generator import DocumentGenerator

def format_date(value):
    """Format date value for display"""
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime('%d/%m/%Y')
    if isinstance(value, str):
        try:
            # Try to parse and format
            dt = datetime.strptime(value, '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except:
            return value
    return str(value)

def generate_notes_from_data(data):
    """Generate notes similar to VBA macro logic"""
    notes = []
    serial = 1
    
    totals = data.get('totals', {})
    title_data = data.get('title_data', {})
    
    work_order_amount = totals.get('work_order_amount', 0)
    last_bill_amount = totals.get('last_bill_amount', 0)
    this_bill_amount = totals.get('net_payable', totals.get('grand_total', 0))
    upto_date_amount = last_bill_amount + this_bill_amount
    
    # Calculate percentage
    if work_order_amount > 0:
        percentage = (upto_date_amount / work_order_amount) * 100
    else:
        percentage = 0
    
    # Note 1: Percentage completion
    notes.append(f"{serial}. The work has been completed {percentage:.2f}% of the Work Order Amount.")
    serial += 1
    
    # Note 2-4: Deviation based on percentage
    if percentage < 90:
        notes.append(f"{serial}. The execution of work at final stage is less than 90% of the Work Order Amount, the Requisite Deviation Statement is enclosed to observe check on unuseful expenditure. Approval of the Deviation is having jurisdiction under this office.")
        serial += 1
    elif percentage > 100 and percentage <= 105:
        notes.append(f"{serial}. Requisite Deviation Statement is enclosed. The Overall Excess is less than or equal to 5% and is having approval jurisdiction under this office.")
        serial += 1
    elif percentage > 105:
        notes.append(f"{serial}. Requisite Deviation Statement is enclosed. The Overall Excess is more than 5% and Approval of the Deviation Case is required from the Superintending Engineer, PWD Electrical Circle, Udaipur.")
        serial += 1
    
    # Note 5-7: Delay handling
    date_commencement = title_data.get('Date of Commencement', '')
    date_completion = title_data.get('Date of Completion', '')
    actual_completion = title_data.get('Actual Date of Completion', '')
    
    if date_commencement and date_completion:
        try:
            if isinstance(date_commencement, str):
                start_date = datetime.strptime(date_commencement, '%Y-%m-%d')
            else:
                start_date = date_commencement
            
            if isinstance(date_completion, str):
                sched_date = datetime.strptime(date_completion, '%Y-%m-%d')
            else:
                sched_date = date_completion
            
            time_allowed = (sched_date - start_date).days
            
            if actual_completion:
                if isinstance(actual_completion, str):
                    actual_date = datetime.strptime(actual_completion, '%Y-%m-%d')
                else:
                    actual_date = actual_completion
                
                delay_days = (actual_date - sched_date).days
                
                if delay_days > 0:
                    notes.append(f"{serial}. Time allowed for completion of the work was {time_allowed} days. The Work was delayed by {delay_days} days.")
                    serial += 1
                    
                    if delay_days > (0.5 * time_allowed):
                        notes.append(f"{serial}. Approval of the Time Extension Case is required from the Superintending Engineer, PWD Electrical Circle, Udaipur.")
                    else:
                        notes.append(f"{serial}. Approval of the Time Extension Case is to be done by this office.")
                    serial += 1
                else:
                    notes.append(f"{serial}. Work was completed in time.")
                    serial += 1
        except Exception as e:
            pass  # Skip date calculations if parsing fails
    
    # Note 8-9: Extra items
    extra_items_sum = totals.get('extra_items_sum', 0)
    if extra_items_sum and extra_items_sum > 0:
        extra_percentage = (extra_items_sum / work_order_amount * 100) if work_order_amount > 0 else 0
        if extra_percentage > 5:
            notes.append(f"{serial}. The amount of Extra items is Rs. {extra_items_sum:,.2f} which is {extra_percentage:.2f}% of the Work Order Amount; exceed 5%, require approval from the Superintending Engineer, PWD Electrical Circle, Udaipur.")
        else:
            notes.append(f"{serial}. The amount of Extra items is Rs. {extra_items_sum:,.2f} which is {extra_percentage:.2f}% of the Work Order Amount; under 5%, approval of the same is to be granted by this office.")
        serial += 1
    
    # Note 10: Excess quantity
    excess_quantity = title_data.get('Excess Quantity', 'No')
    if excess_quantity and str(excess_quantity).lower() in ['yes', 'y']:
        if percentage <= 100:
            saving = 100 - percentage
            notes.append(f"{serial}. The details of the items wherein EXCESS QUANTITY has been executed during the work completion are attached. There is a saving in the work of the tune of {saving:.2f}%; (i.e., Overall Excess = NIL, just excess quantity items are recorded), the approval of which falls under the jurisdiction of this office.")
        else:
            excess = percentage - 100
            notes.append(f"{serial}. The details of the items wherein EXCESS QUANTITY has been executed during the work completion are attached. There is an Overall excess of {excess:.2f}% requires approval as already narrated.")
        serial += 1
    
    # Note 11: QC reports (mandatory)
    notes.append(f"{serial}. Quality Control (QC) test reports attached.")
    serial += 1
    
    # Note 12: Hand over statement
    repair_work = title_data.get('Repair Work', 'No')
    if repair_work and str(repair_work).lower() not in ['yes', 'y']:
        notes.append(f"{serial}. A copy of Hand Over statement duly signed by client department representative is attached.")
        serial += 1
    
    # Note 13: Delay comment
    delay_comment = title_data.get('Delay Comment', 'No')
    if delay_comment and str(delay_comment).lower() in ['yes', 'y']:
        notes.append(f"{serial}. The Bill is submitted very late; explanation from concerned Assistant Engineer may be sought.")
        serial += 1
    
    # Final note
    notes.append(f"{serial}. Please peruse above details for necessary decision-making.")
    notes.append(" ")
    notes.append("                      Premlata Jain")
    notes.append("                     AAO- As Auditor")
    
    return notes

def process_file(input_file, output_dir):
    """Process a single input file and generate note sheet"""
    print(f"\n{'='*70}")
    print(f"Processing: {input_file.name}")
    print(f"{'='*70}")
    
    result = {
        'input_file': str(input_file),
        'status': 'pending',
        'error': None,
        'title_data': {},
        'totals': {},
        'notes_count': 0,
        'output_file': None,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Process Excel file
        processor = ExcelProcessor()
        processed_data = processor.process_excel(str(input_file))
        
        # Extract title data
        title_data = processed_data.get('title_data', {})
        result['title_data'] = {k: str(v) for k, v in title_data.items()}
        
        # Generate documents
        generator = DocumentGenerator(processed_data)
        template_data = generator.template_data
        
        # Generate notes
        notes = generate_notes_from_data(template_data)
        template_data['notes'] = notes
        result['notes_count'] = len(notes)
        
        # Get totals
        totals = template_data.get('totals', {})
        result['totals'] = {
            'work_order_amount': totals.get('work_order_amount', 0),
            'last_bill_amount': totals.get('last_bill_amount', 0),
            'this_bill_amount': totals.get('net_payable', totals.get('grand_total', 0)),
            'upto_date_amount': totals.get('last_bill_amount', 0) + totals.get('net_payable', totals.get('grand_total', 0)),
            'extra_items_sum': totals.get('extra_items_sum', 0),
            'total_deductions': totals.get('total_deductions', 0),
            'net_payable': totals.get('net_payable', totals.get('grand_total', 0))
        }
        
        # Generate note sheet HTML
        note_sheet_html = generator._render_template('note_sheet.html')
        
        # Save HTML file
        output_file = output_dir / f"{input_file.stem}_notesheet.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(note_sheet_html)
        
        result['output_file'] = str(output_file)
        result['status'] = 'success'
        
        print(f"[OK] Generated: {output_file.name}")
        print(f"     Notes: {len(notes)} items")
        print(f"     Work Order: Rs. {result['totals']['work_order_amount']:,.2f}")
        print(f"     This Bill: Rs. {result['totals']['this_bill_amount']:,.2f}")
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        result['traceback'] = traceback.format_exc()
        print(f"[ERROR] {str(e)}")
        traceback.print_exc()
    
    return result

def main():
    """Main function to process all test files"""
    print("="*70)
    print("BATCH TEST: NOTE SHEET GENERATION")
    print("="*70)
    
    # Setup directories
    test_input_dir = Path('TEST_INPUT_FILES')
    output_base_dir = Path('notesheet_test_output')
    output_base_dir.mkdir(exist_ok=True)
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = output_base_dir / f"test_run_{timestamp}"
    output_dir.mkdir(exist_ok=True)
    
    print(f"\nInput Directory: {test_input_dir}")
    print(f"Output Directory: {output_dir}")
    
    # Get all input files
    input_files = list(test_input_dir.glob('*.xlsx'))
    
    if not input_files:
        print(f"\n[WARNING] No .xlsx files found in {test_input_dir}")
        return
    
    print(f"\nFound {len(input_files)} input files")
    
    # Process each file
    results = []
    for input_file in sorted(input_files):
        result = process_file(input_file, output_dir)
        results.append(result)
    
    # Generate summary report
    report_file = output_dir / 'test_report.json'
    summary_file = output_dir / 'test_summary.txt'
    
    # Save JSON report
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_files': len(input_files),
            'results': results
        }, f, indent=2, default=str)
    
    # Generate text summary
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("NOTE SHEET GENERATION - TEST SUMMARY\n")
        f.write("="*70 + "\n\n")
        f.write(f"Test Run: {timestamp}\n")
        f.write(f"Total Files Processed: {len(input_files)}\n\n")
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = sum(1 for r in results if r['status'] == 'error')
        
        f.write(f"Success: {success_count}\n")
        f.write(f"Errors: {error_count}\n\n")
        
        f.write("-"*70 + "\n")
        f.write("DETAILED RESULTS\n")
        f.write("-"*70 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"{i}. {Path(result['input_file']).name}\n")
            f.write(f"   Status: {result['status'].upper()}\n")
            
            if result['status'] == 'success':
                f.write(f"   Output: {Path(result['output_file']).name}\n")
                f.write(f"   Notes Generated: {result['notes_count']}\n")
                f.write(f"   Work Order Amount: Rs. {result['totals']['work_order_amount']:,.2f}\n")
                f.write(f"   This Bill Amount: Rs. {result['totals']['this_bill_amount']:,.2f}\n")
                f.write(f"   Extra Items: Rs. {result['totals']['extra_items_sum']:,.2f}\n")
                
                # Show key title data
                title_data = result.get('title_data', {})
                if title_data:
                    f.write(f"   Key Fields:\n")
                    for key in ['Agreement No', 'Work Order No', 'Project Name', 'Contractor Name']:
                        if key in title_data:
                            f.write(f"     - {key}: {title_data[key]}\n")
            else:
                f.write(f"   Error: {result['error']}\n")
            
            f.write("\n")
        
        # Summary statistics
        f.write("-"*70 + "\n")
        f.write("STATISTICS\n")
        f.write("-"*70 + "\n\n")
        
        if success_count > 0:
            successful_results = [r for r in results if r['status'] == 'success']
            total_notes = sum(r['notes_count'] for r in successful_results)
            avg_notes = total_notes / success_count if success_count > 0 else 0
            
            total_work_order = sum(r['totals']['work_order_amount'] for r in successful_results)
            total_this_bill = sum(r['totals']['this_bill_amount'] for r in successful_results)
            
            f.write(f"Average Notes per File: {avg_notes:.1f}\n")
            f.write(f"Total Work Order Amount: Rs. {total_work_order:,.2f}\n")
            f.write(f"Total This Bill Amount: Rs. {total_this_bill:,.2f}\n")
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print(f"\nResults saved to: {output_dir}")
    print(f"  - JSON Report: {report_file.name}")
    print(f"  - Text Summary: {summary_file.name}")
    print(f"  - HTML Files: {len([r for r in results if r['status'] == 'success'])} files")
    
    # Print summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    print(f"\nSummary:")
    print(f"  Success: {success_count}/{len(input_files)}")
    print(f"  Errors: {error_count}/{len(input_files)}")

if __name__ == "__main__":
    main()


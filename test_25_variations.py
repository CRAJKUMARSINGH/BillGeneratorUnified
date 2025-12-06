"""
Test the updated XLSM file with 25 different variations
"""
import win32com.client
import os
from datetime import datetime, timedelta
import random
import json

# Test scenarios with different conditions
test_scenarios = [
    # Scenario 1: Normal completion, no delay, no extra items
    {
        "name": "Normal Completion - On Time",
        "work_order_amount": 500000,
        "upto_last_bill": 0,
        "this_bill_amount": 500000,
        "start_date": "2024-01-01",
        "schedule_completion": "2024-06-30",
        "actual_completion": "2024-06-30",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 2: Work completed with slight delay
    {
        "name": "Slight Delay - 10 days",
        "work_order_amount": 750000,
        "upto_last_bill": 300000,
        "this_bill_amount": 450000,
        "start_date": "2024-02-01",
        "schedule_completion": "2024-08-31",
        "actual_completion": "2024-09-10",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 3: Major delay (>50% of allowed time)
    {
        "name": "Major Delay - Requires SE Approval",
        "work_order_amount": 1000000,
        "upto_last_bill": 500000,
        "this_bill_amount": 500000,
        "start_date": "2024-01-15",
        "schedule_completion": "2024-07-15",
        "actual_completion": "2024-11-15",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "Yes"
    },
    # Scenario 4: Work with extra items <5%
    {
        "name": "Extra Items Under 5%",
        "work_order_amount": 800000,
        "upto_last_bill": 400000,
        "this_bill_amount": 430000,
        "start_date": "2024-03-01",
        "schedule_completion": "2024-09-01",
        "actual_completion": "2024-09-01",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 30000,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 5: Work with extra items >5%
    {
        "name": "Extra Items Over 5% - Requires SE Approval",
        "work_order_amount": 600000,
        "upto_last_bill": 200000,
        "this_bill_amount": 450000,
        "start_date": "2024-04-01",
        "schedule_completion": "2024-10-01",
        "actual_completion": "2024-10-01",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 50000,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 6: Work <90% complete
    {
        "name": "Less than 90% Complete",
        "work_order_amount": 1000000,
        "upto_last_bill": 400000,
        "this_bill_amount": 450000,
        "start_date": "2024-01-01",
        "schedule_completion": "2024-12-31",
        "actual_completion": "2024-12-31",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 7: Work 100-105% complete
    {
        "name": "Excess 100-105%",
        "work_order_amount": 500000,
        "upto_last_bill": 250000,
        "this_bill_amount": 265000,
        "start_date": "2024-02-01",
        "schedule_completion": "2024-08-01",
        "actual_completion": "2024-08-01",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "Yes",
        "delay_comment": "No"
    },
    # Scenario 8: Work >105% complete
    {
        "name": "Excess Over 105% - Requires SE Approval",
        "work_order_amount": 400000,
        "upto_last_bill": 200000,
        "this_bill_amount": 250000,
        "start_date": "2024-03-01",
        "schedule_completion": "2024-09-01",
        "actual_completion": "2024-09-01",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "Yes",
        "delay_comment": "No"
    },
    # Scenario 9: Repair work
    {
        "name": "Repair Work",
        "work_order_amount": 300000,
        "upto_last_bill": 150000,
        "this_bill_amount": 150000,
        "start_date": "2024-05-01",
        "schedule_completion": "2024-11-01",
        "actual_completion": "2024-11-01",
        "repair_work": "Yes",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 10: Multiple issues - delay + extra items + excess
    {
        "name": "Complex Case - Multiple Issues",
        "work_order_amount": 900000,
        "upto_last_bill": 450000,
        "this_bill_amount": 520000,
        "start_date": "2024-01-10",
        "schedule_completion": "2024-07-10",
        "actual_completion": "2024-10-10",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 70000,
        "excess_quantity": "Yes",
        "delay_comment": "Yes"
    },
    # Scenario 11: Small project completed early
    {
        "name": "Small Project - Early Completion",
        "work_order_amount": 150000,
        "upto_last_bill": 0,
        "this_bill_amount": 150000,
        "start_date": "2024-06-01",
        "schedule_completion": "2024-09-01",
        "actual_completion": "2024-08-15",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 12: Large project with multiple bills
    {
        "name": "Large Project - Multiple Bills",
        "work_order_amount": 5000000,
        "upto_last_bill": 3500000,
        "this_bill_amount": 1500000,
        "start_date": "2023-01-01",
        "schedule_completion": "2024-12-31",
        "actual_completion": "2024-12-31",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 100000,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 13: Minimal delay with extra items
    {
        "name": "Minimal Delay + Extra Items",
        "work_order_amount": 650000,
        "upto_last_bill": 325000,
        "this_bill_amount": 340000,
        "start_date": "2024-02-15",
        "schedule_completion": "2024-08-15",
        "actual_completion": "2024-08-20",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 15000,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 14: Exactly 100% completion
    {
        "name": "Exactly 100% Complete",
        "work_order_amount": 850000,
        "upto_last_bill": 425000,
        "this_bill_amount": 425000,
        "start_date": "2024-03-15",
        "schedule_completion": "2024-09-15",
        "actual_completion": "2024-09-15",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 15: First bill only
    {
        "name": "First Bill - No Previous Payment",
        "work_order_amount": 450000,
        "upto_last_bill": 0,
        "this_bill_amount": 225000,
        "start_date": "2024-04-01",
        "schedule_completion": "2024-10-01",
        "actual_completion": "2024-10-01",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 16: Final bill with savings
    {
        "name": "Final Bill - With Savings",
        "work_order_amount": 700000,
        "upto_last_bill": 350000,
        "this_bill_amount": 280000,
        "start_date": "2024-01-20",
        "schedule_completion": "2024-07-20",
        "actual_completion": "2024-07-20",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "Yes",
        "delay_comment": "No"
    },
    # Scenario 17: Moderate delay with excess quantity
    {
        "name": "Moderate Delay + Excess Quantity",
        "work_order_amount": 550000,
        "upto_last_bill": 275000,
        "this_bill_amount": 300000,
        "start_date": "2024-02-10",
        "schedule_completion": "2024-08-10",
        "actual_completion": "2024-09-01",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "Yes",
        "delay_comment": "No"
    },
    # Scenario 18: Very large project
    {
        "name": "Very Large Project",
        "work_order_amount": 10000000,
        "upto_last_bill": 7500000,
        "this_bill_amount": 2500000,
        "start_date": "2023-06-01",
        "schedule_completion": "2025-05-31",
        "actual_completion": "2025-05-31",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 250000,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 19: Short duration project
    {
        "name": "Short Duration - 60 Days",
        "work_order_amount": 200000,
        "upto_last_bill": 0,
        "this_bill_amount": 200000,
        "start_date": "2024-07-01",
        "schedule_completion": "2024-08-30",
        "actual_completion": "2024-08-30",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 20: Delayed submission
    {
        "name": "Late Bill Submission",
        "work_order_amount": 480000,
        "upto_last_bill": 240000,
        "this_bill_amount": 240000,
        "start_date": "2024-01-05",
        "schedule_completion": "2024-07-05",
        "actual_completion": "2024-07-05",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "Yes"
    },
    # Scenario 21: All conditions present
    {
        "name": "All Conditions - Worst Case",
        "work_order_amount": 800000,
        "upto_last_bill": 400000,
        "this_bill_amount": 480000,
        "start_date": "2024-01-01",
        "schedule_completion": "2024-06-30",
        "actual_completion": "2024-12-31",
        "repair_work": "Yes",
        "extra_item": "Yes",
        "extra_item_amount": 80000,
        "excess_quantity": "Yes",
        "delay_comment": "Yes"
    },
    # Scenario 22: Minimal project
    {
        "name": "Minimal Project - 50K",
        "work_order_amount": 50000,
        "upto_last_bill": 0,
        "this_bill_amount": 50000,
        "start_date": "2024-08-01",
        "schedule_completion": "2024-09-30",
        "actual_completion": "2024-09-30",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 23: Three bills scenario
    {
        "name": "Third Bill - Progressive Payment",
        "work_order_amount": 1200000,
        "upto_last_bill": 800000,
        "this_bill_amount": 400000,
        "start_date": "2023-10-01",
        "schedule_completion": "2024-09-30",
        "actual_completion": "2024-09-30",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 40000,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 24: Exactly at 5% extra items threshold
    {
        "name": "Exactly 5% Extra Items",
        "work_order_amount": 600000,
        "upto_last_bill": 300000,
        "this_bill_amount": 330000,
        "start_date": "2024-03-01",
        "schedule_completion": "2024-09-01",
        "actual_completion": "2024-09-01",
        "repair_work": "No",
        "extra_item": "Yes",
        "extra_item_amount": 30000,
        "excess_quantity": "No",
        "delay_comment": "No"
    },
    # Scenario 25: Exactly at 105% completion threshold
    {
        "name": "Exactly 105% Complete",
        "work_order_amount": 400000,
        "upto_last_bill": 200000,
        "this_bill_amount": 220000,
        "start_date": "2024-04-15",
        "schedule_completion": "2024-10-15",
        "actual_completion": "2024-10-15",
        "repair_work": "No",
        "extra_item": "No",
        "extra_item_amount": 0,
        "excess_quantity": "Yes",
        "delay_comment": "No"
    }
]

def fill_excel_data(ws, scenario):
    """Fill Excel sheet with test data"""
    # Fill basic information
    ws.Range("C5").Value = f"AGR-{random.randint(1000, 9999)}/2024"
    ws.Range("C13").Value = datetime.strptime(scenario["start_date"], "%Y-%m-%d")
    ws.Range("C14").Value = datetime.strptime(scenario["schedule_completion"], "%Y-%m-%d")
    ws.Range("C15").Value = datetime.strptime(scenario["actual_completion"], "%Y-%m-%d")
    
    # Fill amounts
    ws.Range("C18").Value = scenario["work_order_amount"]
    ws.Range("C19").Value = scenario["upto_last_bill"]
    ws.Range("C20").Value = scenario["this_bill_amount"]
    
    # Fill other fields
    ws.Range("C22").Value = scenario["repair_work"]
    ws.Range("C23").Value = scenario["extra_item"]
    ws.Range("C24").Value = scenario["extra_item_amount"]
    ws.Range("C25").Value = scenario["excess_quantity"]
    ws.Range("C26").Value = scenario["delay_comment"]

def validate_output(scenario, output_text):
    """Validate the generated output against expected conditions"""
    results = {
        "scenario": scenario["name"],
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # Calculate expected values
    work_order = scenario["work_order_amount"]
    total_expenditure = scenario["upto_last_bill"] + scenario["this_bill_amount"]
    percentage_done = (total_expenditure / work_order * 100) if work_order > 0 else 0
    
    start = datetime.strptime(scenario["start_date"], "%Y-%m-%d")
    schedule = datetime.strptime(scenario["schedule_completion"], "%Y-%m-%d")
    actual = datetime.strptime(scenario["actual_completion"], "%Y-%m-%d")
    
    time_allowed = (schedule - start).days
    delay_days = (actual - schedule).days
    
    # Check 1: Percentage calculation
    if f"{percentage_done:.2f}%" in output_text:
        results["passed"].append(f"✓ Correct percentage: {percentage_done:.2f}%")
    else:
        results["failed"].append(f"✗ Percentage not found or incorrect (expected {percentage_done:.2f}%)")
    
    # Check 2: Deviation statement for <90%
    if percentage_done < 90:
        if "less than 90%" in output_text and "Deviation Statement" in output_text:
            results["passed"].append("✓ Correct deviation statement for <90%")
        else:
            results["failed"].append("✗ Missing deviation statement for <90% completion")
    
    # Check 3: Deviation for 100-105%
    if 100 < percentage_done <= 105:
        if "less than or equal to 5%" in output_text:
            results["passed"].append("✓ Correct deviation for 100-105%")
        else:
            results["failed"].append("✗ Missing or incorrect deviation for 100-105%")
    
    # Check 4: SE approval for >105%
    if percentage_done > 105:
        if "more than 5%" in output_text and "Superintending Engineer" in output_text:
            results["passed"].append("✓ Correct SE approval requirement for >105%")
        else:
            results["failed"].append("✗ Missing SE approval requirement for >105%")
    
    # Check 5: Delay handling
    if delay_days > 0:
        if f"{delay_days} days" in output_text:
            results["passed"].append(f"✓ Correct delay days: {delay_days}")
        else:
            results["failed"].append(f"✗ Delay days not found (expected {delay_days})")
        
        # Check SE approval for major delay
        if delay_days > (0.5 * time_allowed):
            if "Superintending Engineer" in output_text:
                results["passed"].append("✓ SE approval required for major delay")
            else:
                results["failed"].append("✗ Missing SE approval for major delay")
    else:
        if "completed in time" in output_text:
            results["passed"].append("✓ Correctly identified on-time completion")
        else:
            results["failed"].append("✗ Should mention on-time completion")
    
    # Check 6: Extra items
    if scenario["extra_item"] == "Yes":
        extra_percentage = (scenario["extra_item_amount"] / work_order * 100) if work_order > 0 else 0
        if f"Rs. {scenario['extra_item_amount']}" in output_text or f"Rs..{scenario['extra_item_amount']}" in output_text:
            results["passed"].append(f"✓ Extra item amount mentioned: Rs. {scenario['extra_item_amount']}")
        else:
            results["warnings"].append(f"⚠ Extra item amount format may vary")
        
        if extra_percentage > 5:
            if "exceed 5%" in output_text and "Superintending Engineer" in output_text:
                results["passed"].append("✓ SE approval required for extra items >5%")
            else:
                results["failed"].append("✗ Missing SE approval for extra items >5%")
        else:
            if "under 5%" in output_text:
                results["passed"].append("✓ Correct handling of extra items <5%")
            else:
                results["failed"].append("✗ Incorrect handling of extra items <5%")
    
    # Check 7: Excess quantity
    if scenario["excess_quantity"] == "Yes":
        if "EXCESS QUANTITY" in output_text:
            results["passed"].append("✓ Excess quantity mentioned")
        else:
            results["failed"].append("✗ Excess quantity not mentioned")
    
    # Check 8: Mandatory items
    if "Quality Control (QC) test reports" in output_text:
        results["passed"].append("✓ QC test reports mentioned")
    else:
        results["failed"].append("✗ Missing QC test reports mention")
    
    # Check 9: Hand over statement
    if scenario["repair_work"] == "No":
        if "Hand Over statement" in output_text:
            results["passed"].append("✓ Hand over statement mentioned")
        else:
            results["failed"].append("✗ Missing hand over statement")
    
    # Check 10: Late submission
    if scenario["delay_comment"] == "Yes":
        if "submitted very late" in output_text:
            results["passed"].append("✓ Late submission noted")
        else:
            results["failed"].append("✗ Late submission not noted")
    
    # Check 11: Final statement
    if "Please peruse above details" in output_text:
        results["passed"].append("✓ Final statement present")
    else:
        results["failed"].append("✗ Missing final statement")
    
    # Check 12: Signature
    if "Premlata Jain" in output_text and "AAO" in output_text:
        results["passed"].append("✓ Signature block present")
    else:
        results["failed"].append("✗ Missing signature block")
    
    return results

def run_tests():
    """Run all 25 test scenarios"""
    print("="*80)
    print("TESTING XLSM FILE WITH 25 VARIATIONS")
    print("="*80)
    print()
    
    # Initialize Excel
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    
    file_path = os.path.abspath('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_UPDATED.xlsm')
    
    all_results = []
    summary = {
        "total_tests": len(test_scenarios),
        "total_checks": 0,
        "passed_checks": 0,
        "failed_checks": 0,
        "warnings": 0
    }
    
    for idx, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*80}")
        print(f"TEST {idx}/25: {scenario['name']}")
        print(f"{'='*80}")
        
        try:
            # Open workbook
            wb = xl.Workbooks.Open(file_path)
            ws = wb.Sheets("BillChecklist")
            
            # Fill data
            print(f"  Filling data...")
            fill_excel_data(ws, scenario)
            
            # Run macro
            print(f"  Running macro...")
            xl.Application.Run("GenerateBillNotes")
            
            # Get output
            output = ws.Range("B44").Value
            
            if not output:
                print(f"  ✗ ERROR: No output generated!")
                all_results.append({
                    "scenario": scenario["name"],
                    "error": "No output generated"
                })
                wb.Close(False)
                continue
            
            # Validate output
            print(f"  Validating output...")
            results = validate_output(scenario, output)
            all_results.append(results)
            
            # Print results
            print(f"\n  Results:")
            for check in results["passed"]:
                print(f"    {check}")
                summary["passed_checks"] += 1
                summary["total_checks"] += 1
            
            for check in results["failed"]:
                print(f"    {check}")
                summary["failed_checks"] += 1
                summary["total_checks"] += 1
            
            for warning in results["warnings"]:
                print(f"    {warning}")
                summary["warnings"] += 1
            
            # Save output to file
            output_file = f"test_output/test_{idx:02d}_{scenario['name'].replace(' ', '_').replace('/', '_')}.txt"
            os.makedirs("test_output", exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Test Scenario: {scenario['name']}\n")
                f.write("="*80 + "\n\n")
                f.write("Input Data:\n")
                f.write(json.dumps(scenario, indent=2))
                f.write("\n\n" + "="*80 + "\n\n")
                f.write("Generated Output:\n")
                f.write(output)
            
            print(f"  ✓ Output saved to: {output_file}")
            
            # Close workbook without saving
            wb.Close(False)
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            all_results.append({
                "scenario": scenario["name"],
                "error": str(e)
            })
            try:
                wb.Close(False)
            except:
                pass
    
    # Close Excel
    xl.Quit()
    
    # Generate summary report
    print("\n\n" + "="*80)
    print("FINAL SUMMARY REPORT")
    print("="*80)
    print(f"\nTotal Test Scenarios: {summary['total_tests']}")
    print(f"Total Validation Checks: {summary['total_checks']}")
    print(f"Passed Checks: {summary['passed_checks']} ({summary['passed_checks']/summary['total_checks']*100:.1f}%)")
    print(f"Failed Checks: {summary['failed_checks']} ({summary['failed_checks']/summary['total_checks']*100:.1f}%)")
    print(f"Warnings: {summary['warnings']}")
    
    # Calculate accuracy
    accuracy = (summary['passed_checks'] / summary['total_checks'] * 100) if summary['total_checks'] > 0 else 0
    print(f"\n{'='*80}")
    print(f"OVERALL ACCURACY: {accuracy:.2f}%")
    print(f"{'='*80}")
    
    # Detailed breakdown
    print("\n\nDETAILED BREAKDOWN BY SCENARIO:")
    print("="*80)
    for idx, result in enumerate(all_results, 1):
        if "error" in result:
            print(f"\n{idx}. {result['scenario']}: ERROR - {result['error']}")
        else:
            passed = len(result["passed"])
            failed = len(result["failed"])
            total = passed + failed
            scenario_accuracy = (passed / total * 100) if total > 0 else 0
            status = "✓ PASS" if failed == 0 else "✗ FAIL" if failed > passed else "⚠ PARTIAL"
            print(f"\n{idx}. {result['scenario']}: {status}")
            print(f"   Passed: {passed}/{total} ({scenario_accuracy:.1f}%)")
            if failed > 0:
                print(f"   Failed checks:")
                for check in result["failed"]:
                    print(f"     {check}")
    
    # Save summary to file
    summary_file = "test_output/SUMMARY_REPORT.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("XLSM FILE TESTING - SUMMARY REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total Test Scenarios: {summary['total_tests']}\n")
        f.write(f"Total Validation Checks: {summary['total_checks']}\n")
        f.write(f"Passed Checks: {summary['passed_checks']} ({summary['passed_checks']/summary['total_checks']*100:.1f}%)\n")
        f.write(f"Failed Checks: {summary['failed_checks']} ({summary['failed_checks']/summary['total_checks']*100:.1f}%)\n")
        f.write(f"Warnings: {summary['warnings']}\n")
        f.write(f"\nOVERALL ACCURACY: {accuracy:.2f}%\n")
        f.write("\n" + "="*80 + "\n\n")
        f.write("DETAILED BREAKDOWN:\n\n")
        for idx, result in enumerate(all_results, 1):
            if "error" in result:
                f.write(f"{idx}. {result['scenario']}: ERROR - {result['error']}\n")
            else:
                passed = len(result["passed"])
                failed = len(result["failed"])
                total = passed + failed
                scenario_accuracy = (passed / total * 100) if total > 0 else 0
                f.write(f"{idx}. {result['scenario']}: {passed}/{total} passed ({scenario_accuracy:.1f}%)\n")
    
    print(f"\n\n✓ Summary report saved to: {summary_file}")
    print(f"✓ All test outputs saved to: test_output/")
    
    return accuracy

if __name__ == "__main__":
    accuracy = run_tests()
    print(f"\n\nFINAL RESULT: {accuracy:.2f}% ACCURACY")

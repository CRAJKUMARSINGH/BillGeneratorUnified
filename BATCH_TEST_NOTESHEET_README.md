# Batch Test Note Sheet Generation

## Overview
This script processes all test input files and generates note sheets with comprehensive reports.

## Usage

```bash
python batch_test_notesheet.py
```

## What It Does

1. **Processes All Test Files**: Automatically finds all `.xlsx` files in `TEST_INPUT_FILES/`
2. **Generates Note Sheets**: Creates HTML note sheets for each input file
3. **Incorporates Title Sheet Data**: Uses all available title sheet fields
4. **Generates Notes**: Creates notes using VBA macro logic
5. **Saves Reports**: Creates JSON and text summary reports

## Output Structure

```
notesheet_test_output/
└── test_run_YYYYMMDD_HHMMSS/
    ├── test_report.json          # Detailed JSON report
    ├── test_summary.txt          # Human-readable summary
    └── *_notesheet.html         # Generated note sheets (one per input file)
```

## Title Sheet Data Incorporation

The script incorporates title sheet data in the following fields:

### Basic Information
- Agreement No / Work Order No
- A&F Sanction
- Technical Section
- Measurement Book No & Page
- Sub Division
- Name of Work / Project Name
- Name of Contractor / Firm
- Original/Deposit
- Budget Provision

### Dates
- Date of Commencement
- Date of Completion
- Actual Date of Completion

### Additional Fields
- Delay Extension
- Notice Issued
- Repair Work
- Excess Quantity
- Delay Comment
- Liquidated Damages

## Generated Notes Logic

The notes are generated using the same logic as the VBA macro:

1. **Percentage Completion**: Calculates work completion percentage
2. **Deviation Statements**: Based on percentage (<90%, 100-105%, >105%)
3. **Delay Handling**: Calculates delays and approval requirements
4. **Extra Items**: Includes extra items notes if applicable
5. **Excess Quantity**: Handles excess quantity scenarios
6. **Mandatory Notes**: QC reports, Hand Over statements
7. **Delay Comments**: Late bill submission notes
8. **Final Note**: Decision-making note with signature

## Report Contents

### JSON Report (`test_report.json`)
Contains detailed information for each file:
- Input file path
- Status (success/error)
- Title data extracted
- Totals calculated
- Number of notes generated
- Output file path
- Error information (if any)

### Text Summary (`test_summary.txt`)
Human-readable summary including:
- Test run timestamp
- Total files processed
- Success/error counts
- Detailed results per file
- Statistics (averages, totals)

## Example Output

```
======================================================================
BATCH TEST: NOTE SHEET GENERATION
======================================================================

Input Directory: TEST_INPUT_FILES
Output Directory: notesheet_test_output\test_run_20251206_060347

Found 8 input files

======================================================================
Processing: 0511-N-extra.xlsx
======================================================================
[OK] Generated: 0511-N-extra_notesheet.html
     Notes: 8 items
     Work Order: Rs. 83,330.00
     This Bill: Rs. 87,588.16

...

Summary:
  Success: 8/8
  Errors: 0/8
```

## Features

✅ **Batch Processing**: Processes all files automatically
✅ **Title Sheet Integration**: Uses all available title sheet data
✅ **Note Generation**: Creates notes using VBA macro logic
✅ **Error Handling**: Continues processing even if one file fails
✅ **Comprehensive Reports**: JSON and text summaries
✅ **Timestamped Output**: Each test run in separate folder

## Notes

- The script uses the same note generation logic as the VBA macro
- All title sheet fields are incorporated wherever feasible
- Generated HTML files can be converted to PDF or printed
- Reports include detailed statistics and error information


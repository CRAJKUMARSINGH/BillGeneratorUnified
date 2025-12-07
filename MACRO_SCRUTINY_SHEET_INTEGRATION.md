# Macro Scrutiny Sheet Integration Guide

## Overview
This document describes the integration of the Macro Scrutiny Sheet functionality into the bill processing workflow. For each new bill process, the system automatically:

1. **Copies the template sheet** from "even BILL NOTE SHEET.xlsm" within the same workbook
2. **Renames the sheet** using format: `[First 5 words of contractor]_[Agreement Number]`
3. **Populates required cells** from the processed bill data
4. **Runs the macro button** programmatically (cell E37)
5. **Exports to PDF** with name "MACRO scrutiny SHEET IN PDF"

## Requirements

### Files Required
- **Template File**: `ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm`
  - This is the macro-enabled Excel file containing the template sheet
  - The template sheet should have a macro button in cell E37

### Python Dependencies
- `pywin32` - For COM automation with Excel
- `openpyxl` - For reading/writing Excel files
- `pandas` - For data processing (optional but recommended)

Install with:
```bash
pip install pywin32 openpyxl pandas
```

## Cell Mapping

The following cells are populated from the processed bill data:

| Cell | Data Source | Description |
|------|-------------|-------------|
| C3 | `title_data['Agreement No.']` | Agreement Number |
| C8 | `title_data['Name of Work ;-)']` | Name of Work |
| C9 | `title_data['Name of Contractor or supplier :']` | Name of Contractor |
| C12 | `title_data['Date of Commencement']` | Date of Commencement |
| C13 | `title_data['Date of Completion']` | Date of Completion |
| C14 | "WIP" (running bills) or `title_data['Date of actual completion of work :']` | Work Status |
| C17 | `totals['work_order_amount']` | Work Order Amount |
| C18 | 0 (first/final bills) or `title_data['Amount Paid Vide Last Bill']` | Last Bill Amount |
| C19 | `totals['net_payable']` | This Bill Amount |
| C29 | `totals['extra_items_sum'] + totals['tender_premium_amount']` | Sum of Extra Items + Tender Premium |

## Bill Type Logic

### C14 (Work Status)
- **Running Bills**: Shows "WIP" (Work In Progress)
- **First/Final Bills**: Shows actual completion date

### C18 (Last Bill Amount)
- **First Bill**: 0
- **Final Bill**: 0
- **Running Bill**: Amount from "Amount Paid Vide Last Bill" field in title data

### C29 (Extra Items + Tender Premium)
- Sum of all extra items plus tender premium amount
- Can be zero when no extra items

## Usage

### Basic Usage

```python
from automated_scrutiny_sheet_generator import create_scrutiny_sheet_for_bill
from core.processors.excel_processor import ExcelProcessor

# Process Excel file
processor = ExcelProcessor()
processed_data = processor.process_excel("input_file.xlsx")

# Determine bill type (you can infer from filename or data)
bill_type = "running"  # or "first" or "final"

# Create scrutiny sheet
result = create_scrutiny_sheet_for_bill(
    workbook_path="ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm",
    processed_data=processed_data,
    bill_type=bill_type,
    output_pdf_dir="output"
)

if result['success']:
    print(f"Sheet created: {result['sheet_name']}")
    print(f"PDF exported: {result['pdf_path']}")
else:
    print(f"Error: {result['error']}")
```

### Using the Wrapper Function

```python
from add_macro_scrutiny_sheet import add_macro_scrutiny_sheet

# Process Excel file
processor = ExcelProcessor()
processed_data = processor.process_excel("input_file.xlsx")

# Add macro scrutiny sheet
result = add_macro_scrutiny_sheet(
    processed_data=processed_data,
    output_file_path="output/scrutiny_sheet.xlsm",
    bill_type="running"
)

if result['success']:
    print(f"✅ Success! Sheet: {result['sheet_name']}")
    print(f"   PDF: {result['pdf_file']}")
```

## Integration into Bill Processing Workflow

### Option 1: Integrate into Batch Processor

Add to `core/processors/batch_processor.py` or your main processing function:

```python
from add_macro_scrutiny_sheet import add_macro_scrutiny_sheet

def process_bill(input_file):
    # ... existing processing code ...
    
    # Process Excel
    processor = ExcelProcessor()
    processed_data = processor.process_excel(input_file)
    
    # Generate documents
    generator = DocumentGenerator(processed_data)
    html_documents = generator.generate_all_documents()
    
    # Add macro scrutiny sheet
    template_path = Path("ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm")
    if template_path.exists():
        # Determine bill type from filename or data
        bill_type = determine_bill_type(input_file, processed_data)
        
        macro_result = add_macro_scrutiny_sheet(
            processed_data=processed_data,
            output_file_path=str(template_path),  # Updates the template file
            template_path=str(template_path),
            bill_type=bill_type
        )
        
        if macro_result.get('success'):
            print(f"✅ Macro scrutiny sheet added: {macro_result['sheet_name']}")
```

### Option 2: Standalone Processing

Create a script to process all bills:

```python
from pathlib import Path
from core.processors.excel_processor import ExcelProcessor
from automated_scrutiny_sheet_generator import create_scrutiny_sheet_for_bill

def process_all_bills(input_dir="input", output_dir="output"):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    template_path = Path("ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm")
    
    processor = ExcelProcessor()
    
    for excel_file in input_path.glob("*.xlsx"):
        print(f"Processing: {excel_file.name}")
        
        # Process Excel
        processed_data = processor.process_excel(str(excel_file))
        
        # Determine bill type
        bill_type = "running"  # Determine from filename or data
        if "final" in excel_file.name.lower():
            bill_type = "final"
        elif "first" in excel_file.name.lower():
            bill_type = "first"
        
        # Create scrutiny sheet
        result = create_scrutiny_sheet_for_bill(
            workbook_path=str(template_path),
            processed_data=processed_data,
            bill_type=bill_type,
            output_pdf_dir=str(output_path)
        )
        
        if result['success']:
            print(f"  ✅ Sheet: {result['sheet_name']}")
            print(f"  ✅ PDF: {Path(result['pdf_path']).name}")
        else:
            print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
```

## Sheet Name Format

The sheet name is generated as:
```
[First 5 words of contractor name]_[Agreement Number]
```

Example:
- Contractor: "M/s. Shree Krishna Builders Jaipur"
- Agreement: "48/2024-25"
- Sheet Name: "M s Shree Krishna Builders_48/2024-25"

**Note**: Sheet names are sanitized to comply with Excel's 31-character limit and invalid character restrictions.

## PDF Export

The PDF is exported with the exact name format:
```
MACRO scrutiny SHEET IN PDF_[Sheet Name].pdf
```

Example:
```
MACRO scrutiny SHEET IN PDF_M s Shree Krishna Builders_48-2024-25.pdf
```

## Macro Execution

The system attempts multiple methods to execute the macro button in cell E37:

1. **Find shape/button** overlapping cell E37 and execute its OnAction macro
2. **Try common macro names** like "GenerateBillNotes", "GenerateNotes", etc.
3. **Simulate click** on the cell to trigger the button

If automatic execution fails, a warning is displayed and the macro must be run manually.

## Error Handling

The system handles various error scenarios:

- **Missing template file**: Returns error with file path
- **Missing data**: Attempts to calculate from available data
- **Macro execution failure**: Continues with PDF export (macro can be run manually)
- **PDF export failure**: Returns error but sheet is still created

## Troubleshooting

### Macro Not Executing
- Check that the macro button is actually in cell E37
- Verify the macro name matches common patterns
- Try running the macro manually to ensure it works
- Check Excel security settings allow macro execution

### Missing Data in Cells
- Verify the processed_data contains `title_data` with required fields
- Check that `totals` are calculated or can be derived from data
- Ensure field names match expected variations (see cell mapping table)

### PDF Not Generated
- Verify Excel is installed and accessible via COM
- Check that the sheet exists after macro execution
- Ensure output directory is writable

## Notes

- The template workbook is modified in-place (sheets are added to it)
- Each bill process adds a new sheet to the template workbook
- The template file should be backed up before processing multiple bills
- Consider copying the template file for each batch of bills to avoid conflicts


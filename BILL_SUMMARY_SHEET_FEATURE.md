# Bill Summary Sheet Addition Feature

## Overview
This feature adds a new sheet to each processed Excel bill file with a dynamically generated name based on the contractor's name and agreement number. The sheet contains a summary of key bill information for easy reference.

## Implementation Details

### Sheet Name Generation
The sheet name is generated using the format:
**[First 5 letters of contractor's first name] [Agreement number without year]**

For example:
- Contractor: "M/s. Shree Krishna Builders Jaipur"
- Agreement No.: "48/2024-25"
- Generated Sheet Name: "Shree 48"

### Logic
1. **Contractor Name Processing**:
   - Removes common prefixes like "M/s.", "Mr.", "Mrs.", etc.
   - Extracts the first word after the prefix
   - Takes the first 5 letters of that word

2. **Agreement Number Processing**:
   - For format "XX/YYYY-ZZ", extracts the "XX" part
   - For format "XXXX", keeps the entire number

### Data Included in Summary Sheet
The summary sheet contains two columns:
- **Field**: Description of the data
- **Value**: The actual data value

Fields included:
- Bill Number
- Contractor Name
- Agreement Number
- Work Description
- Work Order Amount
- Start Date
- Completion Date
- Actual Completion Date
- Calculated Total Amount (based on work order data)

## Code Implementation

### Files Modified
1. **core/processors/batch_processor.py**: 
   - Added helper functions for name and number processing
   - Added `add_bill_summary_sheet()` function
   - Integrated sheet addition into the batch processing workflow

### Key Functions
- `extract_contractor_first_name()`: Processes contractor names
- `extract_agreement_number_without_year()`: Extracts agreement numbers
- `generate_sheet_name()`: Creates the sheet name
- `create_bill_summary_data()`: Prepares summary data
- `add_bill_summary_sheet()`: Adds the new sheet to Excel files

## Usage
The feature is automatically applied during batch processing. For each processed bill:
1. A copy of the original Excel file is created
2. A new sheet with the summary data is added
3. The sheet name follows the specified naming convention
4. The enhanced file is saved in the output folder

## Example Output
For a bill with contractor "M/s. Shree Krishna Builders Jaipur" and agreement "48/2024-25":
- New sheet named "Shree 48" is added
- Sheet contains key bill information in a structured format
- Easy reference for reviewers and auditors

## Benefits
- Quick access to key bill information
- Standardized naming convention for easy identification
- Automated process requiring no manual intervention
- Preserves original file while adding valuable summary information
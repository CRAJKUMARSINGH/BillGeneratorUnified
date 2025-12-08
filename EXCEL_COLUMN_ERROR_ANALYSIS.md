# Excel Column Error Analysis

## Issue Description

Error: `Usecols do not match columns, columns expected but not found: ['Item No.'] (sheet: Work Order)`

This error occurs when attempting to read Excel files using `pd.read_excel()` with `usecols` parameter specifying column names that don't match what's actually in the file.

## Root Cause Analysis

### File Structure vs. Code Expectations

1. **Actual Excel Files**: Contain columns named:
   - `'Item'` (not `'Item No.'`)
   - `'Description'`
   - `'Unit'`
   - `'Quantity'`
   - `'Rate'`

2. **Code Expectations**: Some code attempts to read with:
   - `'Item No.'` (which doesn't exist in the files)
   - Other expected column names

### Where the Error Occurs

The error occurs when code directly calls:
```python
pd.read_excel(file, 'Work Order', usecols=['Item No.', 'Description', 'Unit', 'Quantity', 'Rate'])
```

But the file actually contains:
```python
['Item', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount', 'BSR']
```

## Solution Implementation

### Existing Solution: Flexible Column Mapping

The codebase already includes a robust solution in `core/processors/excel_processor.py`:

```python
# Define column mappings for different naming conventions
self.column_mappings = {
    'Work Order': {
        'Item No.': 'Item',  # Map expected to actual
        'Item': 'Item',
        'Description': 'Description',
        'Unit': 'Unit',
        'Quantity': 'Quantity',
        'Rate': 'Rate'
    },
    # Similar mappings for other sheets...
}
```

### How the Solution Works

1. **Column Detection**: First reads a sample of the file to detect actual column names
2. **Flexible Mapping**: Maps expected column names to actual column names
3. **Robust Reading**: Uses the actual column names when calling `pd.read_excel()`
4. **Standardization**: Renames columns to standard names in the output

### Recommended Approach

Instead of direct pandas calls, use the ExcelProcessor:

```python
from core.processors.excel_processor import ExcelProcessor

processor = ExcelProcessor()
processed_data = processor.process_excel(file_path)
work_order_df = processed_data['work_order_data']
# This will have standardized column names: ['Item No.', 'Description', 'Unit', 'Quantity', 'Rate']
```

## Best Practices

1. **Always use the ExcelProcessor** for reading Excel files in this project
2. **Never hardcode column names** in direct pandas calls
3. **Leverage the flexible mapping system** which handles various naming conventions
4. **Test with actual files** to ensure compatibility

## Verification

Tests confirm that the ExcelProcessor correctly handles:
- Files with `'Item'` column (current files)
- Would also handle files with `'Item No.'` column (if they existed)
- Provides consistent output with standardized column names
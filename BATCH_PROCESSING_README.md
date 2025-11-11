# Batch Processing with Date/Time/Filename Stamped Folders

## Overview
The batch processor now creates organized output folders with timestamps and filenames for easy tracking and management.

## Folder Structure

```
output/
├── 20241111_143025_ProjectA/
│   ├── html/
│   │   ├── First Page Summary.html
│   │   ├── Deviation Statement.html
│   │   ├── Final Bill Scrutiny Sheet.html
│   │   ├── Extra Items Statement.html
│   │   ├── Certificate II.html
│   │   └── Certificate III.html
│   └── pdf/
│       ├── First Page Summary.pdf
│       ├── Deviation Statement.pdf
│       ├── Final Bill Scrutiny Sheet.pdf
│       ├── Extra Items Statement.pdf
│       ├── Certificate II.pdf
│       └── Certificate III.pdf
├── 20241111_143026_ProjectB/
│   ├── html/
│   └── pdf/
└── 20241111_143027_ProjectC/
    ├── html/
    └── pdf/
```

## Folder Naming Convention

**Format:** `YYYYMMDD_HHMMSS_filename`

- **YYYYMMDD**: Date (Year, Month, Day)
- **HHMMSS**: Time (Hour, Minute, Second)
- **filename**: Original Excel filename (without extension)

**Example:** `20241111_143025_ProjectA`
- Date: November 11, 2024
- Time: 14:30:25 (2:30:25 PM)
- File: ProjectA.xlsx

## How to Use

### Method 1: Command Line (Batch Script)

1. Place your Excel files in the `input/` folder
2. Run `BATCH_RUN.bat`
3. Check the `output/` folder for results

### Method 2: Web Interface (Streamlit)

1. Run `LAUNCH.bat` and select option 5 (SmartBillFlow)
2. Select "📦 Batch Processing" mode in the sidebar
3. Upload multiple Excel files
4. Click "🚀 Process All Files"
5. View results with output folder paths

### Method 3: Python Script

```python
from core.processors.batch_processor import BatchProcessor
from core.config.config_loader import ConfigLoader

# Load config
config = ConfigLoader.load_from_env('BILL_CONFIG', 'config/smartbillflow.json')

# Create processor
processor = BatchProcessor(config)

# Process files
files = ['file1.xlsx', 'file2.xlsx']
results = processor.process_batch(files)

# Check results
for filename, result in results.items():
    if result['status'] == 'success':
        print(f"Output: {result['output_folder']}")
```

## Features

✅ **Timestamped Folders**: Each batch run creates unique folders
✅ **Organized Structure**: Separate HTML and PDF subfolders
✅ **Original Filename**: Easy to identify which Excel file was processed
✅ **No Overwrites**: Timestamps prevent accidental file overwrites
✅ **Batch Processing**: Process multiple files at once
✅ **Progress Tracking**: Real-time progress updates
✅ **Error Handling**: Detailed error messages for failed files

## Output Files

Each processed Excel file generates:

### HTML Files (in `html/` subfolder)
- First Page Summary.html
- Deviation Statement.html
- Final Bill Scrutiny Sheet.html
- Extra Items Statement.html (if applicable)
- Certificate II.html
- Certificate III.html

### PDF Files (in `pdf/` subfolder)
- First Page Summary.pdf
- Deviation Statement.pdf
- Final Bill Scrutiny Sheet.pdf
- Extra Items Statement.pdf (if applicable)
- Certificate II.pdf
- Certificate III.pdf

## Benefits

1. **Easy Tracking**: Timestamp shows exactly when files were processed
2. **No Confusion**: Each Excel file has its own dedicated folder
3. **Version Control**: Multiple runs of the same file create separate folders
4. **Organized**: HTML and PDF files are separated for easy access
5. **Audit Trail**: Folder names provide complete processing history

## Example Output

```
Processing: ProjectA.xlsx
   📁 Output folder: output\20241111_143025_ProjectA
   ✅ Success!
      - HTML files: 6
      - PDF files: 6

Processing: ProjectB.xlsx
   📁 Output folder: output\20241111_143026_ProjectB
   ✅ Success!
      - HTML files: 5
      - PDF files: 5
```

## Troubleshooting

**Issue**: No output folder created
- **Solution**: Check if the Excel file has all required sheets (Title, Work Order, Bill Quantity)

**Issue**: Missing PDF files
- **Solution**: Ensure PDF generation libraries are installed (weasyprint, xhtml2pdf, or playwright)

**Issue**: Folder permission errors
- **Solution**: Run with appropriate permissions or change output directory

## Configuration

The output base directory can be changed in `batch_processor.py`:

```python
self.output_base_dir = Path("output")  # Change to your preferred location
```

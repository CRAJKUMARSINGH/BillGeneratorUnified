# Macro Scrutiny Sheet Download Integration

## Overview
This document describes the integration of macro-enabled scrutiny sheets into the download center, allowing users to easily download and manage these specialized Excel files.

## Changes Made

### 1. Enhanced Batch Processor (`core/processors/batch_processor_enhanced.py`)
- Added support for generating macro-enabled scrutiny sheets during batch processing
- Integrated `simple_scrutiny_sheet_generator.py` to create `.xlsm` files
- Added `macro_sheet` field to `ProcessingResult` dataclass
- Implemented automatic saving of macro sheets to output folders
- Added PDF export functionality for scrutiny sheets

### 2. Enhanced Download Center (`core/ui/enhanced_download_center.py`)
- Added dedicated "Macro Sheets Only" quick action button
- Implemented `_create_macro_sheets_zip()` function for bulk downloading
- Added special section in file browser for macro sheets with dedicated ZIP download
- Updated `integrate_with_batch_processor()` to properly handle macro sheet files

## New Features

### Quick Actions in ZIP Creator
A new "📊 Macro Sheets Only" button has been added to the ZIP Creator section that allows users to:
- Quickly select all macro-enabled scrutiny sheets (.xlsm files)
- Create a ZIP archive containing only these specialized files

### Dedicated Macro Sheets Section
In the file browser, there's now:
- A special section highlighting macro-enabled scrutiny sheets
- A "Download All Macro Sheets as ZIP" button for bulk downloading

### Automatic Integration
During batch processing:
- Macro scrutiny sheets are automatically generated for each processed file
- Both .xlsm files and their PDF exports are added to the download manager
- Files are properly categorized in the "Excel Files" category

## Usage Instructions

### 1. Batch Processing with Macro Sheets
When using batch processing, macro scrutiny sheets are automatically generated:
1. Upload Excel files for processing
2. The system will automatically create macro-enabled scrutiny sheets (.xlsm)
3. PDF versions are also generated when possible
4. All files are added to the download center automatically

### 2. Downloading Individual Macro Sheets
From the Download Center:
1. Navigate to the File Browser tab
2. Scroll to the "Macro Scrutiny Sheets" section
3. Click the "Download All Macro Sheets as ZIP" button to download all at once
4. Or individually download specific sheets using their download buttons

### 3. Creating Custom ZIP with Macro Sheets
From the ZIP Creator tab:
1. Use the "📊 Macro Sheets Only" quick action button to select all macro sheets
2. Customize the ZIP name if desired
3. Click "Create and Download ZIP" to generate the archive

## File Organization

Macro sheets are organized as follows:
- **File Extension**: .xlsm (Excel Macro-Enabled Workbook)
- **Category**: Excel Files
- **Naming Convention**: `[original_filename]_scrutiny_sheet.xlsm`
- **PDF Exports**: `[original_filename]_scrutiny_sheet.pdf`

## Technical Details

### Dependencies
- `simple_scrutiny_sheet_generator.py` for creating macro sheets
- `openpyxl` for Excel file manipulation
- `win32com.client` for macro execution (when available)

### Template Requirements
The system expects the template file at:
```
ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm
```

### Error Handling
- Graceful degradation when COM components are unavailable
- Detailed error reporting for troubleshooting
- Automatic fallback to basic Excel operations when macros cannot be executed

## Troubleshooting

### Common Issues
1. **Template Not Found**: Ensure `ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm` exists
2. **COM Errors**: Install `pywin32` package for full macro support
3. **Permission Issues**: Ensure write access to output directories

### Verification
After processing, check that:
- .xlsm files appear in the download center
- Files are properly named with the original filename prefix
- PDF exports are generated when possible
# BillGeneratorUnified Test Suite

This directory contains comprehensive test scripts to validate the functionality of the BillGeneratorUnified application.

## 🧪 Test Runner Scripts

### `run_all_tests.py`
A comprehensive Python script that runs all tests in sequence:
- Enhanced PDF generation tests
- Chrome headless PDF generation tests
- Batch processing with Excel files
- Launcher script validation
- Dependency checks

### `RUN_ALL_TESTS.bat`
Windows batch file for easy execution of all tests.

## 🚀 Quick Start

### Windows
Double-click `RUN_ALL_TESTS.bat` or run from command prompt:
```cmd
RUN_ALL_TESTS.bat
```

### Cross-platform
```bash
python run_all_tests.py
```

## 📋 What the Tests Do

1. **Environment Setup**
   - Copies test Excel files from `TEST_INPUT_FILES/` to `input/` directory
   - Creates necessary output directories

2. **Dependency Check**
   - Verifies required Python packages are installed

3. **Enhanced PDF Tests**
   - Tests basic HTML to PDF conversion
   - Tests different zoom levels
   - Tests optimal zoom calculation
   - Tests batch conversion
   - Tests CSS zoom injection

4. **Chrome Headless Tests**
   - Validates Chrome/Chromium installation
   - Tests direct Chrome headless PDF generation
   - Tests enhanced generator with Chrome headless

5. **Batch Processing Test**
   - Processes all Excel files in the `input/` directory
   - Generates HTML and PDF outputs
   - Creates timestamped output folders

6. **Launcher Tests**
   - Runs all launcher scripts in the `launchers/` directory
   - Validates different configuration modes

## 📁 Output Directories

- `OUTPUT_FILES/` - Main output directory for generated bills
- `test_output/` - Test-specific output files
- `input/` - Input Excel files (created during test setup)
- Timestamped folders - Created by batch processing tests

## ✅ Expected Results

When all tests pass, you should see:
- ✅ PASS messages for all tests
- Generated PDF files in output directories
- No error messages

## ❌ Troubleshooting

Common issues and solutions:

1. **Missing Dependencies**
   ```
   pip install -r requirements.txt
   ```

2. **Chrome/Chromium Not Found**
   - Install Chrome from https://www.google.com/chrome/
   - Or install Chromium via package manager

3. **Permission Errors**
   - Ensure you have write permissions to the directory
   - Run as administrator if needed (Windows)

4. **Timeout Errors**
   - Increase the timeout value in the test script
   - Check system resources

## 🛠 Customization

You can modify the test behavior by editing `run_all_tests.py`:
- Adjust timeout values
- Add or remove specific tests
- Modify output directories
- Change test file locations

## 📊 Test Results

The test runner provides a detailed summary at the end:
- Number of tests passed/failed
- Specific error messages for failed tests
- Instructions for checking output files
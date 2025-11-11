# BillGenerator Unified

**Professional Bill Generation System with Batch Processing, Enhanced PDF Generation, and Timestamped Outputs**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)](https://github.com/CRAJKUMARSINGH/BillGeneratorUnified)

## 🎯 Features

### Core Features
- ✅ **Excel Upload Mode** - Process Excel files with bill data
- ✅ **Online Entry Mode** - Manual bill entry through web interface
- ✅ **Batch Processing** - Process multiple Excel files at once
- ✅ **Enhanced PDF Generation** - Pixel-perfect PDFs with no table shrinking
- ✅ **Timestamped Outputs** - Organized output folders with date/time/filename stamps
- ✅ **Multiple Variants** - 5 different configurations (V01-V04, SmartBillFlow)

### Enhanced PDF Generation
- 🎨 **CSS Zoom Property** - Precise content scaling
- 🔒 **Disable Smart Shrinking** - Prevents automatic content adjustment
- 📐 **Pixel-Perfect Calculations** - Exact measurements (A4 = 794x1123px at 96 DPI)
- 🚀 **Auto Engine Selection** - wkhtmltopdf → Playwright → WeasyPrint
- ✅ **No Table Shrinking** - Tables maintain 100% width permanently

### Batch Processing
- 📦 **Multiple File Processing** - Process all Excel files at once
- 📁 **Timestamped Folders** - Format: `YYYYMMDD_HHMMSS_filename`
- 📊 **Progress Tracking** - Real-time progress updates
- 🔄 **Error Handling** - Continues processing even if one file fails
- 📂 **Organized Structure** - Separate HTML and PDF subfolders

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/CRAJKUMARSINGH/BillGeneratorUnified.git
cd BillGeneratorUnified

# Install dependencies
pip install -r requirements.txt

# Optional: Install PDF engines for best quality
# wkhtmltopdf (recommended)
# Download from: https://wkhtmltopdf.org/downloads.html

# Playwright (alternative)
pip install playwright
playwright install chromium

# WeasyPrint (alternative)
pip install weasyprint
```

## 🚀 Quick Start

### Method 1: Batch Processing (Recommended)

1. **Place Excel files in input folder:**
   ```
   input/
   ├── ProjectA.xlsx
   ├── ProjectB.xlsx
   └── ProjectC.xlsx
   ```

2. **Run batch processing:**
   ```bash
   # Windows
   BATCH_RUN.bat
   
   # Or use main launcher
   LAUNCH.bat
   # Then select option 6
   ```

3. **Check outputs:**
   ```
   output/
   ├── 20241111_143025_ProjectA/
   │   ├── html/  ← 6 HTML files
   │   └── pdf/   ← 6 PDF files
   ├── 20241111_143026_ProjectB/
   │   ├── html/
   │   └── pdf/
   └── 20241111_143027_ProjectC/
       ├── html/
       └── pdf/
   ```

### Method 2: Web Interface

```bash
# Run main launcher
LAUNCH.bat

# Select option 5 (SmartBillFlow)
# Access web interface at http://localhost:8501
```

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
```

## 📁 Project Structure

```
BillGeneratorUnified/
├── core/
│   ├── config/              # Configuration files
│   ├── generators/          # Document and PDF generators
│   │   ├── document_generator.py
│   │   └── pdf_generator_enhanced.py
│   ├── processors/          # Excel and batch processors
│   │   ├── excel_processor.py
│   │   └── batch_processor.py
│   ├── templates/           # Jinja2 templates
│   └── ui/                  # Streamlit UI components
├── config/                  # Configuration JSON files
│   ├── v01.json
│   ├── v02.json
│   ├── v03.json
│   ├── v04.json
│   └── smartbillflow.json
├── launchers/               # Application launchers
├── input/                   # Input Excel files
├── output/                  # Generated outputs (timestamped)
├── app.py                   # Main Streamlit application
├── batch_run_demo.py        # Batch processing script
├── LAUNCH.bat               # Main launcher
└── BATCH_RUN.bat            # Batch processing launcher
```

## 📊 Generated Documents

Each Excel file generates **6 documents** in both HTML and PDF formats:

1. **First Page Summary** - Project overview and summary
2. **Deviation Statement** - Quantity deviations and changes
3. **Final Bill Scrutiny Sheet** - Detailed bill calculations
4. **Extra Items Statement** - Additional items (if applicable)
5. **Certificate II** - Completion certificate
6. **Certificate III** - Quality assurance certificate

## 🔧 Configuration

### Available Variants

| Variant | Features | Use Case |
|---------|----------|----------|
| **V01** | Standard features | Basic bill generation |
| **V02** | Light version | Quick processing |
| **V03** | Basic features | Simple bills |
| **V04** | Advanced + Batch | Multiple files |
| **SmartBillFlow** | All features | Production use |

### Excel File Format

Required sheets:
- **Title** - Project information (key-value pairs)
- **Work Order** - Work items with quantities and rates
- **Bill Quantity** - Bill quantity details

Optional sheets:
- **Extra Items** - Additional items
- **Deviation** - Quantity deviations

## 🎨 Enhanced PDF Generation

### No Table Shrinking (Permanent Fix)

The system includes a **permanent fix** to prevent table shrinking in PDFs:

```python
# Automatic in batch processing
processor = BatchProcessor(config)
results = processor.process_batch(files)
# Tables will NOT shrink ✅

# Manual usage
from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator

generator = EnhancedPDFGenerator()
pdf = generator.auto_convert(
    html_content,
    zoom=1.0,
    disable_smart_shrinking=True  # CRITICAL
)
```

### Protection Layers

1. **CSS Rules**: `table-layout: fixed !important`
2. **Engine Settings**: `--disable-smart-shrinking` (wkhtmltopdf)
3. **Viewport Control**: Fixed dimensions (794x1123px)
4. **Cell Protection**: Text wraps instead of shrinking

## 📚 Documentation

- **[BATCH_PROCESSING_README.md](BATCH_PROCESSING_README.md)** - Batch processing guide
- **[ENHANCED_PDF_GUIDE.md](ENHANCED_PDF_GUIDE.md)** - Enhanced PDF generation
- **[NO_SHRINK_FIX.md](NO_SHRINK_FIX.md)** - Table shrinking fix details
- **[WHERE_ARE_OUTPUTS.md](WHERE_ARE_OUTPUTS.md)** - Output location guide
- **[QUICK_START_BATCH.md](QUICK_START_BATCH.md)** - Quick start guide

## 🆘 Troubleshooting

### No output folder created
**Solution:** Run batch processing first - folder is created automatically

### Tables shrinking in PDF
**Solution:** The fix is automatic. Ensure `disable_smart_shrinking=True`

### Missing PDF files
**Solution:** Install PDF engine (wkhtmltopdf, playwright, or weasyprint)

### Excel file not processing
**Solution:** Ensure Excel has required sheets (Title, Work Order, Bill Quantity)

## 🧪 Testing

```bash
# Test enhanced PDF generation
python test_enhanced_pdf.py

# Check test outputs
explorer test_output
```

## 📝 Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
jinja2>=3.1.2
weasyprint>=60.0
xhtml2pdf>=0.2.11
playwright>=1.40.0
reportlab>=4.0.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Rajkumar Singh Chauhan**

- GitHub: [@CRAJKUMARSINGH](https://github.com/CRAJKUMARSINGH)

## 🙏 Acknowledgments

- Built with Streamlit for the web interface
- Uses Jinja2 for template rendering
- Multiple PDF engines for flexibility
- Enhanced with pixel-perfect PDF generation

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in the `docs/` folder
- Review troubleshooting guides

---

**Made with ❤️ by Rajkumar Singh Chauhan**

**Status:** ✅ Production Ready | **Version:** 2.0.0 | **Last Updated:** November 2024

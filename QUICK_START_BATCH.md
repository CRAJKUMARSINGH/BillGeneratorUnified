# Quick Start - Batch Processing

## 🚀 Get Started in 3 Steps

### Step 1: Prepare Your Files
Place your Excel files in the `input/` folder:
```
input/
├── ProjectA.xlsx
├── ProjectB.xlsx
└── ProjectC.xlsx
```

### Step 2: Run Batch Processing

**Option A: Using LAUNCH.bat**
1. Double-click `LAUNCH.bat`
2. Select option `6` (Batch Run)
3. Wait for processing to complete

**Option B: Direct Batch Run**
1. Double-click `BATCH_RUN.bat`
2. Wait for processing to complete

**Option C: Web Interface**
1. Run `LAUNCH.bat` → Select option `5` (SmartBillFlow)
2. In sidebar, select "📦 Batch Processing"
3. Upload files and click "🚀 Process All Files"

### Step 3: Get Your Results
Find your outputs in timestamped folders:
```
output/
├── 20241111_143025_ProjectA/
│   ├── html/  ← HTML files here
│   └── pdf/   ← PDF files here
├── 20241111_143026_ProjectB/
│   ├── html/
│   └── pdf/
└── 20241111_143027_ProjectC/
    ├── html/
    └── pdf/
```

## 📁 What You Get

Each Excel file generates **6 documents** in both HTML and PDF:

1. **First Page Summary** - Overview and project info
2. **Deviation Statement** - Quantity deviations
3. **Final Bill Scrutiny Sheet** - Detailed calculations
4. **Extra Items Statement** - Additional items (if any)
5. **Certificate II** - Completion certificate
6. **Certificate III** - Quality certificate

## 🎯 Folder Naming

**Format:** `YYYYMMDD_HHMMSS_filename`

**Example:** `20241111_143025_ProjectA`
- **20241111** = November 11, 2024
- **143025** = 2:30:25 PM
- **ProjectA** = Original filename

## ✅ Benefits

- ✨ **No Overwrites** - Each run creates unique folders
- 📅 **Easy Tracking** - Know when files were processed
- 📂 **Organized** - HTML and PDF separated
- 🔍 **Searchable** - Find by date, time, or filename
- 📊 **Batch Ready** - Process multiple files at once

## 💡 Tips

1. **File Names**: Use descriptive names (e.g., `ProjectA_Final.xlsx`)
2. **Organization**: Folders are sorted by timestamp automatically
3. **Backup**: Old outputs are never deleted - manage manually
4. **Speed**: Processing time depends on file size and complexity

## 🆘 Troubleshooting

**No output created?**
- Check if Excel has required sheets: Title, Work Order, Bill Quantity

**Missing PDF files?**
- Install PDF libraries: `pip install weasyprint xhtml2pdf`

**Permission errors?**
- Run as administrator or check folder permissions

## 📞 Need Help?

Check these files:
- `BATCH_PROCESSING_README.md` - Detailed documentation
- `EXAMPLE_OUTPUT_STRUCTURE.txt` - Visual folder structure
- `batch_run_demo.py` - Source code

---

**Ready to process?** Place your Excel files in `input/` and run `BATCH_RUN.bat`! 🚀

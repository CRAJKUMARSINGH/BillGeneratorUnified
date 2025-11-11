# 📁 WHERE ARE THE OUTPUTS?

## 🎯 Output Location

All batch processing outputs are saved in **timestamped folders** in the `output/` directory:

```
BillGeneratorUnified/
├── input/                    ← PUT YOUR EXCEL FILES HERE
│   ├── ProjectA.xlsx
│   ├── ProjectB.xlsx
│   └── ProjectC.xlsx
│
└── output/                   ← OUTPUTS APPEAR HERE
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
    │
    ├── 20241111_143026_ProjectB/
    │   ├── html/
    │   └── pdf/
    │
    └── 20241111_143027_ProjectC/
        ├── html/
        └── pdf/
```

## 📂 Folder Structure Explained

### Input Folder: `input/`
**Purpose:** Place your Excel files here for batch processing

**Location:** `C:\Users\Rajkumar\BillGeneratorUnified\input\`

**What to do:**
1. Copy your Excel files to this folder
2. Run batch processing
3. Files will be processed automatically

### Output Folder: `output/`
**Purpose:** All generated HTML and PDF files are saved here

**Location:** `C:\Users\Rajkumar\BillGeneratorUnified\output\`

**Folder naming:** `YYYYMMDD_HHMMSS_filename`
- `YYYYMMDD` = Date (e.g., 20241111 = Nov 11, 2024)
- `HHMMSS` = Time (e.g., 143025 = 2:30:25 PM)
- `filename` = Original Excel filename without extension

**Example:**
```
20241111_143025_ProjectA
│
├── Date: November 11, 2024
├── Time: 2:30:25 PM
└── File: ProjectA.xlsx
```

## 🔍 How to Find Your Outputs

### Method 1: Windows Explorer
1. Open File Explorer
2. Navigate to: `C:\Users\Rajkumar\BillGeneratorUnified\output\`
3. Look for folders with today's date
4. Open the folder → Open `html/` or `pdf/` subfolder

### Method 2: Command Line
```cmd
cd C:\Users\Rajkumar\BillGeneratorUnified
dir output /s
```

### Method 3: Quick Open
```cmd
explorer output
```

## 📊 What Files Are Generated?

For each Excel file, you get **6 documents** in both HTML and PDF:

| Document | Description |
|----------|-------------|
| **First Page Summary** | Project overview and summary |
| **Deviation Statement** | Quantity deviations and changes |
| **Final Bill Scrutiny Sheet** | Detailed bill calculations |
| **Extra Items Statement** | Additional items (if any) |
| **Certificate II** | Completion certificate |
| **Certificate III** | Quality assurance certificate |

## 🚀 Quick Test to Generate Outputs

### Step 1: Create a Test Excel File
Place any Excel file in the `input/` folder (even a blank one for testing)

### Step 2: Run Batch Processing
```cmd
BATCH_RUN.bat
```

### Step 3: Check Output
```cmd
explorer output
```

You'll see a new timestamped folder with your outputs!

## 📍 Current Status

**Input Folder:** `C:\Users\Rajkumar\BillGeneratorUnified\input\`
- Status: ✅ Exists
- Files: None yet (waiting for your Excel files)

**Output Folder:** `C:\Users\Rajkumar\BillGeneratorUnified\output\`
- Status: Will be created automatically when you run batch processing
- Files: None yet (will appear after processing)

## 🎯 Step-by-Step: First Run

### 1. Prepare Input
```cmd
# Copy your Excel file to input folder
copy "C:\path\to\your\file.xlsx" input\
```

### 2. Run Processing
```cmd
# Option A: Direct batch run
BATCH_RUN.bat

# Option B: Main launcher
LAUNCH.bat
# Then select option 6
```

### 3. View Outputs
```cmd
# Open output folder
explorer output

# Or list outputs
dir output /s
```

### 4. Expected Result
```
output/
└── 20241111_HHMMSS_yourfile/
    ├── html/  ← 6 HTML files
    └── pdf/   ← 6 PDF files
```

## 📝 Output Folder Naming Examples

| Excel File | Output Folder Name |
|------------|-------------------|
| `ProjectA.xlsx` | `20241111_143025_ProjectA` |
| `Final_Bill_2024.xlsx` | `20241111_143026_Final_Bill_2024` |
| `Client_ABC.xlsx` | `20241111_143027_Client_ABC` |

## 🔄 Multiple Runs

Each time you run batch processing, **new folders are created**:

```
output/
├── 20241111_140000_ProjectA/  ← First run at 2:00 PM
├── 20241111_143000_ProjectA/  ← Second run at 2:30 PM
└── 20241111_150000_ProjectA/  ← Third run at 3:00 PM
```

**No files are overwritten!** Each run creates a unique timestamped folder.

## 🆘 Troubleshooting

### Issue: No output folder created
**Cause:** Batch processing hasn't been run yet
**Solution:** Run `BATCH_RUN.bat` or place Excel files in `input/` folder

### Issue: Output folder is empty
**Cause:** Processing failed or no Excel files in input folder
**Solution:** 
1. Check console output for errors
2. Ensure Excel files are in `input/` folder
3. Check Excel files have required sheets (Title, Work Order, Bill Quantity)

### Issue: Can't find specific output
**Cause:** Multiple output folders exist
**Solution:** 
1. Sort by date (newest first)
2. Look at folder name timestamp
3. Match timestamp with when you ran the process

## 📂 Alternative Output Locations

If you want outputs in a different location, you can:

### Option 1: Change Output Directory
Edit `core/processors/batch_processor.py`:
```python
self.output_base_dir = Path("output")  # Change to your preferred path
```

### Option 2: Copy Outputs After Processing
```cmd
# Copy all outputs to another location
xcopy output "D:\MyOutputs\" /E /I
```

### Option 3: Create Symbolic Link
```cmd
# Link output folder to another drive
mklink /D "D:\BillOutputs" "C:\Users\Rajkumar\BillGeneratorUnified\output"
```

## 🎉 Summary

**Input Location:** `input/` folder
**Output Location:** `output/` folder with timestamped subfolders
**Folder Format:** `YYYYMMDD_HHMMSS_filename`
**Files Per Excel:** 6 HTML + 6 PDF = 12 files total

**To check outputs:**
```cmd
explorer output
```

**To run batch processing:**
```cmd
BATCH_RUN.bat
```

---

**Ready to generate outputs?** Place your Excel files in `input/` and run `BATCH_RUN.bat`! 🚀

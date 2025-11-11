# Installation Guide - BillGenerator Unified

## 📋 Table of Contents
- [Quick Install](#quick-install)
- [System Requirements](#system-requirements)
- [Python Dependencies](#python-dependencies)
- [PDF Engines](#pdf-engines)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Install

### For Windows

```bash
# 1. Clone repository
git clone https://github.com/CRAJKUMARSINGH/BillGeneratorUnified.git
cd BillGeneratorUnified

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright (for PDF generation)
playwright install chromium

# 4. Run the application
LAUNCH.bat
```

### For Linux/macOS

```bash
# 1. Clone repository
git clone https://github.com/CRAJKUMARSINGH/BillGeneratorUnified.git
cd BillGeneratorUnified

# 2. Install system packages
sudo apt-get update
sudo apt-get install -y chromium-browser wkhtmltopdf

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright
playwright install chromium

# 5. Run the application
python -m streamlit run app.py
```

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB for application + 1 GB for dependencies

### Recommended Requirements
- **Python**: 3.10 or higher
- **RAM**: 8 GB or more
- **Disk Space**: 2 GB free space

## 📦 Python Dependencies

### Core Dependencies

```bash
pip install streamlit pandas openpyxl jinja2
```

### PDF Generation Engines (Install at least one)

#### Option 1: Chrome Headless (Recommended - Best Quality)
```bash
# Already installed if you have Chrome/Chromium
# Or install via Playwright:
pip install playwright
playwright install chromium
```

#### Option 2: wkhtmltopdf
**Windows:**
- Download from: https://wkhtmltopdf.org/downloads.html
- Install and add to PATH

**Linux:**
```bash
sudo apt-get install wkhtmltopdf
```

**macOS:**
```bash
brew install wkhtmltopdf
```

#### Option 3: WeasyPrint
```bash
pip install weasyprint
```

**Linux additional dependencies:**
```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

#### Option 4: xhtml2pdf
```bash
pip install xhtml2pdf
```

### All Dependencies at Once

```bash
pip install -r requirements.txt
```

## 🔧 PDF Engines

The system supports multiple PDF engines with automatic fallback:

### Priority Order:
1. **Chrome Headless** (Best quality, no table shrinking)
2. **wkhtmltopdf** (Good quality, widely supported)
3. **Playwright** (Good quality, cross-platform)
4. **WeasyPrint** (Fast, good for simple layouts)
5. **xhtml2pdf** (Fallback option)

### Installing Chrome Headless

**Windows:**
- Chrome is usually pre-installed
- Location: `C:\Program Files\Google\Chrome\Application\chrome.exe`

**Linux:**
```bash
# Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Or Chromium
sudo apt-get install chromium-browser
```

**macOS:**
```bash
brew install --cask google-chrome
```

### Verifying PDF Engine Installation

```python
# Test script
from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator

generator = EnhancedPDFGenerator()
html = "<html><body><h1>Test</h1></body></html>"

try:
    pdf = generator.auto_convert(html)
    print("✅ PDF generation working!")
except Exception as e:
    print(f"❌ Error: {e}")
```

## 🖥️ Platform-Specific Instructions

### Windows

1. **Install Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

2. **Install Git** (optional, for cloning)
   - Download from: https://git-scm.com/download/win

3. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```cmd
   LAUNCH.bat
   ```

### Linux (Ubuntu/Debian)

1. **Update System**
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

2. **Install Python and pip**
   ```bash
   sudo apt-get install python3 python3-pip
   ```

3. **Install System Packages**
   ```bash
   sudo apt-get install -y \
       chromium-browser \
       wkhtmltopdf \
       libpango-1.0-0 \
       libpangoft2-1.0-0 \
       fonts-liberation
   ```

4. **Install Python Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

### macOS

1. **Install Homebrew** (if not installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python@3.10
   ```

3. **Install PDF Engines**
   ```bash
   brew install --cask google-chrome
   brew install wkhtmltopdf
   ```

4. **Install Python Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

## ✅ Verification

### Test Installation

```bash
# Test Python
python --version

# Test pip
pip --version

# Test Streamlit
streamlit --version

# Test imports
python -c "import streamlit, pandas, openpyxl, jinja2; print('✅ All imports successful')"
```

### Test PDF Generation

```bash
# Run test script
python test_enhanced_pdf.py

# Check output
ls test_output/
```

### Test Batch Processing

```bash
# Place a test Excel file in input/
# Run batch processing
python batch_run_demo.py

# Check output
ls output/
```

## 🆘 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:**
```bash
pip install streamlit
```

### Issue: `No PDF engine available`
**Solution:** Install at least one PDF engine:
```bash
# Quick fix - install Playwright
pip install playwright
playwright install chromium
```

### Issue: `wkhtmltopdf: command not found`
**Solution:**
- **Windows**: Download and install from wkhtmltopdf.org
- **Linux**: `sudo apt-get install wkhtmltopdf`
- **macOS**: `brew install wkhtmltopdf`

### Issue: WeasyPrint fails on Windows
**Solution:** WeasyPrint has complex dependencies on Windows. Use Chrome Headless or wkhtmltopdf instead.

### Issue: Permission denied errors
**Solution:**
```bash
# Linux/macOS
chmod +x *.bat
chmod +x *.py

# Or run with sudo
sudo pip install -r requirements.txt
```

### Issue: Port already in use (Streamlit)
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Chrome not found
**Solution:**
```bash
# Check Chrome installation
google-chrome --version  # Linux
chrome --version         # macOS
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version  # Windows
```

## 🔄 Updating

### Update Python Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update from Git
```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## 🐳 Docker Installation (Optional)

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    wkhtmltopdf \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t billgenerator .
docker run -p 8501:8501 billgenerator
```

## 📚 Additional Resources

- **Python**: https://www.python.org/
- **Streamlit**: https://streamlit.io/
- **wkhtmltopdf**: https://wkhtmltopdf.org/
- **Playwright**: https://playwright.dev/python/
- **WeasyPrint**: https://weasyprint.org/

## 🎉 Success!

If all tests pass, you're ready to use BillGenerator Unified!

```bash
# Start the application
LAUNCH.bat  # Windows
# or
streamlit run app.py  # Linux/macOS
```

Access the web interface at: http://localhost:8501

---

**Need help?** Open an issue on GitHub: https://github.com/CRAJKUMARSINGH/BillGeneratorUnified/issues

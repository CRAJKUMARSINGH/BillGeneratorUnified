# Enhanced PDF Generation Guide
## CSS Zoom + Disable Smart Shrinking + Pixel-Perfect Calculations

## 🎯 Overview

The enhanced PDF generator provides **pixel-perfect** PDF output using three key techniques:

1. **CSS Zoom Property** - Precise content scaling
2. **Disable Smart Shrinking** - Prevents automatic content adjustment
3. **Exact Pixel Calculations** - Accurate measurements and positioning

## 🔧 Key Features

### 1. CSS Zoom Property

The generator adds CSS zoom to HTML before PDF conversion:

```css
body {
    zoom: 1.0;  /* 100% = no scaling, 0.9 = 90%, etc. */
    -moz-transform: scale(1.0);
    -moz-transform-origin: 0 0;
}
```

**Benefits:**
- Precise content scaling
- Maintains aspect ratios
- Works across all PDF engines

### 2. Disable Smart Shrinking

For **wkhtmltopdf**, the critical flag is added:

```bash
wkhtmltopdf --disable-smart-shrinking input.html output.pdf
```

**Why This Matters:**
- ❌ **Without flag**: Content automatically shrinks to fit page
- ✅ **With flag**: Content renders at exact specified size
- 🎯 **Result**: Pixel-perfect output matching HTML

### 3. Pixel-Perfect Calculations

```python
# A4 dimensions at 96 DPI
page_width_px = (210mm / 25.4) * 96 = 794 pixels
page_height_px = (297mm / 25.4) * 96 = 1123 pixels

# Calculate optimal zoom
zoom = page_width_px / content_width_px
```

## 📦 Installation

### Option 1: Chrome/Chromium Headless (Recommended - Best Quality)

**Windows:**
```bash
# Chrome is usually already installed
# If not, download from: https://www.google.com/chrome/
```

**Linux:**
```bash
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Or install Chromium
sudo apt-get install chromium-browser
```

**macOS:**
```bash
# Chrome is usually already installed
# Or install via Homebrew
brew install --cask google-chrome
```

**Command:**
```bash
google-chrome --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf=output.pdf input.html
```

### Option 2: wkhtmltopdf

**Windows:**
```bash
# Download from: https://wkhtmltopdf.org/downloads.html
# Install and add to PATH
```

**Linux:**
```bash
sudo apt-get install wkhtmltopdf
```

**macOS:**
```bash
brew install wkhtmltopdf
```

### Option 3: Playwright

```bash
pip install playwright
playwright install chromium
```

### Option 4: WeasyPrint

```bash
pip install weasyprint
```

## 🚀 Usage

### Basic Usage

```python
from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator

# Create generator
generator = EnhancedPDFGenerator()

# Convert HTML to PDF
html_content = "<html><body><h1>Test</h1></body></html>"
pdf_bytes = generator.auto_convert(
    html_content,
    zoom=1.0,
    disable_smart_shrinking=True
)

# Save PDF
with open('output.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

### Batch Processing

```python
# Convert multiple documents
html_documents = {
    'Document 1': html_content_1,
    'Document 2': html_content_2,
    'Document 3': html_content_3
}

pdf_documents = generator.batch_convert(
    html_documents,
    zoom=1.0,
    disable_smart_shrinking=True
)

# Save all PDFs
for name, pdf_bytes in pdf_documents.items():
    with open(f'{name}.pdf', 'wb') as f:
        f.write(pdf_bytes)
```

### Calculate Optimal Zoom

```python
# If your content is 1000px wide
content_width = 1000
optimal_zoom = generator.calculate_optimal_zoom(content_width)

print(f"Optimal zoom: {optimal_zoom}")  # e.g., 0.79

# Use calculated zoom
pdf_bytes = generator.auto_convert(html_content, zoom=optimal_zoom)
```

## 🎨 CSS Enhancements

The generator automatically adds these CSS rules:

```css
/* Pixel-Perfect CSS Zoom */
body {
    zoom: 1.0;
    -moz-transform: scale(1.0);
    -moz-transform-origin: 0 0;
}

/* Disable text rendering optimizations */
* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: geometricPrecision;
}

/* Exact pixel calculations */
table {
    border-collapse: collapse;
    table-layout: fixed;
}

/* Prevent content overflow */
* {
    box-sizing: border-box;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
```

## 🔍 Engine Priority

The generator tries engines in this order:

1. **Chrome/Chromium Headless** (Best quality with `--disable-smart-shrinking`)
   - Command: `google-chrome --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf`
   - Usually already installed on most systems
   - Pixel-perfect rendering
   
2. **wkhtmltopdf** (Excellent quality with `--disable-smart-shrinking`)
   - Dedicated PDF conversion tool
   - Fast and reliable
   
3. **Playwright** (Good quality, slower)
   - Browser automation
   - Consistent rendering
   
4. **WeasyPrint** (Fast, good for simple layouts)
   - Pure Python solution
   - Good for basic documents

## ⚙️ Configuration Options

### Zoom Levels

```python
# 100% - Original size
pdf = generator.auto_convert(html, zoom=1.0)

# 90% - Slightly smaller
pdf = generator.auto_convert(html, zoom=0.9)

# 110% - Slightly larger
pdf = generator.auto_convert(html, zoom=1.1)
```

### Smart Shrinking

```python
# Disable smart shrinking (recommended for pixel-perfect)
pdf = generator.auto_convert(html, disable_smart_shrinking=True)

# Enable smart shrinking (auto-fit content)
pdf = generator.auto_convert(html, disable_smart_shrinking=False)
```

### DPI Settings

```python
generator = EnhancedPDFGenerator()
generator.dpi = 96   # Standard screen DPI
generator.dpi = 150  # Higher quality
generator.dpi = 300  # Print quality
```

## 📊 Comparison

| Feature | Standard | Enhanced |
|---------|----------|----------|
| CSS Zoom | ❌ | ✅ |
| Disable Smart Shrinking | ❌ | ✅ |
| Pixel-Perfect | ❌ | ✅ |
| Auto Engine Selection | ❌ | ✅ |
| Batch Processing | ❌ | ✅ |
| Optimal Zoom Calculation | ❌ | ✅ |

## 🐛 Troubleshooting

### Issue: Content is shrunk in PDF

**Solution:** Ensure `disable_smart_shrinking=True`

```python
pdf = generator.auto_convert(html, disable_smart_shrinking=True)
```

### Issue: Content overflows page

**Solution:** Calculate and use optimal zoom

```python
zoom = generator.calculate_optimal_zoom(content_width_px)
pdf = generator.auto_convert(html, zoom=zoom)
```

### Issue: wkhtmltopdf not found

**Solution:** Install wkhtmltopdf and add to PATH

```bash
# Windows: Download installer from wkhtmltopdf.org
# Linux: sudo apt-get install wkhtmltopdf
# macOS: brew install wkhtmltopdf
```

### Issue: Fonts look blurry

**Solution:** Increase DPI

```python
generator.dpi = 150  # or 300 for print quality
```

## 📈 Performance Tips

1. **Use wkhtmltopdf** for best quality and speed
2. **Batch convert** multiple documents at once
3. **Cache HTML** if generating same content multiple times
4. **Optimize images** in HTML before conversion
5. **Use fixed table layouts** for consistent rendering

## 🎯 Best Practices

### DO ✅

- Use `disable_smart_shrinking=True` for pixel-perfect output
- Calculate optimal zoom for content that might overflow
- Use fixed widths for tables and containers
- Test with different PDF engines
- Add CSS zoom for precise scaling

### DON'T ❌

- Don't rely on auto-shrinking for consistent output
- Don't use percentage widths without testing
- Don't forget to set proper page margins
- Don't use complex CSS that might not render consistently
- Don't skip testing with actual content

## 📝 Example: Complete Workflow

```python
from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator

# 1. Create generator
generator = EnhancedPDFGenerator()

# 2. Prepare HTML
html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid black; padding: 8px; }
    </style>
</head>
<body>
    <h1>Invoice #12345</h1>
    <table>
        <tr><th>Item</th><th>Quantity</th><th>Price</th></tr>
        <tr><td>Product A</td><td>10</td><td>$100</td></tr>
        <tr><td>Product B</td><td>5</td><td>$50</td></tr>
    </table>
</body>
</html>
"""

# 3. Convert with optimal settings
pdf_bytes = generator.auto_convert(
    html,
    zoom=1.0,
    disable_smart_shrinking=True
)

# 4. Save PDF
with open('invoice.pdf', 'wb') as f:
    f.write(pdf_bytes)

print(f"✅ PDF generated: {len(pdf_bytes)} bytes")
```

## 🔗 Integration with Batch Processor

The enhanced PDF generator is automatically used in batch processing:

```python
from core.processors.batch_processor import BatchProcessor

processor = BatchProcessor(config)
results = processor.process_batch(files)

# PDFs are generated with:
# - CSS Zoom: ✅
# - Disable Smart Shrinking: ✅
# - Pixel-Perfect Calculations: ✅
```

## 📚 Additional Resources

- [wkhtmltopdf Documentation](https://wkhtmltopdf.org/usage/wkhtmltopdf.txt)
- [Playwright PDF Options](https://playwright.dev/python/docs/api/class-page#page-pdf)
- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)
- [CSS Zoom Property](https://developer.mozilla.org/en-US/docs/Web/CSS/zoom)

---

**Ready to generate pixel-perfect PDFs?** Use the enhanced generator for professional-quality output! 🚀

# Chrome Headless PDF Generation - Quick Reference

## 🎯 The Perfect Command

```bash
google-chrome --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf=output.pdf input.html
```

## 🔧 Flag Breakdown

| Flag | Purpose | Why It Matters |
|------|---------|----------------|
| `--headless` | Run without GUI | Background processing |
| `--disable-gpu` | Disable GPU acceleration | Consistent rendering |
| `--no-margins` | Remove default margins | Full page control |
| `--disable-smart-shrinking` | **CRITICAL** - Disable auto-shrinking | **Pixel-perfect output** |
| `--run-all-compositor-stages-before-draw` | Complete rendering | Ensures all content is drawn |
| `--print-to-pdf=output.pdf` | Output file path | Where to save PDF |

## ⚠️ The Critical Flag

### `--disable-smart-shrinking`

**Without this flag:**
- ❌ Content automatically shrinks to fit page
- ❌ Unpredictable scaling
- ❌ Inconsistent output

**With this flag:**
- ✅ Content renders at exact specified size
- ✅ Pixel-perfect output
- ✅ Matches HTML exactly

## 📐 Page Size Control

### Using CSS @page

```html
<style>
    @page {
        size: A4;
        margin: 0;
    }
</style>
```

### Common Page Sizes

```css
@page { size: A4; }        /* 210mm × 297mm */
@page { size: Letter; }    /* 8.5in × 11in */
@page { size: Legal; }     /* 8.5in × 14in */
@page { size: A3; }        /* 297mm × 420mm */
```

## 🎨 CSS Zoom for Scaling

```html
<style>
    body {
        zoom: 1.0;  /* 100% - no scaling */
    }
</style>
```

### Zoom Examples

```css
zoom: 0.8;  /* 80% - smaller */
zoom: 0.9;  /* 90% - slightly smaller */
zoom: 1.0;  /* 100% - original size */
zoom: 1.1;  /* 110% - slightly larger */
```

## 💻 Platform-Specific Commands

### Windows

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf=output.pdf input.html
```

### Linux

```bash
google-chrome --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf=output.pdf input.html
```

### macOS

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf=output.pdf input.html
```

## 🐍 Python Integration

### Using subprocess

```python
import subprocess

cmd = [
    'google-chrome',
    '--headless',
    '--disable-gpu',
    '--no-margins',
    '--disable-smart-shrinking',
    '--run-all-compositor-stages-before-draw',
    '--print-to-pdf=output.pdf',
    'input.html'
]

subprocess.run(cmd, check=True)
```

### Using Enhanced PDF Generator

```python
from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator

generator = EnhancedPDFGenerator()
pdf_bytes = generator.convert_with_chrome_headless(
    html_content,
    disable_smart_shrinking=True,
    zoom=1.0
)
```

## 📊 Pixel-Perfect Calculations

### A4 at 96 DPI

```python
# A4 dimensions
width_mm = 210
height_mm = 297

# Convert to pixels at 96 DPI
width_px = (210 / 25.4) * 96  # 794 pixels
height_px = (297 / 25.4) * 96  # 1123 pixels
```

### Calculate Optimal Zoom

```python
def calculate_zoom(content_width_px, page_width_mm=210, dpi=96):
    page_width_px = (page_width_mm / 25.4) * dpi
    return page_width_px / content_width_px

# Example: Content is 1000px wide
zoom = calculate_zoom(1000)  # Returns 0.79
```

## 🎯 Best Practices

### DO ✅

1. **Always use `--disable-smart-shrinking`** for pixel-perfect output
2. Use CSS `@page` to control page size and margins
3. Use CSS `zoom` property for precise scaling
4. Test with actual content before batch processing
5. Set explicit widths for tables and containers

### DON'T ❌

1. Don't rely on auto-shrinking for consistent output
2. Don't use percentage widths without testing
3. Don't forget to set `@page` margins
4. Don't use complex CSS that might not render consistently
5. Don't skip the `--run-all-compositor-stages-before-draw` flag

## 🔍 Troubleshooting

### Issue: Content is shrunk

**Solution:** Add `--disable-smart-shrinking` flag

```bash
google-chrome --headless --disable-smart-shrinking --print-to-pdf=output.pdf input.html
```

### Issue: Content overflows page

**Solution:** Use CSS zoom to scale down

```html
<style>
    body { zoom: 0.9; }
</style>
```

### Issue: Chrome not found

**Solution:** Use full path to Chrome executable

```bash
# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless ...

# Linux
/usr/bin/google-chrome --headless ...

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless ...
```

### Issue: Incomplete rendering

**Solution:** Add `--run-all-compositor-stages-before-draw`

```bash
google-chrome --headless --run-all-compositor-stages-before-draw --print-to-pdf=output.pdf input.html
```

## 📈 Performance Tips

1. **Batch Processing:** Generate multiple PDFs in parallel
2. **Reuse HTML:** Cache HTML content if generating same document multiple times
3. **Optimize Images:** Compress images before embedding in HTML
4. **Minimize CSS:** Remove unused CSS rules
5. **Use System Fonts:** Avoid loading external fonts if possible

## 🎨 Example: Complete HTML Template

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 0;
        }
        
        body {
            font-family: Arial, sans-serif;
            margin: 20mm;
            zoom: 1.0;
        }
        
        * {
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            text-rendering: geometricPrecision;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        
        th, td {
            border: 1px solid #000;
            padding: 8px;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <h1>Document Title</h1>
    <table>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
        </tr>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </table>
</body>
</html>
```

## 🚀 Quick Start

1. **Create HTML file:**
   ```bash
   echo "<html><body><h1>Test</h1></body></html>" > test.html
   ```

2. **Generate PDF:**
   ```bash
   google-chrome --headless --disable-gpu --no-margins --disable-smart-shrinking --run-all-compositor-stages-before-draw --print-to-pdf=test.pdf test.html
   ```

3. **Check output:**
   ```bash
   ls -lh test.pdf
   ```

## 📚 Additional Resources

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Headless Chrome Documentation](https://developers.google.com/web/updates/2017/04/headless-chrome)
- [CSS Paged Media](https://www.w3.org/TR/css-page-3/)

---

**Remember:** The `--disable-smart-shrinking` flag is the key to pixel-perfect PDF output! 🎯

# Format Alignment with BillGeneratorHistorical

## Reference Repository
- **GitHub:** https://github.com/CRAJKUMARSINGH/BillGeneratorHistorical
- **Deployment:** https://bill-priyanka-add-percentage.streamlit.app/

## Output Format Requirements

### Document Templates (Must Match Exactly)

1. **First Page Summary**
   - Project information header
   - Work items table with columns:
     - Unit
     - Quantity Since
     - Quantity Upto
     - S.No
     - Description
     - Rate
     - Amount Upto
     - Amount Since
     - Remarks
   - Total calculations
   - Tender premium percentage
   - Grand total

2. **Deviation Statement**
   - Deviation analysis
   - Excess/Saving calculations
   - Item-wise deviations

3. **Final Bill Scrutiny Sheet**
   - Detailed bill calculations
   - Deductions (SD, IT, GST, LC)
   - Net payable amount

4. **Extra Items Statement** (if applicable)
   - Additional items not in work order
   - Separate calculations

5. **Certificate II**
   - Completion certificate
   - Work completion details

6. **Certificate III**
   - Quality assurance certificate
   - Compliance details

### Layout Specifications

#### Table Format:
```css
table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

th, td {
    border: 1px solid #000;
    padding: 8px;
    text-align: left;
    vertical-align: top;
}

th {
    background-color: #f0f0f0;
    font-weight: bold;
}
```

#### Page Format:
- **Size:** A4 (210mm × 297mm)
- **Margins:** 10mm all sides
- **Font:** Arial, 10-12pt
- **Line Height:** 1.2-1.5

#### Number Format:
- **Currency:** ₹ (Indian Rupee)
- **Decimals:** 2 places (e.g., 1,234.56)
- **Thousands Separator:** Comma (Indian system)

### Color Scheme

#### Headers:
- Background: #f0f0f0 (light gray)
- Text: #000000 (black)
- Border: #000000 (black, 1px solid)

#### Totals Row:
- Background: #e0e0e0 (slightly darker gray)
- Font-weight: bold

#### Highlight Rows:
- Background: #fff3cd (light yellow) for important items
- Background: #d4edda (light green) for positive values
- Background: #f8d7da (light red) for negative values

### Typography

#### Headings:
- H1: 16pt, bold, center-aligned
- H2: 14pt, bold, left-aligned
- H3: 12pt, bold, left-aligned

#### Body Text:
- Font: Arial, 10-11pt
- Line height: 1.4
- Text align: Left (numbers: right)

### Table Column Widths (First Page)

| Column | Width | Alignment |
|--------|-------|-----------|
| Unit | 6% | Left |
| Qty Since | 8% | Right |
| Qty Upto | 8% | Right |
| S.No | 6% | Center |
| Description | 37% | Left |
| Rate | 8% | Right |
| Amt Upto | 11% | Right |
| Amt Since | 9% | Right |
| Remarks | 7% | Left |

### PDF Generation Settings

```python
# Playwright settings
pdf_settings = {
    'format': 'A4',
    'print_background': True,
    'margin': {
        'top': '10mm',
        'right': '10mm',
        'bottom': '10mm',
        'left': '10mm'
    },
    'prefer_css_page_size': True,
    'scale': 1.0,  # No scaling
    'display_header_footer': False
}
```

### Critical CSS for No Shrinking

```css
/* CRITICAL: Prevent table shrinking */
table {
    table-layout: fixed !important;
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    border-collapse: collapse !important;
}

th, td {
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    padding: 8px !important;
}

/* Page settings */
@page {
    size: A4;
    margin: 10mm;
}

body {
    margin: 0;
    padding: 10mm;
    font-family: Arial, sans-serif;
    font-size: 10pt;
}
```

### Document Structure

#### Header Section:
```html
<div class="header" style="text-align: center; margin-bottom: 20px;">
    <h1>Document Title</h1>
    <p>Date: DD/MM/YYYY</p>
</div>
```

#### Project Info Section:
```html
<table class="info-table">
    <tr>
        <td><strong>Project Name:</strong></td>
        <td>{{project_name}}</td>
    </tr>
    <tr>
        <td><strong>Contract No:</strong></td>
        <td>{{contract_no}}</td>
    </tr>
    <!-- More fields -->
</table>
```

#### Work Items Table:
```html
<table class="work-items">
    <thead>
        <tr>
            <th>Unit</th>
            <th>Qty Since</th>
            <!-- More columns -->
        </tr>
    </thead>
    <tbody>
        {% for item in work_items %}
        <tr>
            <td>{{item.unit}}</td>
            <td class="amount">{{item.quantity_since}}</td>
            <!-- More cells -->
        </tr>
        {% endfor %}
    </tbody>
    <tfoot>
        <tr class="total-row">
            <td colspan="6">Total</td>
            <td class="amount">{{total_amount}}</td>
            <td class="amount">{{total_amount}}</td>
            <td></td>
        </tr>
    </tfoot>
</table>
```

### Footer Section:
```html
<div class="footer" style="margin-top: 30px;">
    <p><strong>Prepared by:</strong> {{prepared_by}}</p>
    <p><strong>Date:</strong> {{date}}</p>
    <p><strong>Signature:</strong> _________________</p>
</div>
```

## Verification Checklist

- [ ] Table layout matches reference
- [ ] Column widths are correct
- [ ] Number formatting is consistent
- [ ] Colors match exactly
- [ ] Fonts and sizes are correct
- [ ] Page margins are 10mm
- [ ] Tables don't shrink in PDF
- [ ] All 6 documents generate correctly
- [ ] Extra items appear when present
- [ ] Calculations are accurate
- [ ] Headers and footers are consistent

## Testing

1. Generate all documents from test files
2. Compare with reference outputs
3. Verify PDF rendering
4. Check table alignment
5. Validate calculations
6. Test with and without extra items

## Notes

- The format MUST match the BillGeneratorHistorical deployment exactly
- Any deviations should be documented and approved
- PDF generation must not shrink tables
- All calculations must be accurate
- Layout must be professional and print-ready

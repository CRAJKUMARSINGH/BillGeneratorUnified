# Manual VBA Macro Update Instructions

## File Updated
✓ **ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_TEMP.xlsm**

## What Was Done
1. ✓ Added rows for 17.A, 17.B, and 17.C
2. ✓ Updated all Excel formulas to reference correct cells
3. ⚠ VBA macro needs manual update (Excel security restriction)

## How to Update the VBA Macro Manually

### Step 1: Enable VBA Project Access (One-time setup)
1. Open Excel
2. Go to **File → Options → Trust Center → Trust Center Settings**
3. Click **Macro Settings**
4. Check ✓ **"Trust access to the VBA project object model"**
5. Click OK

### Step 2: Update the Macro
1. Open **ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_TEMP.xlsm**
2. Press **Alt + F11** to open VBA Editor
3. Find the module containing `GenerateBillNotes` (usually Module1 or similar)
4. Select ALL the code (Ctrl+A) and DELETE it
5. Open **updated_macro.vba** in a text editor
6. Copy ALL the code
7. Paste it into the VBA Editor
8. Press **Ctrl + S** to save
9. Close VBA Editor
10. Save the file as **english Note FINAL BILL NOTE SHEET.xlsm** (replace original)

## Key Changes in the Updated Macro

### Cell Reference Updates:
- **C18** → Item 16: Amount of Work Order (unchanged)
- **C19** → Item 17.A: Sum of payment upto last bill (NEW)
- **C20** → Item 17.B: Amount of this bill (NEW)
- **C21** → Item 17.C: Actual expenditure = A + B (NEW, calculated)
- **C22** → Repair Work (was C20)
- **C23** → Extra Item (was C21)
- **C24** → Extra Item Amount (was C22)
- **C25** → Excess Quantity (was C23)
- **C26** → Delay Comment (was C24)

### Output Cell:
- Changed from **B42** to **B44** (moved down 2 rows)

## Formula Updates in Sheet

All formulas have been automatically updated:
- Item 18 (Balance): `=C18-C21` (Work Order - Actual Expenditure)
- Item 17.C: `=C19+C20` (Sum of last bill + this bill)
- Net Amount: `=C21` (references 17.C)
- All deduction formulas updated to reference correct rows

## Verification Checklist

After updating the macro, verify:
- [ ] Item 17.A shows "Sum of payment upto last bill Rs."
- [ ] Item 17.B shows "Amount of this bill Rs."
- [ ] Item 17.C shows "Actual expenditure upto this bill = (A + B) Rs."
- [ ] Item 17.C formula is `=C19+C20`
- [ ] Item 18 (Balance) formula is `=C18-C21`
- [ ] Run the macro (Alt+F8, select GenerateBillNotes, Run)
- [ ] Check that output appears in cell B44
- [ ] Verify the generated notes are correct

## Backup
Original file backed up to:
**ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET_backup_20251205_204026.xlsm**

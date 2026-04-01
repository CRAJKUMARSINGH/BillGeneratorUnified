# CRITICAL: TEST INPUT FILES LOCATION

## 🔴 MANDATORY READING FOR ALL SOFTWARE ENGINEERS

**Date Created:** March 1, 2026  
**Priority:** CRITICAL  
**Status:** PERMANENT REFERENCE

---

## 📁 TEST INPUT FILES LOCATION

### ✅ CORRECT LOCATION (USE THIS)

```
TEST_INPUT_FILES/
```

**All test Excel files are located in the `TEST_INPUT_FILES` folder at the root of the repository.**

### ❌ WRONG LOCATION (DO NOT USE)

```
ATTACHED_ASSETS/  ❌ WRONG - Do not use for testing
```

---

## 📋 AVAILABLE TEST FILES

Located in: `TEST_INPUT_FILES/`

### Excel Files for Testing

1. **FirstFINALvidExtra.xlsx** ⭐ RECOMMENDED
2. **FirstFINALnoExtra.xlsx**
3. **3rdFinalVidExtra.xlsx**
4. **3rdFinalNoExtra.xlsx**
5. **3rdRunningVidExtra.xlsx**
6. **3rdRunningNoExtra.xlsx**
7. **0511Wextra.xlsx**
8. **0511-N-extra.xlsx**

### PDF Files (Reference Only)

- **FIRST_PAGE..pdf**
- **kachru.pdf**

---

## 🚀 HOW TO USE IN TESTING

### For Manual Browser Testing

1. Start the app: `streamlit run app.py`
2. Select: **"💻 Online Entry"** mode
3. Enable: **"🆕 Use Excel-Like Grid (Phase 2)"**
4. Click: **"Upload Excel file"**
5. Navigate to: **`TEST_INPUT_FILES`** folder
6. Select: **`FirstFINALvidExtra.xlsx`** (recommended)
7. Click: **Open**

### For Automated Testing

```python
# Use this path in test scripts
test_file = Path("TEST_INPUT_FILES/FirstFINALvidExtra.xlsx")

# NOT this
# test_file = Path("ATTACHED_ASSETS/some_file.xlsx")  ❌ WRONG
```

---

## 📝 UPDATE ALL DOCUMENTATION

When creating or updating documentation, always reference:

```
TEST_INPUT_FILES/
```

**NOT:**
- `ATTACHED_ASSETS/`
- `test_files/`
- `input_files/`
- Any other location

---

## 🔍 WHY THIS MATTERS

### Consistency
- All engineers use the same test files
- Reproducible test results
- No confusion about file locations

### Organization
- Test files separated from assets
- Clear naming convention
- Easy to find and maintain

### Quality Assurance
- Standardized testing
- Reliable test data
- Consistent results across team

---

## 📚 RELATED DOCUMENTATION

### Files That Reference TEST_INPUT_FILES

1. **BROWSER_TEST_GUIDE.md** - Browser testing instructions
2. **README.md** - Should reference this location
3. **Test scripts** - All automated tests
4. **User manuals** - Testing sections

### Files to Update

If you create new documentation, make sure to:
- ✅ Reference `TEST_INPUT_FILES/` folder
- ✅ Use recommended test files
- ✅ Include this location in examples
- ❌ Do NOT reference `ATTACHED_ASSETS/` for testing

---

## 🎯 QUICK REFERENCE

### For New Engineers

**Q: Where are the test files?**  
**A:** `TEST_INPUT_FILES/` folder at repository root

**Q: Which file should I use for testing?**  
**A:** `FirstFINALvidExtra.xlsx` (recommended)

**Q: Can I use files from ATTACHED_ASSETS?**  
**A:** NO. Use `TEST_INPUT_FILES/` only

**Q: Where do I put new test files?**  
**A:** Add them to `TEST_INPUT_FILES/` folder

---

## 🔄 MAINTENANCE

### Adding New Test Files

1. Place file in `TEST_INPUT_FILES/` folder
2. Update this document with file name
3. Update `BROWSER_TEST_GUIDE.md`
4. Update relevant test scripts
5. Commit with clear message

### Removing Test Files

1. Remove from `TEST_INPUT_FILES/` folder
2. Update this document
3. Update all references in documentation
4. Update test scripts
5. Commit with clear message

---

## ⚡ EMERGENCY REFERENCE

If you're in a hurry and need to test RIGHT NOW:

```bash
# 1. Start app
streamlit run app.py

# 2. In browser:
#    - Select "💻 Online Entry"
#    - Enable "🆕 Use Excel-Like Grid (Phase 2)"
#    - Upload: TEST_INPUT_FILES/FirstFINALvidExtra.xlsx
```

---

## 📞 CONTACT

If you have questions about test files:
1. Read this document first
2. Check `BROWSER_TEST_GUIDE.md`
3. Check `README.md`
4. Ask team lead

---

## 🏆 BEST PRACTICES

### DO ✅

- Use `TEST_INPUT_FILES/` for all testing
- Use `FirstFINALvidExtra.xlsx` as default test file
- Document any new test files added
- Keep test files organized
- Use consistent naming

### DON'T ❌

- Use `ATTACHED_ASSETS/` for testing
- Create test files in random locations
- Use undocumented test files
- Mix test files with production files
- Forget to update documentation

---

## 📊 FILE STRUCTURE

```
BillGeneratorUnified/
├── TEST_INPUT_FILES/           ⭐ USE THIS FOR TESTING
│   ├── FirstFINALvidExtra.xlsx ⭐ RECOMMENDED
│   ├── FirstFINALnoExtra.xlsx
│   ├── 3rdFinalVidExtra.xlsx
│   ├── 3rdFinalNoExtra.xlsx
│   ├── 3rdRunningVidExtra.xlsx
│   ├── 3rdRunningNoExtra.xlsx
│   ├── 0511Wextra.xlsx
│   └── 0511-N-extra.xlsx
│
├── ATTACHED_ASSETS/            ❌ NOT FOR TESTING
│   └── (reference materials only)
│
├── app.py
├── README.md
└── ...
```

---

## 🎓 TRAINING CHECKLIST

For new team members:

- [ ] Read this document completely
- [ ] Locate `TEST_INPUT_FILES/` folder
- [ ] Verify test files are present
- [ ] Test with `FirstFINALvidExtra.xlsx`
- [ ] Read `BROWSER_TEST_GUIDE.md`
- [ ] Understand why we use this location
- [ ] Know where NOT to look for test files
- [ ] Can explain to others

---

## 🔐 VERSION CONTROL

### This Document

- **Created:** March 1, 2026
- **Last Updated:** March 1, 2026
- **Version:** 1.0
- **Status:** Active

### Test Files Location

- **Location:** `TEST_INPUT_FILES/`
- **Status:** Permanent
- **Change Policy:** Requires team approval

---

## 🚨 CRITICAL REMINDERS

### 1. ALWAYS USE TEST_INPUT_FILES/

```
✅ CORRECT: TEST_INPUT_FILES/FirstFINALvidExtra.xlsx
❌ WRONG:   ATTACHED_ASSETS/some_file.xlsx
```

### 2. RECOMMENDED TEST FILE

```
FirstFINALvidExtra.xlsx
```

### 3. UPDATE DOCUMENTATION

When you add/remove test files, update:
- This document
- BROWSER_TEST_GUIDE.md
- README.md
- Test scripts

---

## 📖 SUMMARY

**ONE SENTENCE SUMMARY:**

> All test Excel files are in `TEST_INPUT_FILES/` folder, use `FirstFINALvidExtra.xlsx` for testing.

**THREE KEY POINTS:**

1. 📁 Location: `TEST_INPUT_FILES/`
2. ⭐ Recommended: `FirstFINALvidExtra.xlsx`
3. ❌ Don't use: `ATTACHED_ASSETS/`

---

**THIS IS A PERMANENT REFERENCE DOCUMENT**

**DO NOT DELETE OR MOVE THIS FILE**

**ALL ENGINEERS MUST READ THIS BEFORE TESTING**

---

*Last Updated: March 1, 2026*  
*Maintained by: Development Team*  
*Status: Active and Mandatory*

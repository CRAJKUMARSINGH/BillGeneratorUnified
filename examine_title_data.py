import pandas as pd

# Read the Title sheet
df = pd.read_excel('TEST_INPUT_FILES/0511-N-extra.xlsx', 'Title', header=None)

print("Title sheet structure:")
print("=" * 50)
for i, row in df.head(15).iterrows():
    if len(row) > 1:
        print(f"{i:2d}: {row[0]} => {row[1]}")
    else:
        print(f"{i:2d}: {row[0]}")

# Get the title data as the processor would
title_data = {}
for index, row in df.iterrows():
    if len(row) >= 2:
        key = str(row[0]).strip() if pd.notna(row[0]) else None
        value = row[1] if pd.notna(row[1]) else None
        
        if key and key != 'nan':
            title_data[key] = value

print("\nTitle data keys and values:")
print("=" * 50)
for key, value in title_data.items():
    print(f"'{key}': '{value}'")

# Find contractor name and agreement number
contractor_key = "Name of Contractor or supplier :"
agreement_key = "Agreement No."

contractor_name = title_data.get(contractor_key, "")
agreement_number = title_data.get(agreement_key, "")

print(f"\nContractor Name: '{contractor_name}'")
print(f"Agreement Number: '{agreement_number}'")

# Extract first 5 letters of contractor name
if contractor_name:
    first_5_letters = contractor_name[:5]
    print(f"First 5 letters of contractor name: '{first_5_letters}'")

# Extract agreement number without year (assuming format like XX/XXXX-XX)
if agreement_number:
    # Split by '/' and take the part after '/', then split by '-' and take first part
    parts = str(agreement_number).split('/')
    if len(parts) > 1:
        agreement_without_year = parts[1].split('-')[0] if '-' in parts[1] else parts[1]
        print(f"Agreement number without year: '{agreement_without_year}'")
    else:
        agreement_without_year = agreement_number
        print(f"Agreement number without year: '{agreement_without_year}'")

# Create sheet name
if contractor_name and agreement_number:
    first_5_letters = contractor_name[:5]
    parts = str(agreement_number).split('/')
    agreement_without_year = parts[1].split('-')[0] if len(parts) > 1 and '-' in parts[1] else (parts[1] if len(parts) > 1 else agreement_number)
    sheet_name = f"{first_5_letters} {agreement_without_year}"
    print(f"\nProposed sheet name: '{sheet_name}'")
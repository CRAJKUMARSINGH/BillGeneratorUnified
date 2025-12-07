import pandas as pd
import re

def extract_contractor_first_name(contractor_name):
    """Extract the first name from contractor name, skipping prefixes like 'M/s.'"""
    if not contractor_name:
        return ""
    
    # Remove common prefixes
    prefixes = ['M/s.', 'M/S.', 'Mr.', 'Mrs.', 'Ms.']
    cleaned_name = contractor_name.strip()
    
    for prefix in prefixes:
        if cleaned_name.startswith(prefix):
            cleaned_name = cleaned_name[len(prefix):].strip()
            break
    
    # Extract first word/name
    words = cleaned_name.split()
    if words:
        # Return first 5 letters of the first word
        return words[0][:5]
    return ""

def extract_agreement_number_without_year(agreement_number):
    """Extract agreement number without year part"""
    if not agreement_number:
        return ""
    
    # Handle format like "48/2024-25" -> we want "48"
    parts = str(agreement_number).split('/')
    if len(parts) > 1:
        # Take the part before the slash
        return parts[0]
    else:
        # If no slash, just return the whole thing
        return str(agreement_number)

# Read the Title sheet
df = pd.read_excel('TEST_INPUT_FILES/0511-N-extra.xlsx', 'Title', header=None)

# Get the title data as the processor would
title_data = {}
for index, row in df.iterrows():
    if len(row) >= 2:
        key = str(row[0]).strip() if pd.notna(row[0]) else None
        value = row[1] if pd.notna(row[1]) else None
        
        if key and key != 'nan':
            title_data[key] = value

# Find contractor name and agreement number
contractor_key = "Name of Contractor or supplier :"
agreement_key = "Agreement No."

contractor_name = title_data.get(contractor_key, "")
agreement_number = title_data.get(agreement_key, "")

print(f"Contractor Name: '{contractor_name}'")
print(f"Agreement Number: '{agreement_number}'")

# Extract first 5 letters of contractor first name
first_5_letters = extract_contractor_first_name(contractor_name)
print(f"First 5 letters of contractor first name: '{first_5_letters}'")

# Extract agreement number without year
agreement_without_year = extract_agreement_number_without_year(agreement_number)
print(f"Agreement number without year: '{agreement_without_year}'")

# Create sheet name
if first_5_letters and agreement_without_year:
    sheet_name = f"{first_5_letters} {agreement_without_year}"
    print(f"\nProposed sheet name: '{sheet_name}'")
else:
    print("\nCould not create sheet name due to missing data")
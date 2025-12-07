"""
Demonstration of the Bill Summary Sheet Addition Feature
"""
import os
from core.processors.batch_processor import (
    extract_contractor_first_name, 
    extract_agreement_number_without_year,
    generate_sheet_name
)

def demonstrate_feature():
    """Demonstrate the sheet name generation feature"""
    print("=== BILL SUMMARY SHEET FEATURE DEMONSTRATION ===\n")
    
    # Test cases
    test_cases = [
        {
            "contractor": "M/s. Shree Krishna Builders Jaipur",
            "agreement": "48/2024-25",
            "expected": "Shree 48"
        },
        {
            "contractor": "M/S. ABC Construction Company",
            "agreement": "123/2023-24",
            "expected": "ABC 123"
        },
        {
            "contractor": "Mr. John Smith Enterprises",
            "agreement": "789",
            "expected": "John 789"
        }
    ]
    
    print("Sheet Name Generation Examples:")
    print("-" * 50)
    
    for i, case in enumerate(test_cases, 1):
        contractor = case["contractor"]
        agreement = case["agreement"]
        expected = case["expected"]
        
        # Simulate title data
        title_data = {
            "Name of Contractor or supplier :": contractor,
            "Agreement No.": agreement
        }
        
        # Generate sheet name
        sheet_name = generate_sheet_name(title_data)
        
        print(f"Example {i}:")
        print(f"  Contractor: {contractor}")
        print(f"  Agreement:  {agreement}")
        print(f"  Sheet Name: {sheet_name}")
        print(f"  Expected:   {expected}")
        print(f"  Match:      {'✓' if sheet_name == expected else '✗'}")
        print()

    print("Function Breakdown:")
    print("-" * 30)
    
    # Demonstrate individual functions
    contractor = "M/s. Shree Krishna Builders Jaipur"
    agreement = "48/2024-25"
    
    first_name_part = extract_contractor_first_name(contractor)
    agreement_part = extract_agreement_number_without_year(agreement)
    
    print(f"Contractor: '{contractor}'")
    print(f"  → First 5 letters: '{first_name_part}'")
    print()
    print(f"Agreement: '{agreement}'")
    print(f"  → Without year: '{agreement_part}'")
    print()
    print(f"Combined Sheet Name: '{first_name_part} {agreement_part}'")

if __name__ == "__main__":
    demonstrate_feature()
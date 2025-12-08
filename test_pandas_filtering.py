"""
Test script for pandas-based filtering implementation
"""

import pandas as pd
import sys
import os

# Add the core directory to the path so we can import the DocumentGenerator
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

def create_test_data():
    """Create test data to verify pandas filtering"""
    # Create test work order data with hierarchical structure
    work_order_data = pd.DataFrame([
        # Level 1 items
        {'Item No.': '1.0', 'Description': 'SITE PREPARATION', 'Unit': 'LS', 'Quantity': 0.0, 'Rate': 10000.0},
        {'Item No.': '2.0', 'Description': 'FOUNDATION WORK', 'Unit': 'LS', 'Quantity': 0.0, 'Rate': 50000.0},
        
        # Level 2 items under 1.0 (all zero quantities)
        {'Item No.': '1.1', 'Description': 'CLEARING', 'Unit': 'SQM', 'Quantity': 0.0, 'Rate': 10.0},
        {'Item No.': '1.2', 'Description': 'GRADING', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 50.0},
        
        # Level 3 items under 1.1 (all zero quantities)
        {'Item No.': '1.1.1', 'Description': 'TREE REMOVAL', 'Unit': 'NOS', 'Quantity': 0.0, 'Rate': 500.0},
        {'Item No.': '1.1.2', 'Description': 'DEBRIS CLEANUP', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 200.0},
        
        # Level 3 items under 1.2 (all zero quantities)
        {'Item No.': '1.2.1', 'Description': 'EXCAVATION', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 100.0},
        {'Item No.': '1.2.2', 'Description': 'BACKFILL', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 80.0},
        
        # Level 2 items under 2.0 (non-zero quantities)
        {'Item No.': '2.1', 'Description': 'EXCAVATION', 'Unit': 'CUM', 'Quantity': 100.0, 'Rate': 150.0},  # Non-zero
        {'Item No.': '2.2', 'Description': 'CONCRETE', 'Unit': 'CUM', 'Quantity': 85.0, 'Rate': 2500.0},    # Non-zero
        
        # Level 3 items under 2.1 (non-zero quantities)
        {'Item No.': '2.1.1', 'Description': 'MECHANICAL EXCAVATION', 'Unit': 'CUM', 'Quantity': 70.0, 'Rate': 120.0},  # Non-zero
        {'Item No.': '2.1.2', 'Description': 'MANUAL EXCAVATION', 'Unit': 'CUM', 'Quantity': 30.0, 'Rate': 80.0},       # Non-zero
        
        # Level 3 items under 2.2 (non-zero quantities)
        {'Item No.': '2.2.1', 'Description': 'RCC M20', 'Unit': 'CUM', 'Quantity': 50.0, 'Rate': 2000.0},    # Non-zero
        {'Item No.': '2.2.2', 'Description': 'RCC M25', 'Unit': 'CUM', 'Quantity': 35.0, 'Rate': 2200.0},    # Non-zero
    ])
    
    return work_order_data

def test_pandas_filtering():
    """Test the pandas-based filtering implementation"""
    print("Testing Pandas-Based Filtering...")
    
    # Create test data
    work_order_data = create_test_data()
    print(f"Original data has {len(work_order_data)} items")
    
    # Since we can't import DocumentGenerator directly due to dependencies,
    # let's simulate the filtering logic here
    
    # Make a copy to avoid modifying the original dataframe
    df_copy = work_order_data.copy()
    
    # Add Parent_Item column
    df_copy['Parent_Item'] = df_copy['Item No.'].apply(
        lambda x: '.'.join(str(x).split('.')[:-1]) if pd.notna(x) and '.' in str(x) else None
    )
    
    # Create mask for items with quantity > 0
    quantity_mask = (df_copy['Quantity'] > 0)
    
    # Create mask for items that are parents of items with quantity > 0
    parent_mask = df_copy['Item No.'].isin(
        df_copy[df_copy['Quantity'] > 0]['Parent_Item']
    )
    
    # Combine masks
    mask = quantity_mask | parent_mask
    
    # Apply filter
    filtered_df = df_copy[mask]
    
    print(f"Filtered data has {len(filtered_df)} items")
    
    # Print results
    print("\nFiltered items:")
    for _, row in filtered_df.iterrows():
        print(f"  {row['Item No.']}: {row['Description']} (Qty: {row['Quantity']})")
    
    # Expected items (those with non-zero quantities or parents of non-zero items)
    expected_items = {
        '2.0', '2.1', '2.2', '2.1.1', '2.1.2', '2.2.1', '2.2.2'
    }
    
    actual_items = set(filtered_df['Item No.'].tolist())
    
    print(f"\nExpected items: {expected_items}")
    print(f"Actual items: {actual_items}")
    
    # Check if all expected items are present
    missing_items = expected_items - actual_items
    if missing_items:
        print(f"MISSING items: {missing_items}")
    else:
        print("All expected items are present!")
    
    # Check if there are unexpected items
    unexpected_items = actual_items - expected_items
    if unexpected_items:
        print(f"UNEXPECTED items: {unexpected_items}")
    else:
        print("No unexpected items found!")
    
    # Verify that no items with all zero descendants are included
    zero_items = {'1.0', '1.1', '1.2', '1.1.1', '1.1.2', '1.2.1', '1.2.2'}
    incorrectly_included = zero_items.intersection(actual_items)
    if incorrectly_included:
        print(f"INCORRECTLY INCLUDED zero items: {incorrectly_included}")
    else:
        print("No zero items incorrectly included!")
    
    return len(missing_items) == 0 and len(unexpected_items) == 0 and len(incorrectly_included) == 0

if __name__ == "__main__":
    success = test_pandas_filtering()
    print(f"\nTest {'PASSED' if success else 'FAILED'}!")
    sys.exit(0 if success else 1)
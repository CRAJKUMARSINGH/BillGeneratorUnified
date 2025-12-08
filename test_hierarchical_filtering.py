"""
Test script for hierarchical filtering implementation
"""

import pandas as pd
from core.generators.document_generator import DocumentGenerator
from core.processors.hierarchical_filter import filter_zero_hierarchy, parse_hierarchical_items, HierarchicalItem

def create_test_data():
    """Create test data to verify hierarchical filtering"""
    # Create test work order data with hierarchical structure
    work_order_data = pd.DataFrame([
        # Level 1 items
        {'Item No.': '1.0', 'Description': 'SITE PREPARATION', 'Unit': 'LS', 'Quantity': 0.0, 'Rate': 10000.0},
        {'Item No.': '2.0', 'Description': 'FOUNDATION WORK', 'Unit': 'LS', 'Quantity': 0.0, 'Rate': 50000.0},
        
        # Level 2 items under 1.0
        {'Item No.': '1.1', 'Description': 'CLEARING', 'Unit': 'SQM', 'Quantity': 0.0, 'Rate': 10.0},
        {'Item No.': '1.2', 'Description': 'GRADING', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 50.0},
        
        # Level 3 items under 1.1
        {'Item No.': '1.1.1', 'Description': 'TREE REMOVAL', 'Unit': 'NOS', 'Quantity': 0.0, 'Rate': 500.0},
        {'Item No.': '1.1.2', 'Description': 'DEBRIS CLEANUP', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 200.0},
        
        # Level 3 items under 1.2
        {'Item No.': '1.2.1', 'Description': 'EXCAVATION', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 100.0},
        {'Item No.': '1.2.2', 'Description': 'BACKFILL', 'Unit': 'CUM', 'Quantity': 0.0, 'Rate': 80.0},
        
        # Level 2 items under 2.0
        {'Item No.': '2.1', 'Description': 'EXCAVATION', 'Unit': 'CUM', 'Quantity': 100.0, 'Rate': 150.0},  # Non-zero
        {'Item No.': '2.2', 'Description': 'CONCRETE', 'Unit': 'CUM', 'Quantity': 85.0, 'Rate': 2500.0},    # Non-zero
        
        # Level 3 items under 2.1
        {'Item No.': '2.1.1', 'Description': 'MECHANICAL EXCAVATION', 'Unit': 'CUM', 'Quantity': 70.0, 'Rate': 120.0},  # Non-zero
        {'Item No.': '2.1.2', 'Description': 'MANUAL EXCAVATION', 'Unit': 'CUM', 'Quantity': 30.0, 'Rate': 80.0},       # Non-zero
        
        # Level 3 items under 2.2
        {'Item No.': '2.2.1', 'Description': 'RCC M20', 'Unit': 'CUM', 'Quantity': 50.0, 'Rate': 2000.0},    # Non-zero
        {'Item No.': '2.2.2', 'Description': 'RCC M25', 'Unit': 'CUM', 'Quantity': 35.0, 'Rate': 2200.0},    # Non-zero
    ])
    
    return work_order_data

def test_hierarchical_filtering():
    """Test the hierarchical filtering implementation"""
    print("Testing Hierarchical Zero Quantity Filtering...")
    
    # Create test data
    work_order_data = create_test_data()
    print(f"Original data has {len(work_order_data)} items")
    
    # Create a mock data dictionary as expected by DocumentGenerator
    mock_data = {
        'title_data': {},
        'work_order_data': work_order_data,
        'bill_quantity_data': pd.DataFrame(),
        'extra_items_data': pd.DataFrame(),
    }
    
    # Create DocumentGenerator instance
    generator = DocumentGenerator(mock_data)
    
    # Check the filtering results
    template_data = generator.template_data
    
    # Print results
    print(f"Filtered work items: {len(template_data['work_items'])}")
    print("Filtered work items:")
    for item in template_data['work_items']:
        print(f"  {item['item_no']}: {item['description']} (Qty: {item['quantity_since']})")
    
    print("\nFiltered items for templates:")
    for item in template_data['items']:
        print(f"  {item['serial_no']}: {item['description']} (Qty: {item['quantity_since_last']})")
    
    # Verify that only items with non-zero quantities or non-zero descendants are kept
    expected_items = ['2.0', '2.1', '2.2', '2.1.1', '2.1.2', '2.2.1', '2.2.2']
    actual_items = [item['item_no'] for item in template_data['work_items']]
    
    print(f"\nExpected items: {expected_items}")
    print(f"Actual items: {actual_items}")
    
    # Check if all expected items are present
    missing_items = set(expected_items) - set(actual_items)
    if missing_items:
        print(f"MISSING items: {missing_items}")
    else:
        print("All expected items are present!")
    
    # Check if there are unexpected items
    unexpected_items = set(actual_items) - set(expected_items)
    if unexpected_items:
        print(f"UNEXPECTED items: {unexpected_items}")
    else:
        print("No unexpected items found!")

def test_parse_hierarchical_items():
    """Test the parse_hierarchical_items function"""
    print("\nTesting parse_hierarchical_items function...")
    
    # Create test data
    work_order_data = create_test_data()
    
    # Parse hierarchical items
    hierarchical_items = parse_hierarchical_items(work_order_data)
    
    print(f"Parsed {len(hierarchical_items)} root items")
    
    # Print the hierarchy
    for item in hierarchical_items:
        print(f"Root: {item.code} - {item.description} (Qty: {item.quantity})")
        for child in item.children:
            print(f"  Child: {child.code} - {child.description} (Qty: {child.quantity})")
            for grandchild in child.children:
                print(f"    Grandchild: {grandchild.code} - {grandchild.description} (Qty: {grandchild.quantity})")

def test_filter_zero_hierarchy_function():
    """Test the filter_zero_hierarchy function directly"""
    print("\nTesting filter_zero_hierarchy function directly...")
    
    # Create test hierarchical items manually
    item_1_0 = HierarchicalItem("1.0", "SITE PREPARATION", 0.0, "LS", 10000.0)
    item_1_1 = HierarchicalItem("1.1", "CLEARING", 0.0, "SQM", 10.0)
    item_1_1_1 = HierarchicalItem("1.1.1", "TREE REMOVAL", 0.0, "NOS", 500.0)
    item_1_1_2 = HierarchicalItem("1.1.2", "DEBRIS CLEANUP", 0.0, "CUM", 200.0)
    
    item_2_0 = HierarchicalItem("2.0", "FOUNDATION WORK", 0.0, "LS", 50000.0)
    item_2_1 = HierarchicalItem("2.1", "EXCAVATION", 100.0, "CUM", 150.0)  # Non-zero
    item_2_1_1 = HierarchicalItem("2.1.1", "MECHANICAL EXCAVATION", 70.0, "CUM", 120.0)  # Non-zero
    item_2_1_2 = HierarchicalItem("2.1.2", "MANUAL EXCAVATION", 30.0, "CUM", 80.0)  # Non-zero
    
    # Build hierarchy
    item_1_1.children = [item_1_1_1, item_1_1_2]
    item_1_0.children = [item_1_1]
    
    item_2_1.children = [item_2_1_1, item_2_1_2]
    item_2_0.children = [item_2_1]
    
    root_items = [item_1_0, item_2_0]
    
    # Apply filtering
    filtered_items = filter_zero_hierarchy(root_items)
    
    print(f"Original root items: {len(root_items)}")
    print(f"Filtered root items: {len(filtered_items)}")
    
    for item in filtered_items:
        print(f"Filtered root: {item.code} - {item.description} (Qty: {item.quantity})")
        for child in item.children:
            print(f"  Child: {child.code} - {child.description} (Qty: {child.quantity})")
            for grandchild in child.children:
                print(f"    Grandchild: {grandchild.code} - {grandchild.description} (Qty: {grandchild.quantity})")

if __name__ == "__main__":
    test_parse_hierarchical_items()
    test_filter_zero_hierarchy_function()
    test_hierarchical_filtering()
    print("\nAll tests completed!")
"""
Simple verification of filtering logic without external dependencies
"""

def has_nonzero_in_hierarchy(item):
    """Check if item or any descendant has non-zero quantity"""
    # Check current item
    if item.get('quantity_since', 0) > 0 or item.get('quantity_upto', 0) > 0 or item.get('quantity', 0) > 0:
        return True
    
    # Check children recursively
    for child in item.get('children', []):
        if has_nonzero_in_hierarchy(child):
            return True
    
    return False

def filter_zero_hierarchy(items):
    """
    Recursively filter items where all descendants have zero quantities
    
    Rules:
    - If item has qty > 0, keep it
    - If any descendant has qty > 0, keep parent
    - If all descendants are zero, remove parent
    """
    filtered_items = []
    
    for item in items:
        # Check if item or any descendant has non-zero quantity
        if has_nonzero_in_hierarchy(item):
            # Recursively filter children
            if 'children' in item and item['children']:
                item['children'] = filter_zero_hierarchy(item['children'])
            filtered_items.append(item)
    
    return filtered_items

# Test data representing a hierarchical structure
test_data = [
    {
        'item_no': '1.0',
        'description': 'SITE PREPARATION',
        'quantity_since': 0,
        'quantity_upto': 0,
        'children': [
            {
                'item_no': '1.1',
                'description': 'CLEARING',
                'quantity_since': 0,
                'quantity_upto': 0,
                'children': [
                    {
                        'item_no': '1.1.1',
                        'description': 'TREE REMOVAL',
                        'quantity_since': 0,
                        'quantity_upto': 0,
                        'children': []
                    },
                    {
                        'item_no': '1.1.2',
                        'description': 'DEBRIS CLEANUP',
                        'quantity_since': 0,
                        'quantity_upto': 0,
                        'children': []
                    }
                ]
            },
            {
                'item_no': '1.2',
                'description': 'GRADING',
                'quantity_since': 0,
                'quantity_upto': 0,
                'children': [
                    {
                        'item_no': '1.2.1',
                        'description': 'EXCAVATION',
                        'quantity_since': 0,
                        'quantity_upto': 0,
                        'children': []
                    },
                    {
                        'item_no': '1.2.2',
                        'description': 'BACKFILL',
                        'quantity_since': 0,
                        'quantity_upto': 0,
                        'children': []
                    }
                ]
            }
        ]
    },
    {
        'item_no': '2.0',
        'description': 'FOUNDATION WORK',
        'quantity_since': 0,
        'quantity_upto': 0,
        'children': [
            {
                'item_no': '2.1',
                'description': 'EXCAVATION',
                'quantity_since': 100,
                'quantity_upto': 100,
                'children': [
                    {
                        'item_no': '2.1.1',
                        'description': 'MECHANICAL EXCAVATION',
                        'quantity_since': 70,
                        'quantity_upto': 70,
                        'children': []
                    },
                    {
                        'item_no': '2.1.2',
                        'description': 'MANUAL EXCAVATION',
                        'quantity_since': 30,
                        'quantity_upto': 30,
                        'children': []
                    }
                ]
            },
            {
                'item_no': '2.2',
                'description': 'CONCRETE',
                'quantity_since': 85,
                'quantity_upto': 85,
                'children': [
                    {
                        'item_no': '2.2.1',
                        'description': 'RCC M20',
                        'quantity_since': 50,
                        'quantity_upto': 50,
                        'children': []
                    },
                    {
                        'item_no': '2.2.2',
                        'description': 'RCC M25',
                        'quantity_since': 35,
                        'quantity_upto': 35,
                        'children': []
                    }
                ]
            }
        ]
    }
]

print("Testing hierarchical filtering logic...")
print(f"Original items: {len(test_data)}")

# Apply filtering
filtered_data = filter_zero_hierarchy(test_data)

print(f"Filtered items: {len(filtered_data)}")

# Print results
for item in filtered_data:
    print(f"Root item: {item['item_no']} - {item['description']}")
    for child in item.get('children', []):
        print(f"  Child: {child['item_no']} - {child['description']}")
        for grandchild in child.get('children', []):
            print(f"    Grandchild: {grandchild['item_no']} - {grandchild['description']}")

print("\nExpected result: Only item 2.0 and its descendants should remain")
print("Verification:", "PASS" if len(filtered_data) == 1 and filtered_data[0]['item_no'] == '2.0' else "FAIL")
#!/usr/bin/env python3
"""
Utility script to display the first 20 rows of title data from Excel files
in a clear, formatted manner for verification.
"""

import pandas as pd
import json
from pathlib import Path
from core.processors.excel_processor import ExcelProcessor

def display_first_20_rows_from_excel(file_path, max_rows=20):
    """
    Display the first 20 rows of title data from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file
        max_rows (int): Maximum number of rows to display (default: 20)
        
    Returns:
        dict: Extracted title data
    """
    try:
        print(f"Displaying first {max_rows} rows from: {Path(file_path).name}")
        print("=" * 60)
        
        # Read the Title sheet directly
        title_df = pd.read_excel(file_path, 'Title', header=None)
        
        # Display raw data
        print("RAW TITLE DATA:")
        print("-" * 30)
        for index, row in title_df.head(max_rows).iterrows():
            if len(row) >= 2:
                key = str(row[0]).strip() if pd.notna(row[0]) else "EMPTY"
                value = str(row[1]).strip() if pd.notna(row[1]) else "EMPTY"
                print(f"{index+1:2d}. {key:<30} : {value}")
        
        print("\n" + "=" * 60)
        
        # Process using our ExcelProcessor
        processor = ExcelProcessor()
        processed_data = processor.process_excel(file_path)
        title_data = processed_data.get('title_data', {})
        
        # Display processed data
        print("PROCESSED TITLE DATA:")
        print("-" * 30)
        print(f"Total keys in processed data: {len(title_data)}")
        print(f"First 20 rows processed: {title_data.get('_first_20_rows_processed', False)}")
        print(f"First 20 rows count: {title_data.get('_first_20_rows_count', 0)}")
        
        print("\nKEY-VALUE PAIRS:")
        print("-" * 30)
        row_counter = 0
        for key, value in title_data.items():
            # Skip internal metadata keys for cleaner display
            if not key.startswith('_'):
                print(f"{row_counter+1:2d}. {key:<30} : {value}")
                row_counter += 1
                if row_counter >= max_rows:
                    break
        
        # Show any additional metadata
        print("\nMETADATA:")
        print("-" * 30)
        for key, value in title_data.items():
            if key.startswith('_'):
                print(f"{key:<30} : {value}")
        
        return title_data
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {}

def compare_first_20_rows_across_files(file_paths):
    """
    Compare the first 20 rows of title data across multiple files.
    
    Args:
        file_paths (list): List of file paths to compare
    """
    print("COMPARING FIRST 20 ROWS ACROSS FILES")
    print("=" * 60)
    
    all_title_data = {}
    
    # Process each file
    for file_path in file_paths:
        print(f"\nProcessing: {Path(file_path).name}")
        processor = ExcelProcessor()
        try:
            processed_data = processor.process_excel(file_path)
            title_data = processed_data.get('title_data', {})
            all_title_data[Path(file_path).name] = title_data
            
            print(f"  Rows processed: {title_data.get('_first_20_rows_count', 0)}")
            print(f"  Total keys: {len(title_data)}")
        except Exception as e:
            print(f"  Error: {e}")
            all_title_data[Path(file_path).name] = {}
    
    # Compare common keys
    if all_title_data:
        print("\nCOMMON KEYS ANALYSIS:")
        print("-" * 30)
        
        # Get all keys from all files
        all_keys = set()
        for title_data in all_title_data.values():
            all_keys.update(key for key in title_data.keys() if not key.startswith('_'))
        
        # Count occurrences of each key
        key_occurrences = {}
        for key in all_keys:
            count = sum(1 for title_data in all_title_data.values() if key in title_data)
            key_occurrences[key] = count
        
        # Show keys that appear in all files
        common_keys = [key for key, count in key_occurrences.items() if count == len(all_title_data)]
        print(f"Keys present in all files ({len(all_title_data)}): {len(common_keys)}")
        for key in sorted(common_keys)[:10]:  # Show first 10
            print(f"  - {key}")
        if len(common_keys) > 10:
            print(f"  ... and {len(common_keys) - 10} more")
        
        # Show keys that appear in some files
        partial_keys = [key for key, count in key_occurrences.items() if 0 < count < len(all_title_data)]
        print(f"\nKeys present in some files: {len(partial_keys)}")
        for key in sorted(partial_keys)[:10]:  # Show first 10
            files_with_key = [filename for filename, title_data in all_title_data.items() if key in title_data]
            print(f"  - {key} (in {len(files_with_key)} files)")
        if len(partial_keys) > 10:
            print(f"  ... and {len(partial_keys) - 10} more")
        
        # Show sample values for common keys
        if common_keys:
            print("\nSAMPLE VALUES FOR COMMON KEYS:")
            print("-" * 30)
            for key in sorted(common_keys)[:5]:  # Show first 5
                print(f"{key}:")
                for filename, title_data in all_title_data.items():
                    value = title_data.get(key, "NOT FOUND")
                    print(f"  {filename:<20} : {value}")
                print()

def export_first_20_rows_to_json(file_path, output_path=None):
    """
    Export the first 20 rows of title data to JSON format.
    
    Args:
        file_path (str): Path to the Excel file
        output_path (str): Path to output JSON file (optional)
        
    Returns:
        str: Path to the exported JSON file
    """
    print(f"Exporting first 20 rows from: {Path(file_path).name}")
    
    # Process the file
    processor = ExcelProcessor()
    processed_data = processor.process_excel(file_path)
    title_data = processed_data.get('title_data', {})
    
    # Filter to first 20 rows data only (exclude internal metadata)
    filtered_data = {k: v for k, v in title_data.items() if not k.startswith('_')}
    
    # Limit to first 20 entries if there are more
    if len(filtered_data) > 20:
        filtered_data = dict(list(filtered_data.items())[:20])
    
    # Add metadata
    export_data = {
        "source_file": str(file_path),
        "extraction_timestamp": pd.Timestamp.now().isoformat(),
        "total_keys_extracted": len(title_data),
        "first_20_rows_processed": title_data.get('_first_20_rows_processed', False),
        "first_20_rows_count": title_data.get('_first_20_rows_count', 0),
        "title_data_first_20_rows": filtered_data
    }
    
    # Determine output path
    if not output_path:
        output_path = Path(file_path).with_suffix('.first_20_rows.json')
    
    # Export to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"Exported to: {output_path}")
    return str(output_path)

def main():
    """Main function to demonstrate first 20 rows display functionality."""
    import sys
    from pathlib import Path
    
    if len(sys.argv) < 2:
        print("Usage: python display_first_20_rows.py <excel_file> [excel_file2] ...")
        print("Options:")
        print("  Single file: Display first 20 rows")
        print("  Multiple files: Compare first 20 rows across files")
        return
    
    file_paths = sys.argv[1:]
    
    # Check if files exist
    valid_files = []
    for file_path in file_paths:
        if Path(file_path).exists():
            valid_files.append(file_path)
        else:
            print(f"Warning: File not found - {file_path}")
    
    if not valid_files:
        print("No valid files found.")
        return
    
    if len(valid_files) == 1:
        # Single file display
        file_path = valid_files[0]
        title_data = display_first_20_rows_from_excel(file_path)
        
        # Offer to export to JSON
        export_choice = input("\nExport to JSON? (y/N): ").strip().lower()
        if export_choice == 'y':
            export_first_20_rows_to_json(file_path)
    else:
        # Multiple file comparison
        compare_first_20_rows_across_files(valid_files)
        
        # Offer to export each file to JSON
        export_choice = input("\nExport each file to JSON? (y/N): ").strip().lower()
        if export_choice == 'y':
            for file_path in valid_files:
                try:
                    export_first_20_rows_to_json(file_path)
                except Exception as e:
                    print(f"Failed to export {file_path}: {e}")

if __name__ == "__main__":
    main()
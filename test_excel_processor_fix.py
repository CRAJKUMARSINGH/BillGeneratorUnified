import pandas as pd
from core.processors.excel_processor import ExcelProcessor

def test_excel_processor():
    """Test the Excel processor with actual files"""
    processor = ExcelProcessor()
    
    # Test with one of the actual files
    test_files = [
        "input/0511-N-extra.xlsx",
        "input/3rdFinalNoExtra.xlsx",
        "input/FirstFINALnoExtra.xlsx"
    ]
    
    for file_path in test_files:
        print(f"\n{'='*60}")
        print(f"Testing file: {file_path}")
        print('='*60)
        
        try:
            # Process the Excel file
            result = processor.process_excel(file_path, required_cols_only=True)
            
            print("✅ Processing successful!")
            
            # Show results
            for key, data in result.items():
                if isinstance(data, pd.DataFrame):
                    print(f"\n--- {key} ---")
                    print(f"Shape: {data.shape}")
                    if not data.empty:
                        print(f"Columns: {list(data.columns)}")
                        print("First few rows:")
                        print(data.head(3))
                else:
                    print(f"\n--- {key} ---")
                    if isinstance(data, dict):
                        print(f"Keys: {list(data.keys())[:10]}")  # Show first 10 keys
                    else:
                        print(f"Type: {type(data)}")
                        
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_excel_processor()
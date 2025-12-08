import pandas as pd

def analyze_excel_file(file_path):
    """Analyze the structure of an Excel file"""
    print(f"Analyzing file: {file_path}")
    
    try:
        # Read Excel file
        excel_data = pd.ExcelFile(file_path, engine='openpyxl')
        
        print(f"Available sheets: {excel_data.sheet_names}")
        
        # Analyze each sheet
        for sheet_name in excel_data.sheet_names:
            print(f"\n--- Sheet: {sheet_name} ---")
            try:
                # Read first few rows to understand structure
                df = pd.read_excel(excel_data, sheet_name, nrows=5)
                print(f"Columns: {list(df.columns)}")
                print("First few rows:")
                print(df.head())
                print(f"Data types:\n{df.dtypes}")
            except Exception as e:
                print(f"Error reading sheet {sheet_name}: {e}")
                
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    # Analyze multiple input files to understand the pattern
    files_to_analyze = [
        "input/0511-N-extra.xlsx",
        "input/3rdFinalNoExtra.xlsx",
        "input/FirstFINALnoExtra.xlsx"
    ]
    
    for file_path in files_to_analyze:
        analyze_excel_file(file_path)
        print("\n" + "="*50 + "\n")
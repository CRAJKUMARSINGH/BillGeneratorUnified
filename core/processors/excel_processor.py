import pandas as pd
from typing import Dict, Any
import io
from core.processors.hierarchical_filter import apply_hierarchical_filtering

class ExcelProcessor:
    """Process Excel files and extract bill data"""
    
    def __init__(self):
        self.required_sheets = ['Title', 'Work Order', 'Bill Quantity']
        self.optional_sheets = ['Extra Items', 'Deviation']
    
    def process_excel(self, file, required_cols_only=True) -> Dict[str, Any]:
        """
        Process Excel file and extract all necessary data with optimization
        
        Args:
            file: Uploaded file object or file path
            required_cols_only: Whether to load only required columns for better performance
            
        Returns:
            Dictionary containing processed data
        """
        # Read Excel file
        if hasattr(file, 'read'):
            # It's a file-like object (BytesIO or file object)
            if isinstance(file, io.BytesIO):
                # It's already a BytesIO object
                excel_data = pd.ExcelFile(file, engine='openpyxl')
            else:
                # It's a file object
                file_bytes = file.read()
                # Reset file pointer if possible
                if hasattr(file, 'seek') and hasattr(file, 'tell'):
                    file.seek(0)
                
                # Try to determine the file type from the first bytes
                if file_bytes.startswith(b'PK'):
                    # Likely an .xlsx file
                    excel_data = pd.ExcelFile(io.BytesIO(file_bytes), engine='openpyxl')
                else:
                    # Likely an .xls file
                    excel_data = pd.ExcelFile(io.BytesIO(file_bytes), engine='xlrd')
        else:
            # It's a file path
            # Determine engine based on file extension
            if str(file).endswith('.xlsx'):
                excel_data = pd.ExcelFile(file, engine='openpyxl')
            else:
                excel_data = pd.ExcelFile(file, engine='xlrd')
        
        # Define required columns per sheet for optimization
        required_cols = {
            'Work Order': ['Item No.', 'Description', 'Unit', 'Quantity', 'Rate'],
            'Bill Quantity': ['Item No.', 'Description', 'Quantity', 'Rate'],
            'Extra Items': ['Item No.', 'Description', 'Unit', 'Quantity', 'Rate'],
        }
        
        processed_data = {}
        
        # Process Title sheet
        if 'Title' in excel_data.sheet_names:
            title_df = pd.read_excel(excel_data, 'Title', header=None)
            processed_data['title_data'] = self._process_title_sheet(title_df)
        else:
            processed_data['title_data'] = {}
        
        # Process Work Order sheet with column selection
        if 'Work Order' in excel_data.sheet_names:
            cols = required_cols['Work Order'] if required_cols_only else None
            work_order_df = pd.read_excel(
                excel_data, 
                'Work Order',
                usecols=cols,
                dtype={'Item No.': str}  # Optimize data types
            )
            processed_data['work_order_data'] = work_order_df
        else:
            processed_data['work_order_data'] = pd.DataFrame()
        
        # Process Bill Quantity sheet with column selection
        if 'Bill Quantity' in excel_data.sheet_names:
            cols = required_cols['Bill Quantity'] if required_cols_only else None
            bill_qty_df = pd.read_excel(
                excel_data, 
                'Bill Quantity',
                usecols=cols,
                dtype={'Item No.': str}  # Optimize data types
            )
            processed_data['bill_quantity_data'] = bill_qty_df
        else:
            processed_data['bill_quantity_data'] = pd.DataFrame()
        
        # Process Extra Items sheet (optional) with column selection
        if 'Extra Items' in excel_data.sheet_names:
            cols = required_cols['Extra Items'] if required_cols_only else None
            extra_items_df = pd.read_excel(
                excel_data, 
                'Extra Items',
                usecols=cols,
                dtype={'Item No.': str}  # Optimize data types
            )
            processed_data['extra_items_data'] = extra_items_df
        else:
            processed_data['extra_items_data'] = pd.DataFrame()
        
        # Process Deviation sheet (optional)
        if 'Deviation' in excel_data.sheet_names:
            deviation_df = pd.read_excel(excel_data, 'Deviation')
            processed_data['deviation_data'] = deviation_df
        else:
            processed_data['deviation_data'] = pd.DataFrame()
        
        # Apply hierarchical filtering
        filtered_data = apply_hierarchical_filtering(
            work_order_data=processed_data['work_order_data'],
            bill_quantity_data=processed_data['bill_quantity_data']
        )
        processed_data.update(filtered_data)
        
        return processed_data
    
    def _process_title_sheet(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Process Title sheet which contains key-value pairs
        
        Expected format:
        Column 0: Key names
        Column 1: Values
        """
        title_data = {}
        
        # Process all rows but specifically track first 20 for validation
        first_20_rows = {}
        
        for index, row in df.iterrows():
            if len(row) >= 2:
                key = str(row[0]).strip() if pd.notna(row[0]) else None
                value = row[1] if pd.notna(row[1]) else None
                
                if key and key != 'nan':
                    title_data[key] = value
                    
                    # Track first 20 rows for validation purposes
                    if index < 20:
                        first_20_rows[key] = value
        
        # Add metadata about first 20 rows processing
        title_data['_first_20_rows_processed'] = True
        title_data['_first_20_rows_count'] = len(first_20_rows)
        
        return title_data
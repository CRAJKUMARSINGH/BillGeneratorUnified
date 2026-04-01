"""
Shared UI helper functions and classes for BillGenerator Unified.
Includes ChangeLogger for audit trails and safe conversion utilities.
"""
import pandas as pd
from datetime import datetime
import streamlit as st
import json
from typing import Dict, List, Tuple, Optional, Any

class ChangeLogger:
    """Track all modifications for audit trail in session state"""
    
    @staticmethod
    def initialize():
        """Initialize change log in session state"""
        if 'change_log' not in st.session_state:
            st.session_state.change_log = []
    
    @staticmethod
    def log_change(item_no: str, field: str, old_value: Any, new_value: Any, reason: str = "Manual Edit"):
        """Log a change with timestamp"""
        if 'change_log' not in st.session_state:
            ChangeLogger.initialize()
            
        change_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'item_no': item_no,
            'field': field,
            'old_value': old_value,
            'new_value': new_value,
            'reason': reason,
            'user': 'Admin'
        }
        st.session_state.change_log.append(change_entry)
    
    @staticmethod
    def get_changes() -> List[Dict[str, Any]]:
        """Get all changes"""
        return st.session_state.get('change_log', [])
    
    @staticmethod
    def export_to_dataframe() -> pd.DataFrame:
        """Export change log to DataFrame"""
        changes = st.session_state.get('change_log', [])
        if changes:
            return pd.DataFrame(changes)
        return pd.DataFrame(columns=['timestamp', 'item_no', 'field', 'old_value', 'new_value', 'reason', 'user'])
    
    @staticmethod
    def clear():
        """Clear change log"""
        st.session_state.change_log = []

def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float with fallback"""
    try:
        if value is None or value == '' or str(value).lower() == 'nan':
            return default
        # Remove currency symbols and commas
        clean_val = str(value).replace('₹', '').replace(',', '').strip()
        import math
        f_val = float(clean_val)
        return f_val if not math.isnan(f_val) else default
    except (ValueError, TypeError):
        return default

def update_validation_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Update validation status for each row based on data completeness.
    Status indicators:
    - ⚪ Empty: All fields empty
    - 🟢 Valid: Description + Quantity > 0 + Rate > 0
    - 🟠 Partial: Description but missing Qty or Rate
    - 🔴 Invalid: No description but has Qty or Rate
    """
    if df is None or df.empty:
        return df
        
    result = df.copy()
    if 'Status' not in result.columns:
        result.insert(0, 'Status', '⚪')
        
    for idx, row in result.iterrows():
        qty = safe_float(row.get('Quantity', row.get('Bill Quantity', 0)))
        rate = safe_float(row.get('Rate', row.get('Bill Rate', 0)))
        desc = str(row.get('Description', '')).strip()
        
        is_active = qty > 0 or rate > 0 or desc != ''
        
        if not is_active:
            status = '⚪'
        elif desc and qty > 0 and rate > 0:
            status = '🟢'
        elif desc == '' and (qty > 0 or rate > 0):
            status = '🔴 No Desc'
        elif desc != '' and (qty == 0 or rate == 0):
            status = '🟠 Miss Q/R'
        else:
            status = '🔴 Inv'
            
        result.at[idx, 'Status'] = status
        
    return result

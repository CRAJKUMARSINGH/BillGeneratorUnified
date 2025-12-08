"""
Base Generator - Base class for all document generators
"""
import pandas as pd
from typing import Dict, Any
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os

class BaseGenerator:
    """Base class for all document generators"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.title_data = data.get('title_data', {})
        self.work_order_data = data.get('work_order_data', pd.DataFrame())
        self.bill_quantity_data = data.get('bill_quantity_data', pd.DataFrame())
        self.extra_items_data = data.get('extra_items_data', pd.DataFrame())
        
        # Set up Jinja2 environment for templates
        template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        
        # Template cache
        self._template_cache = {}
    
    def _safe_float(self, value) -> float:
        """Safely convert value to float"""
        if pd.isna(value) or value is None or value == '':
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def _safe_serial_no(self, value) -> str:
        """Safely convert serial number to string"""
        if pd.isna(value) or value is None:
            return ''
        return str(value)
    
    def _format_unit_or_text(self, value) -> str:
        """Format unit or text value"""
        if pd.isna(value) or value is None:
            return ''
        return str(value)
    
    def _format_number(self, value) -> str:
        """Format number for display"""
        if value == 0:
            return ''
        return f"{value:.2f}"
    
    def _number_to_words(self, num: int) -> str:
        """Convert number to words (simplified version)"""
        ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        
        if num == 0:
            return 'Zero'
        
        if num < 10:
            return ones[num]
        elif num < 20:
            return teens[num - 10]
        elif num < 100:
            return tens[num // 10] + ('' if num % 10 == 0 else ' ' + ones[num % 10])
        elif num < 1000:
            return ones[num // 100] + ' Hundred' + ('' if num % 100 == 0 else ' ' + self._number_to_words(num % 100))
        elif num < 100000:
            return self._number_to_words(num // 1000) + ' Thousand' + ('' if num % 1000 == 0 else ' ' + self._number_to_words(num % 1000))
        else:
            return str(num)  # For very large numbers, just return as string
    
    def _has_extra_items(self) -> bool:
        """Check if there are extra items to include"""
        if isinstance(self.extra_items_data, pd.DataFrame):
            return not self.extra_items_data.empty
        return False
    
    def get_template(self, template_name: str):
        """Cache loaded templates"""
        if template_name not in self._template_cache:
            self._template_cache[template_name] = self.jinja_env.get_template(template_name)
        return self._template_cache[template_name]
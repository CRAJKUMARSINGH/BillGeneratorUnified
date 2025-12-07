import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import openpyxl
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from pathlib import Path
import threading
import time

from utils.memory_manager import get_memory_manager
from utils.cache_manager import get_cache_manager
from utils.error_handler import get_error_handler, handle_errors

@dataclass
class ExcelConfig:
    max_rows_per_batch: int = 1000
    auto_save_interval: int = 300  # seconds
    backup_enabled: bool = True
    validation_enabled: bool = True
    memory_optimization: bool = True

@dataclass
class ExcelData:
    sheet_name: str
    data: List[Dict[str, Any]]
    headers: List[str]
    row_count: int
    file_path: str

class ExcelModeEnhanced:
    """Enhanced Excel processing mode with optimization"""
    
    def __init__(self, parent):
        self.parent = parent
        self.logger = logging.getLogger(__name__)
        
        # Managers
        self.memory_manager = get_memory_manager()
        self.cache_manager = get_cache_manager()
        self.error_handler = get_error_handler()
        
        # Configuration
        self.config = ExcelConfig()
        
        # Data storage
        self.current_data: Optional[ExcelData] = None
        self.modified_data: Dict[str, List[Dict[str, Any]]] = {}
        
        # UI components
        self.setup_ui()
        
        # Auto-save timer
        self.last_save_time = time.time()
        self.auto_save_timer()
        
    def setup_ui(self):
        """Setup enhanced Excel UI"""
        # Main frame
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Enhanced Excel Mode", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # File operations frame
        file_frame = ttk.LabelFrame(main_frame, text="File Operations", padding="5")
        file_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Open Excel", 
                  command=self.open_excel_file).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="Save", 
                  command=self.save_excel_file).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Save As", 
                  command=self.save_as_excel_file).grid(row=0, column=2, padx=5)
        ttk.Button(file_frame, text="New Excel", 
                  command=self.new_excel_file).grid(row=0, column=3, padx=5)
        
        # Data operations frame
        data_frame = ttk.LabelFrame(main_frame, text="Data Operations", padding="5")
        data_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(data_frame, text="Add Row", 
                  command=self.add_row).grid(row=0, column=0, padx=5)
        ttk.Button(data_frame, text="Delete Row", 
                  command=self.delete_row).grid(row=0, column=1, padx=5)
        ttk.Button(data_frame, text="Validate Data", 
                  command=self.validate_data).grid(row=0, column=2, padx=5)
        ttk.Button(data_frame, text="Clear Data", 
                  command=self.clear_data).grid(row=0, column=3, padx=5)
        
        # Batch operations frame
        batch_frame = ttk.LabelFrame(main_frame, text="Batch Operations", padding="5")
        batch_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(batch_frame, text="Import CSV", 
                  command=self.import_csv).grid(row=0, column=0, padx=5)
        ttk.Button(batch_frame, text="Export CSV", 
                  command=self.export_csv).grid(row=0, column=1, padx=5)
        ttk.Button(batch_frame, text="Process Batch", 
                  command=self.process_batch).grid(row=0, column=2, padx=5)
        ttk.Button(batch_frame, text="Analyze Data", 
                  command=self.analyze_data).grid(row=0, column=3, padx=5)
        
        # Data display frame
        display_frame = ttk.LabelFrame(main_frame, text="Data Display", padding="5")
        display_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create treeview for data display
        self.tree = ttk.Treeview(display_frame, show='headings')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(display_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.memory_label = ttk.Label(status_frame, text="Memory: Calculating...")
        self.memory_label.grid(row=0, column=1, padx=20)
        
        self.rows_label = ttk.Label(status_frame, text="Rows: 0")
        self.rows_label.grid(row=0, column=2)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_cell_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Start status update timer
        self.update_status()
        
    @handle_errors(category="FILE_IO")
    def open_excel_file(self):
        """Open Excel file"""
        filename = filedialog.askopenfilename(
            title="Open Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.load_excel_file(filename)
                self.status_label.config(text=f"Loaded: {Path(filename).name}")
            except Exception as e:
                self.logger.error(f"Error opening Excel file: {e}")
                messagebox.showerror("Error", f"Failed to open Excel file: {e}")
                
    def load_excel_file(self, file_path: str):
        """Load Excel file with optimization"""
        try:
            # Check cache first
            cache_key = f"excel_file_{file_path}_{Path(file_path).stat().st_mtime}"
            cached_data = self.cache_manager.get(cache_key, "excel")
            
            if cached_data:
                self.current_data = cached_data
                self.display_data()
                self.logger.info(f"Excel file loaded from cache: {file_path}")
                return
                
            # Load file with memory optimization
            if self.config.memory_optimization:
                # Load in chunks for large files
                self.load_excel_chunked(file_path)
            else:
                # Load normally
                self.load_excel_normal(file_path)
                
            # Cache the loaded data
            if self.current_data:
                self.cache_manager.set(cache_key, self.current_data, "excel")
                
        except Exception as e:
            self.logger.error(f"Error loading Excel file: {e}")
            raise
            
    def load_excel_normal(self, file_path: str):
        """Load Excel file normally"""
        # Load all sheets
        excel_file = pd.ExcelFile(file_path)
        
        # For now, load the first sheet
        sheet_name = excel_file.sheet_names[0]
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Convert to list of dictionaries
        data = df.to_dict('records')
        headers = df.columns.tolist()
        
        self.current_data = ExcelData(
            sheet_name=sheet_name,
            data=data,
            headers=headers,
            row_count=len(data),
            file_path=file_path
        )
        
        self.display_data()
        
    def load_excel_chunked(self, file_path: str):
        """Load Excel file in chunks for memory optimization"""
        # For large files, read in chunks
        chunk_size = self.config.max_rows_per_batch
        
        # Read first chunk to get headers
        df_first_chunk = pd.read_excel(file_path, nrows=chunk_size)
        headers = df_first_chunk.columns.tolist()
        
        # Read all data in chunks
        all_data = []
        for chunk in pd.read_excel(file_path, chunksize=chunk_size):
            chunk_data = chunk.to_dict('records')
            all_data.extend(chunk_data)
            
            # Update memory usage
            memory_stats = self.memory_manager.get_memory_stats()
            if memory_stats.memory_percent > 80:
                self.logger.warning("High memory usage during Excel loading")
                break
                
        self.current_data = ExcelData(
            sheet_name="Sheet1",
            data=all_data,
            headers=headers,
            row_count=len(all_data),
            file_path=file_path
        )
        
        self.display_data()
        
    def display_data(self):
        """Display data in treeview"""
        if not self.current_data:
            return
            
        # Clear existing data
        self.tree.delete(*self.tree.get_children())
        
        # Set up columns
        self.tree['columns'] = self.current_data.headers
        for header in self.current_data.headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=100)
            
        # Add data (limit display for performance)
        max_display = min(1000, len(self.current_data.data))
        for i, row in enumerate(self.current_data.data[:max_display]):
            values = [row.get(header, '') for header in self.current_data.headers]
            self.tree.insert('', 'end', values=values)
            
        self.rows_label.config(text=f"Rows: {self.current_data.row_count}")
        
    def new_excel_file(self):
        """Create new Excel file"""
        # Default headers
        headers = ['ID', 'Name', 'Description', 'Quantity', 'Price', 'Total']
        
        self.current_data = ExcelData(
            sheet_name="Sheet1",
            data=[],
            headers=headers,
            row_count=0,
            file_path=""
        )
        
        self.display_data()
        self.status_label.config(text="New Excel file created")
        
    def add_row(self):
        """Add new row"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No Excel file loaded")
            return
            
        # Create dialog for new row
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Row")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Entry fields for each column
        entries = {}
        for i, header in enumerate(self.current_data.headers):
            ttk.Label(dialog, text=f"{header}:").grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[header] = entry
            
        def save_row():
            new_row = {}
            for header, entry in entries.items():
                new_row[header] = entry.get().strip()
                
            self.current_data.data.append(new_row)
            self.current_data.row_count += 1
            
            # Mark as modified
            if self.current_data.file_path not in self.modified_data:
                self.modified_data[self.current_data.file_path] = []
            self.modified_data[self.current_data.file_path].append(new_row)
            
            self.display_data()
            self.status_label.config(text="Row added")
            dialog.destroy()
            
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(self.current_data.headers), column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_row).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).grid(row=0, column=1, padx=5)
        
    def delete_row(self):
        """Delete selected row"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a row to delete")
            return
            
        if messagebox.askyesno("Confirm", "Delete selected row?"):
            # Get selected row index
            item = selection[0]
            row_index = self.tree.index(item)
            
            if row_index < len(self.current_data.data):
                del self.current_data.data[row_index]
                self.current_data.row_count -= 1
                
                self.display_data()
                self.status_label.config(text="Row deleted")
                
    def validate_data(self):
        """Validate Excel data"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No Excel file loaded")
            return
            
        validation_errors = []
        
        # Check for required fields
        required_fields = ['ID', 'Name']
        for field in required_fields:
            if field in self.current_data.headers:
                for i, row in enumerate(self.current_data.data):
                    if not row.get(field):
                        validation_errors.append(f"Row {i+1}: {field} is required")
                        
        # Check numeric fields
        numeric_fields = ['Quantity', 'Price', 'Total']
        for field in numeric_fields:
            if field in self.current_data.headers:
                for i, row in enumerate(self.current_data.data):
                    value = row.get(field)
                    if value:
                        try:
                            float(value)
                        except ValueError:
                            validation_errors.append(f"Row {i+1}: {field} must be numeric")
                            
        if validation_errors:
            # Show validation errors
            error_dialog = tk.Toplevel(self.parent)
            error_dialog.title("Validation Errors")
            error_dialog.geometry("500x400")
            error_dialog.transient(self.parent)
            
            text_widget = tk.Text(error_dialog, wrap=tk.WORD)
            scrollbar = ttk.Scrollbar(error_dialog, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            for error in validation_errors:
                text_widget.insert(tk.END, error + "\n")
                
            ttk.Button(error_dialog, text="Close", 
                      command=error_dialog.destroy).grid(row=1, column=0, pady=10)
                      
        else:
            messagebox.showinfo("Validation", "All data is valid!")
            
    def clear_data(self):
        """Clear all data"""
        if messagebox.askyesno("Confirm", "Clear all data?"):
            self.current_data = None
            self.tree.delete(*self.tree.get_children())
            self.status_label.config(text="Data cleared")
            
    def import_csv(self):
        """Import CSV file"""
        filename = filedialog.askopenfilename(
            title="Import CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                df = pd.read_csv(filename)
                data = df.to_dict('records')
                headers = df.columns.tolist()
                
                self.current_data = ExcelData(
                    sheet_name="Imported",
                    data=data,
                    headers=headers,
                    row_count=len(data),
                    file_path=filename
                )
                
                self.display_data()
                self.status_label.config(text=f"CSV imported: {Path(filename).name}")
                
            except Exception as e:
                self.logger.error(f"Error importing CSV: {e}")
                messagebox.showerror("Error", f"Failed to import CSV: {e}")
                
    def export_csv(self):
        """Export to CSV file"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Export CSV File",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                df = pd.DataFrame(self.current_data.data)
                df.to_csv(filename, index=False)
                self.status_label.config(text=f"CSV exported: {Path(filename).name}")
                
            except Exception as e:
                self.logger.error(f"Error exporting CSV: {e}")
                messagebox.showerror("Error", f"Failed to export CSV: {e}")
                
    def process_batch(self):
        """Process batch operations"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to process")
            return
            
        # Show batch processing dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Batch Processing")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select operation:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        
        operation_var = tk.StringVar(value="calculate_totals")
        operations = [
            ("Calculate Totals", "calculate_totals"),
            ("Remove Duplicates", "remove_duplicates"),
            ("Sort by Name", "sort_by_name"),
            ("Filter by Price", "filter_by_price")
        ]
        
        for i, (text, value) in enumerate(operations):
            ttk.Radiobutton(dialog, text=text, variable=operation_var, 
                           value=value).grid(row=i+1, column=0, sticky=tk.W, padx=20, pady=5)
                           
        def execute_operation():
            operation = operation_var.get()
            
            if operation == "calculate_totals":
                self.calculate_totals()
            elif operation == "remove_duplicates":
                self.remove_duplicates()
            elif operation == "sort_by_name":
                self.sort_by_name()
            elif operation == "filter_by_price":
                self.filter_by_price()
                
            self.status_label.config(text=f"Batch operation completed: {operation}")
            dialog.destroy()
            
        ttk.Button(dialog, text="Execute", command=execute_operation).grid(row=len(operations)+1, column=0, pady=20)
        
    def calculate_totals(self):
        """Calculate totals for rows"""
        if 'Quantity' in self.current_data.headers and 'Price' in self.current_data.headers:
            for row in self.current_data.data:
                try:
                    quantity = float(row.get('Quantity', 0))
                    price = float(row.get('Price', 0))
                    row['Total'] = quantity * price
                except ValueError:
                    row['Total'] = 0
                    
            if 'Total' not in self.current_data.headers:
                self.current_data.headers.append('Total')
                
            self.display_data()
            
    def remove_duplicates(self):
        """Remove duplicate rows"""
        if 'ID' in self.current_data.headers:
            seen_ids = set()
            unique_data = []
            
            for row in self.current_data.data:
                row_id = row.get('ID')
                if row_id not in seen_ids:
                    seen_ids.add(row_id)
                    unique_data.append(row)
                    
            self.current_data.data = unique_data
            self.current_data.row_count = len(unique_data)
            self.display_data()
            
    def sort_by_name(self):
        """Sort data by name"""
        if 'Name' in self.current_data.headers:
            self.current_data.data.sort(key=lambda x: x.get('Name', ''))
            self.display_data()
            
    def filter_by_price(self):
        """Filter data by price"""
        if 'Price' in self.current_data.headers:
            # Show filter dialog
            dialog = tk.Toplevel(self.parent)
            dialog.title("Filter by Price")
            dialog.geometry("300x150")
            dialog.transient(self.parent)
            dialog.grab_set()
            
            ttk.Label(dialog, text="Minimum Price:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
            min_price_var = tk.StringVar(value="0")
            ttk.Entry(dialog, textvariable=min_price_var).grid(row=0, column=1, padx=10, pady=10)
            
            ttk.Label(dialog, text="Maximum Price:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
            max_price_var = tk.StringVar(value="999999")
            ttk.Entry(dialog, textvariable=max_price_var).grid(row=1, column=1, padx=10, pady=10)
            
            def apply_filter():
                try:
                    min_price = float(min_price_var.get())
                    max_price = float(max_price_var.get())
                    
                    filtered_data = []
                    for row in self.current_data.data:
                        try:
                            price = float(row.get('Price', 0))
                            if min_price <= price <= max_price:
                                filtered_data.append(row)
                        except ValueError:
                            continue
                            
                    self.current_data.data = filtered_data
                    self.current_data.row_count = len(filtered_data)
                    self.display_data()
                    dialog.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Invalid price values")
                    
            ttk.Button(dialog, text="Apply", command=apply_filter).grid(row=2, column=0, columnspan=2, pady=20)
            
    def analyze_data(self):
        """Analyze data and show statistics"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to analyze")
            return
            
        # Calculate statistics
        total_rows = len(self.current_data.data)
        numeric_columns = []
        
        for header in self.current_data.headers:
            try:
                values = [float(row.get(header, 0)) for row in self.current_data.data if row.get(header)]
                if values:
                    numeric_columns.append({
                        'name': header,
                        'count': len(values),
                        'sum': sum(values),
                        'avg': sum(values) / len(values),
                        'min': min(values),
                        'max': max(values)
                    })
            except ValueError:
                continue
                
        # Show analysis dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Data Analysis")
        dialog.geometry("500x400")
        dialog.transient(self.parent)
        
        text_widget = tk.Text(dialog, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Display statistics
        text_widget.insert(tk.END, f"Total Rows: {total_rows}\n\n")
        text_widget.insert(tk.END, "Numeric Columns Analysis:\n")
        text_widget.insert(tk.END, "-" * 40 + "\n")
        
        for col in numeric_columns:
            text_widget.insert(tk.END, f"\n{col['name']}:\n")
            text_widget.insert(tk.END, f"  Count: {col['count']}\n")
            text_widget.insert(tk.END, f"  Sum: {col['sum']:.2f}\n")
            text_widget.insert(tk.END, f"  Average: {col['avg']:.2f}\n")
            text_widget.insert(tk.END, f"  Min: {col['min']:.2f}\n")
            text_widget.insert(tk.END, f"  Max: {col['max']:.2f}\n")
            
        ttk.Button(dialog, text="Close", command=dialog.destroy).grid(row=1, column=0, pady=10)
        
    def save_excel_file(self):
        """Save Excel file"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to save")
            return
            
        if self.current_data.file_path:
            self.save_to_file(self.current_data.file_path)
        else:
            self.save_as_excel_file()
            
    def save_as_excel_file(self):
        """Save Excel file as"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to save")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        
        if filename:
            self.save_to_file(filename)
            self.current_data.file_path = filename
            
    def save_to_file(self, file_path: str):
        """Save data to Excel file"""
        try:
            df = pd.DataFrame(self.current_data.data)
            df.to_excel(file_path, index=False)
            self.status_label.config(text=f"Saved: {Path(file_path).name}")
            self.last_save_time = time.time()
            
        except Exception as e:
            self.logger.error(f"Error saving Excel file: {e}")
            messagebox.showerror("Error", f"Failed to save Excel file: {e}")
            
    def on_cell_double_click(self, event):
        """Handle cell double click for editing"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = selection[0]
        column = self.tree.identify_column(event.x)
        row_index = self.tree.index(item)
        
        if column and row_index < len(self.current_data.data):
            col_index = int(column[1:]) - 1
            if col_index < len(self.current_data.headers):
                header = self.current_data.headers[col_index]
                current_value = self.current_data.data[row_index].get(header, '')
                
                # Create edit dialog
                dialog = tk.Toplevel(self.parent)
                dialog.title(f"Edit {header}")
                dialog.geometry("300x100")
                dialog.transient(self.parent)
                dialog.grab_set()
                
                ttk.Label(dialog, text=f"{header}:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
                var = tk.StringVar(value=str(current_value))
                entry = ttk.Entry(dialog, textvariable=var)
                entry.grid(row=0, column=1, padx=10, pady=10)
                entry.select_range(0, tk.END)
                entry.focus()
                
                def save_edit():
                    self.current_data.data[row_index][header] = var.get()
                    self.display_data()
                    dialog.destroy()
                    
                ttk.Button(dialog, text="Save", command=save_edit).grid(row=1, column=0, pady=10)
                ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=1, column=1, pady=10)
                
    def show_context_menu(self, event):
        """Show context menu"""
        selection = self.tree.selection()
        if not selection:
            return
            
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="Edit Cell", command=lambda: self.on_cell_double_click(event))
        menu.add_command(label="Delete Row", command=self.delete_row)
        menu.add_separator()
        menu.add_command(label="Copy Row", command=self.copy_row)
        
        menu.post(event.x_root, event.y_root)
        
    def copy_row(self):
        """Copy selected row to clipboard"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            row_index = self.tree.index(item)
            
            if row_index < len(self.current_data.data):
                row = self.current_data.data[row_index]
                row_text = '\t'.join(str(row.get(header, '')) for header in self.current_data.headers)
                
                self.parent.clipboard_clear()
                self.parent.clipboard_append(row_text)
                self.status_label.config(text="Row copied to clipboard")
                
    def update_status(self):
        """Update status display"""
        try:
            # Update memory usage
            memory_stats = self.memory_manager.get_memory_stats()
            self.memory_label.config(text=f"Memory: {memory_stats.memory_percent:.1f}%")
            
            # Update row count
            if self.current_data:
                self.rows_label.config(text=f"Rows: {self.current_data.row_count}")
                
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
            
        # Schedule next update
        self.parent.after(2000, self.update_status)
        
    def auto_save_timer(self):
        """Auto-save timer"""
        try:
            if (self.current_data and 
                self.current_data.file_path and 
                time.time() - self.last_save_time > self.config.auto_save_interval):
                
                self.save_to_file(self.current_data.file_path)
                self.status_label.config(text="Auto-saved")
                
        except Exception as e:
            self.logger.error(f"Auto-save error: {e}")
            
        # Schedule next check
        self.parent.after(60000, self.auto_save_timer)  # Check every minute
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import logging
from pathlib import Path

from utils.memory_manager import get_memory_manager
from utils.cache_manager import get_cache_manager
from utils.error_handler import get_error_handler
from utils.zip_processor import get_zip_processor
from utils.streaming_processor import get_streaming_processor

@dataclass
class DownloadTask:
    task_id: str
    source_path: str
    destination_path: str
    file_size: int
    progress: float = 0.0
    status: str = "pending"  # pending, downloading, completed, failed, cancelled
    start_time: float = None
    end_time: float = None
    error_message: str = ""
    speed: float = 0.0  # bytes per second

class DownloadUI:
    """Enhanced download management UI"""
    
    def __init__(self, parent):
        self.parent = parent
        self.logger = logging.getLogger(__name__)
        
        # Managers
        self.memory_manager = get_memory_manager()
        self.cache_manager = get_cache_manager()
        self.error_handler = get_error_handler()
        self.zip_processor = get_zip_processor()
        self.streaming_processor = get_streaming_processor()
        
        # Download tasks
        self.download_tasks: Dict[str, DownloadTask] = {}
        self.active_downloads: Dict[str, threading.Thread] = {}
        
        # UI components
        self.setup_ui()
        
        # Start update timer
        self.update_display()
        
    def setup_ui(self):
        """Setup download UI components"""
        # Main frame
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Download Manager", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="Add Download", 
                  command=self.add_download_dialog).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Create ZIP", 
                  command=self.create_zip_dialog).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Clear Completed", 
                  command=self.clear_completed).grid(row=0, column=2, padx=5)
        
        # Downloads list
        list_frame = ttk.LabelFrame(main_frame, text="Active Downloads", padding="5")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview for downloads
        columns = ('File', 'Size', 'Progress', 'Speed', 'Status', 'Time')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=10)
        
        # Configure columns
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Progress details frame
        details_frame = ttk.LabelFrame(main_frame, text="Download Details", padding="5")
        details_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.details_text = tk.Text(details_frame, height=6, width=70)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, 
                                        command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="5")
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.stats_label = ttk.Label(stats_frame, text="Calculating...")
        self.stats_label.grid(row=0, column=0)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_changed)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
    def add_download_dialog(self):
        """Show add download dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Download")
        dialog.geometry("500x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Source file
        ttk.Label(dialog, text="Source File:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        source_var = tk.StringVar()
        source_entry = ttk.Entry(dialog, textvariable=source_var, width=50)
        source_entry.grid(row=0, column=1, padx=10, pady=5)
        
        def browse_source():
            filename = filedialog.askopenfilename(
                title="Select Source File",
                filetypes=[("All Files", "*.*")]
            )
            if filename:
                source_var.set(filename)
                
        ttk.Button(dialog, text="Browse", command=browse_source).grid(row=0, column=2, padx=5, pady=5)
        
        # Destination
        ttk.Label(dialog, text="Destination:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        dest_var = tk.StringVar()
        dest_entry = ttk.Entry(dialog, textvariable=dest_var, width=50)
        dest_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def browse_dest():
            filename = filedialog.asksaveasfilename(
                title="Select Destination",
                filetypes=[("All Files", "*.*")]
            )
            if filename:
                dest_var.set(filename)
                
        ttk.Button(dialog, text="Browse", command=browse_dest).grid(row=1, column=2, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        def add_download():
            source = source_var.get().strip()
            dest = dest_var.get().strip()
            
            if not source or not dest:
                messagebox.showerror("Error", "Please select both source and destination")
                return
                
            if not Path(source).exists():
                messagebox.showerror("Error", "Source file does not exist")
                return
                
            self.add_download(source, dest)
            dialog.destroy()
            
        ttk.Button(button_frame, text="Add", command=add_download).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).grid(row=0, column=1, padx=5)
        
    def add_download(self, source_path: str, destination_path: str):
        """Add a new download task"""
        task_id = f"dl_{int(time.time() * 1000)}"
        
        try:
            file_size = Path(source_path).stat().st_size
            
            task = DownloadTask(
                task_id=task_id,
                source_path=source_path,
                destination_path=destination_path,
                file_size=file_size
            )
            
            self.download_tasks[task_id] = task
            
            # Start download thread
            thread = threading.Thread(target=self.download_worker, args=(task_id,), daemon=True)
            self.active_downloads[task_id] = thread
            thread.start()
            
            self.logger.info(f"Download added: {task_id} - {Path(source_path).name}")
            
        except Exception as e:
            self.logger.error(f"Error adding download: {e}")
            messagebox.showerror("Error", f"Failed to add download: {e}")
            
    def download_worker(self, task_id: str):
        """Download worker thread"""
        task = self.download_tasks[task_id]
        task.status = "downloading"
        task.start_time = time.time()
        
        try:
            def progress_callback(bytes_processed: int, total_bytes: int):
                task.progress = (bytes_processed / total_bytes) * 100
                task.speed = bytes_processed / (time.time() - task.start_time)
                
            # Use streaming processor for download
            result = self.streaming_processor.stream_with_progress(
                task.source_path,
                task.destination_path,
                progress_callback
            )
            
            if result['status'] == 'completed':
                task.status = "completed"
                task.progress = 100.0
            else:
                task.status = "failed"
                task.error_message = result.get('error', 'Unknown error')
                
        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            self.logger.error(f"Download failed: {task_id} - {e}")
            
        finally:
            task.end_time = time.time()
            if task_id in self.active_downloads:
                del self.active_downloads[task_id]
                
    def create_zip_dialog(self):
        """Show create ZIP dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Create ZIP Package")
        dialog.geometry("600x400")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # File selection
        ttk.Label(dialog, text="Select Files:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        # File listbox
        list_frame = ttk.Frame(dialog)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        file_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, height=10)
        file_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
        file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        file_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Browse button
        def add_files():
            files = filedialog.askopenfilenames(
                title="Select Files to ZIP",
                filetypes=[("All Files", "*.*")]
            )
            for file in files:
                file_listbox.insert(tk.END, file)
                
        ttk.Button(dialog, text="Add Files", command=add_files).grid(row=2, column=0, padx=10, pady=5)
        
        # Output path
        ttk.Label(dialog, text="Output ZIP:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        zip_var = tk.StringVar()
        zip_entry = ttk.Entry(dialog, textvariable=zip_var, width=50)
        zip_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def browse_zip():
            filename = filedialog.asksaveasfilename(
                title="Save ZIP As",
                defaultextension=".zip",
                filetypes=[("ZIP Files", "*.zip")]
            )
            if filename:
                zip_var.set(filename)
                
        ttk.Button(dialog, text="Browse", command=browse_zip).grid(row=3, column=2, padx=5, pady=5)
        
        # Create button
        def create_zip():
            selected_files = [file_listbox.get(i) for i in file_listbox.curselection()]
            output_path = zip_var.get().strip()
            
            if not selected_files:
                messagebox.showerror("Error", "Please select files to ZIP")
                return
                
            if not output_path:
                messagebox.showerror("Error", "Please specify output ZIP file")
                return
                
            self.create_zip_package(selected_files, output_path)
            dialog.destroy()
            
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Create ZIP", command=create_zip).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).grid(row=0, column=1, padx=5)
        
        # Configure grid weights
        dialog.columnconfigure(1, weight=1)
        dialog.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
    def create_zip_package(self, files: List[str], output_path: str):
        """Create ZIP package"""
        task_id = f"zip_{int(time.time() * 1000)}"
        
        try:
            # Add to treeview
            self.tree.insert('', 'end', iid=task_id, text=task_id,
                           values=(Path(output_path).name, "Calculating...", "0%", "0 B/s", "Creating ZIP", ""))
            
            # Create ZIP in background thread
            thread = threading.Thread(target=self.zip_worker, args=(task_id, files, output_path), daemon=True)
            thread.start()
            
        except Exception as e:
            self.logger.error(f"Error creating ZIP: {e}")
            messagebox.showerror("Error", f"Failed to create ZIP: {e}")
            
    def zip_worker(self, task_id: str, files: List[str], output_path: str):
        """ZIP creation worker thread"""
        try:
            # Use zip processor to create ZIP
            result = self.zip_processor.create_zip(files, output_path, task_id)
            
            # Update UI
            self.parent.after(0, self.update_zip_result, task_id, result)
            
        except Exception as e:
            self.logger.error(f"ZIP creation failed: {e}")
            self.parent.after(0, self.update_zip_error, task_id, str(e))
            
    def update_zip_result(self, task_id: str, result: Dict[str, Any]):
        """Update ZIP creation result"""
        if result['status'] == 'completed':
            # Update treeview
            self.tree.item(task_id, values=(
                Path(result['output_path']).name,
                f"{result['total_size']:,} bytes",
                "100%",
                "Completed",
                "Completed",
                f"{result['duration']:.2f}s"
            ))
            
            messagebox.showinfo("Success", f"ZIP created successfully:\n{result['output_path']}")
        else:
            self.tree.item(task_id, values=(
                Path(result.get('output_path', 'unknown')).name,
                "Error",
                "0%",
                "Failed",
                "Failed",
                ""
            ))
            
    def update_zip_error(self, task_id: str, error_message: str):
        """Update ZIP error"""
        self.tree.item(task_id, values=(
            "Error",
            "Error",
            "0%",
            "Failed",
            f"Error: {error_message}",
            ""
        ))
        
    def on_selection_changed(self, event):
        """Handle treeview selection change"""
        selection = self.tree.selection()
        if selection:
            task_id = selection[0]
            if task_id in self.download_tasks:
                task = self.download_tasks[task_id]
                self.update_details_display(task)
                
    def update_details_display(self, task: DownloadTask):
        """Update details display"""
        self.details_text.delete(1.0, tk.END)
        
        details = f"""Task ID: {task.task_id}
Source: {task.source_path}
Destination: {task.destination_path}
File Size: {task.file_size:,} bytes
Progress: {task.progress:.1f}%
Status: {task.status}
Speed: {task.speed:,.0f} bytes/sec
"""
        
        if task.start_time:
            details += f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(task.start_time))}\n"
            
        if task.end_time:
            details += f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(task.end_time))}\n"
            details += f"Duration: {task.end_time - task.start_time:.2f} seconds\n"
            
        if task.error_message:
            details += f"Error: {task.error_message}\n"
            
        self.details_text.insert(1.0, details)
        
    def show_context_menu(self, event):
        """Show context menu"""
        item = self.tree.identify('item', event.x, event.y)
        if not item:
            return
            
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="Cancel", command=lambda: self.cancel_download(item))
        menu.add_command(label="Retry", command=lambda: self.retry_download(item))
        menu.add_separator()
        menu.add_command(label="Remove", command=lambda: self.remove_download(item))
        
        menu.post(event.x_root, event.y_root)
        
    def cancel_download(self, task_id: str):
        """Cancel download"""
        if task_id in self.download_tasks:
            task = self.download_tasks[task_id]
            if task.status == "downloading":
                task.status = "cancelled"
                task.end_time = time.time()
                
            if task_id in self.active_downloads:
                # Note: Actual thread cancellation would need proper implementation
                del self.active_downloads[task_id]
                
    def retry_download(self, task_id: str):
        """Retry download"""
        if task_id in self.download_tasks:
            task = self.download_tasks[task_id]
            if task.status in ["failed", "cancelled"]:
                # Reset task and restart
                task.status = "pending"
                task.progress = 0.0
                task.error_message = ""
                
                thread = threading.Thread(target=self.download_worker, args=(task_id,), daemon=True)
                self.active_downloads[task_id] = thread
                thread.start()
                
    def remove_download(self, task_id: str):
        """Remove download from list"""
        if task_id in self.download_tasks:
            task = self.download_tasks[task_id]
            if task.status in ["completed", "failed", "cancelled"]:
                del self.download_tasks[task_id]
                self.tree.delete(task_id)
                
    def clear_completed(self):
        """Clear completed downloads"""
        to_remove = []
        for task_id, task in self.download_tasks.items():
            if task.status in ["completed", "failed", "cancelled"]:
                to_remove.append(task_id)
                
        for task_id in to_remove:
            del self.download_tasks[task_id]
            self.tree.delete(task_id)
            
    def update_display(self):
        """Update display periodically"""
        try:
            # Update treeview
            for task_id, task in self.download_tasks.items():
                if task_id in self.tree.get_children():
                    # Update existing item
                    self.tree.item(task_id, values=(
                        Path(task.source_path).name,
                        f"{task.file_size:,} bytes",
                        f"{task.progress:.1f}%",
                        f"{task.speed:,.0f} B/s",
                        task.status,
                        f"{time.time() - task.start_time:.1f}s" if task.start_time else ""
                    ))
                else:
                    # Add new item
                    self.tree.insert('', 'end', iid=task_id, text=task_id,
                                   values=(
                                       Path(task.source_path).name,
                                       f"{task.file_size:,} bytes",
                                       f"{task.progress:.1f}%",
                                       f"{task.speed:,.0f} B/s",
                                       task.status,
                                       ""
                                   ))
                    
            # Update statistics
            self.update_statistics()
            
        except Exception as e:
            self.logger.error(f"Error updating display: {e}")
            
        # Schedule next update
        self.parent.after(1000, self.update_display)
        
    def update_statistics(self):
        """Update statistics display"""
        total_tasks = len(self.download_tasks)
        active_tasks = sum(1 for task in self.download_tasks.values() 
                          if task.status == "downloading")
        completed_tasks = sum(1 for task in self.download_tasks.values() 
                             if task.status == "completed")
        failed_tasks = sum(1 for task in self.download_tasks.values() 
                          if task.status == "failed")
        
        stats_text = f"Total: {total_tasks} | Active: {active_tasks} | Completed: {completed_tasks} | Failed: {failed_tasks}"
        self.stats_label.config(text=stats_text)
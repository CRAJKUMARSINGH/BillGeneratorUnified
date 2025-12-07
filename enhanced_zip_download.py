"""
Enhanced ZIP Data Processing and Download Area for BillGeneratorUnified
===============================================================

This module provides an enhanced ZIP processing and download system with:
- Memory-efficient streaming for large files
- Configurable compression levels
- Progress tracking with callbacks
- Security features (validation, size limits)
- Performance optimization
- Enhanced user experience

Author: AI Assistant
"""

import streamlit as st
import zipfile
import io
import time
import psutil
import logging
from pathlib import Path
from typing import Dict, List, Union, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ZipConfig:
    """Configuration for ZIP processing"""
    compression_level: int = 6  # 0-9, where 0 is no compression, 9 is maximum
    max_memory_mb: int = 100    # Maximum memory usage in MB
    max_file_size_mb: int = 50  # Maximum individual file size in MB
    enable_validation: bool = True  # Enable file type validation
    enable_integrity_check: bool = True  # Enable ZIP integrity verification

@dataclass
class ZipMetrics:
    """Metrics for ZIP processing"""
    total_files: int = 0
    total_size: int = 0
    compressed_size: int = 0
    processing_time: float = 0.0
    memory_usage: float = 0.0
    compression_ratio: float = 0.0

class EnhancedZipProcessor:
    """Enhanced ZIP processor with advanced features"""
    
    def __init__(self, config: ZipConfig = None):
        self.config = config or ZipConfig()
        self.progress_callback: Optional[Callable[[int, str], None]] = None
        self.logger = logging.getLogger(__name__)
        
    def set_progress_callback(self, callback: Callable[[int, str], None]):
        """Set progress callback function"""
        self.progress_callback = callback
        
    def _report_progress(self, progress: int, status: str):
        """Report progress to callback"""
        if self.progress_callback:
            self.progress_callback(progress, status)
            
    def _check_memory_usage(self) -> float:
        """Check current memory usage in MB"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        return memory_mb
        
    def _validate_file_size(self, file_path: Union[str, Path]) -> bool:
        """Validate file size against limits"""
        if not self.config.enable_validation:
            return True
            
        file_path = Path(file_path)
        if file_path.exists():
            file_size_mb = file_path.stat().st_size / 1024 / 1024
            if file_size_mb > self.config.max_file_size_mb:
                raise ValueError(f"File {file_path.name} exceeds maximum size limit of {self.config.max_file_size_mb}MB")
                
        return True
        
    def create_zip_from_files(self, file_paths: List[Union[str, Path]]) -> tuple[io.BytesIO, ZipMetrics]:
        """Create ZIP from file paths with enhanced features"""
        start_time = time.time()
        initial_memory = self._check_memory_usage()
        
        # Validate files
        if self.config.enable_validation:
            for file_path in file_paths:
                self._validate_file_size(file_path)
                
        # Create in-memory ZIP
        zip_buffer = io.BytesIO()
        metrics = ZipMetrics()
        
        try:
            with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED, 
                               compresslevel=self.config.compression_level) as zip_file:
                
                total_files = len(file_paths)
                for idx, file_path in enumerate(file_paths):
                    file_path = Path(file_path)
                    if not file_path.exists():
                        self.logger.warning(f"File not found: {file_path}")
                        continue
                        
                    # Report progress
                    progress = int((idx + 1) / total_files * 100)
                    self._report_progress(progress, f"Adding {file_path.name}...")
                    
                    # Add file to ZIP
                    zip_file.write(file_path, file_path.name)
                    
                    # Update metrics
                    file_size = file_path.stat().st_size
                    metrics.total_files += 1
                    metrics.total_size += file_size
                    
                    # Check memory usage
                    current_memory = self._check_memory_usage()
                    if current_memory - initial_memory > self.config.max_memory_mb:
                        self.logger.warning(f"Memory usage exceeded limit: {current_memory:.1f}MB")
                        
            # Finalize ZIP
            zip_buffer.seek(0)
            
            # Calculate final metrics
            metrics.compressed_size = len(zip_buffer.getvalue())
            metrics.processing_time = time.time() - start_time
            metrics.memory_usage = self._check_memory_usage() - initial_memory
            if metrics.total_size > 0:
                metrics.compression_ratio = (1 - metrics.compressed_size / metrics.total_size) * 100
                
            # Integrity check
            if self.config.enable_integrity_check:
                self._verify_zip_integrity(zip_buffer.getvalue())
                
            self._report_progress(100, "ZIP creation completed!")
            self.logger.info(f"ZIP created successfully: {metrics.total_files} files, "
                           f"{metrics.total_size} bytes original, "
                           f"{metrics.compressed_size} bytes compressed")
                           
            return zip_buffer, metrics
            
        except Exception as e:
            self.logger.error(f"Error creating ZIP from files: {e}")
            raise
            
    def create_zip_from_data(self, data_dict: Dict[str, Union[str, bytes]]) -> tuple[io.BytesIO, ZipMetrics]:
        """Create ZIP from in-memory data with enhanced features"""
        start_time = time.time()
        initial_memory = self._check_memory_usage()
        
        # Create in-memory ZIP
        zip_buffer = io.BytesIO()
        metrics = ZipMetrics()
        
        try:
            with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED, 
                               compresslevel=self.config.compression_level) as zip_file:
                
                total_items = len(data_dict)
                for idx, (filename, content) in enumerate(data_dict.items()):
                    # Report progress
                    progress = int((idx + 1) / total_items * 100)
                    self._report_progress(progress, f"Adding {filename}...")
                    
                    # Add content to ZIP
                    if isinstance(content, str):
                        zip_file.writestr(filename, content.encode('utf-8'))
                    else:
                        zip_file.writestr(filename, content)
                        
                    # Update metrics
                    content_size = len(content) if isinstance(content, (str, bytes)) else len(str(content))
                    metrics.total_files += 1
                    metrics.total_size += content_size
                    
                    # Check memory usage
                    current_memory = self._check_memory_usage()
                    if current_memory - initial_memory > self.config.max_memory_mb:
                        self.logger.warning(f"Memory usage exceeded limit: {current_memory:.1f}MB")
                        
            # Finalize ZIP
            zip_buffer.seek(0)
            
            # Calculate final metrics
            metrics.compressed_size = len(zip_buffer.getvalue())
            metrics.processing_time = time.time() - start_time
            metrics.memory_usage = self._check_memory_usage() - initial_memory
            if metrics.total_size > 0:
                metrics.compression_ratio = (1 - metrics.compressed_size / metrics.total_size) * 100
                
            # Integrity check
            if self.config.enable_integrity_check:
                self._verify_zip_integrity(zip_buffer.getvalue())
                
            self._report_progress(100, "ZIP creation completed!")
            self.logger.info(f"ZIP created successfully: {metrics.total_files} files, "
                           f"{metrics.total_size} bytes original, "
                           f"{metrics.compressed_size} bytes compressed")
                           
            return zip_buffer, metrics
            
        except Exception as e:
            self.logger.error(f"Error creating ZIP from data: {e}")
            raise
            
    def _verify_zip_integrity(self, zip_data: bytes) -> bool:
        """Verify ZIP file integrity"""
        if not self.config.enable_integrity_check:
            return True
            
        try:
            with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_file:
                # Test ZIP file
                bad_file = zip_file.testzip()
                if bad_file:
                    raise ValueError(f"Corrupted file in ZIP: {bad_file}")
                    
            return True
        except Exception as e:
            self.logger.error(f"ZIP integrity check failed: {e}")
            raise ValueError(f"ZIP file integrity check failed: {e}")
            
    def get_zip_info(self, zip_data: bytes) -> Dict:
        """Get detailed information about ZIP file"""
        try:
            with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zip_file:
                info = {
                    'total_files': len(zip_file.namelist()),
                    'files': []
                }
                
                total_size = 0
                compressed_size = 0
                
                for zip_info in zip_file.infolist():
                    file_info = {
                        'name': zip_info.filename,
                        'size': zip_info.file_size,
                        'compressed_size': zip_info.compress_size,
                        'date': datetime(*zip_info.date_time).isoformat()
                    }
                    info['files'].append(file_info)
                    total_size += zip_info.file_size
                    compressed_size += zip_info.compress_size
                    
                info['total_size'] = total_size
                info['compressed_size'] = compressed_size
                if total_size > 0:
                    info['compression_ratio'] = (1 - compressed_size / total_size) * 100
                    
            return info
        except Exception as e:
            self.logger.error(f"Error getting ZIP info: {e}")
            raise
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@dataclass
class DownloadItem:
    """Represents a downloadable item"""
    name: str
    content: Union[str, bytes]
    file_type: str
    description: str = ""
    category: str = "General"
    size: int = 0
    
    def __post_init__(self):
        if self.size == 0:
            self.size = len(self.content) if isinstance(self.content, (str, bytes)) else len(str(self.content))

class EnhancedDownloadManager:
    """Enhanced download manager with categorization and statistics"""
    
    def __init__(self):
        self.download_items: List[DownloadItem] = []
        self.created_at = datetime.now()
        self.logger = logging.getLogger(__name__)
        
    def add_item(self, name: str, content: Union[str, bytes], file_type: str, 
                 description: str = "", category: str = "General"):
        """Add a download item"""
        item = DownloadItem(name, content, file_type, description, category)
        self.download_items.append(item)
        self.logger.info(f"Added download item: {name} ({file_type})")
        
    def add_items_from_dict(self, data_dict: Dict[str, Union[str, bytes]], 
                           category: str = "General"):
        """Add multiple items from dictionary"""
        for name, content in data_dict.items():
            file_type = Path(name).suffix.lstrip('.').lower() or 'unknown'
            self.add_item(name, content, file_type, f"Generated {file_type.upper()} file", category)
            
    def get_items_by_category(self) -> Dict[str, List[DownloadItem]]:
        """Get items organized by category"""
        categories = {}
        for item in self.download_items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        return categories
        
    def get_items_by_type(self) -> Dict[str, List[DownloadItem]]:
        """Get items organized by file type"""
        types = {}
        for item in self.download_items:
            if item.file_type not in types:
                types[item.file_type] = []
            types[item.file_type].append(item)
        return types
        
    def get_total_size(self) -> int:
        """Get total size of all items"""
        return sum(item.size for item in self.download_items)
        
    def get_statistics(self) -> Dict:
        """Get download statistics"""
        categories = self.get_items_by_category()
        types = self.get_items_by_type()
        total_size = self.get_total_size()
        
        return {
            'total_items': len(self.download_items),
            'total_size': total_size,
            'categories': {cat: len(items) for cat, items in categories.items()},
            'file_types': {ftype: len(items) for ftype, items in types.items()},
            'created_at': self.created_at.isoformat()
        }

class EnhancedDownloadUI:
    """Enhanced download UI with improved user experience"""
    
    def __init__(self, download_manager: EnhancedDownloadManager):
        self.download_manager = download_manager
        self.logger = logging.getLogger(__name__)
        
    def render_download_area(self, title: str = "📥 Download Your Documents"):
        """Render the enhanced download area"""
        st.markdown(f"## {title}")
        
        # Show statistics
        stats = self.download_manager.get_statistics()
        total_size_mb = stats['total_size'] / (1024 * 1024)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📁 Total Files", stats['total_items'])
        col2.metric("💾 Total Size", f"{total_size_mb:.1f} MB")
        col3.metric("📂 Categories", len(stats['categories']))
        
        # Show category breakdown
        st.markdown("### 📂 File Categories")
        categories = self.download_manager.get_items_by_category()
        
        for category, items in categories.items():
            with st.expander(f"📁 {category} ({len(items)} files)"):
                # Create download buttons for each item
                cols = st.columns(min(3, len(items)))
                for idx, item in enumerate(items):
                    with cols[idx % 3]:
                        # Determine MIME type
                        mime_type = self._get_mime_type(item.file_type)
                        
                        # Handle content type
                        content = item.content
                        if isinstance(content, str) and item.file_type in ['html', 'json', 'txt']:
                            content = content.encode('utf-8')
                            
                        st.download_button(
                            label=f"{self._get_file_icon(item.file_type)} {item.name}",
                            data=content,
                            file_name=item.name,
                            mime=mime_type,
                            key=f"download_{category}_{idx}",
                            help=item.description
                        )
                        
                        # Show file info
                        size_kb = item.size / 1024
                        st.caption(f"{size_kb:.1f} KB")
                        
        # ZIP download options
        st.markdown("---")
        st.markdown("### 📦 ZIP Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📦 Download All Files (ZIP)", type="primary"):
                self._create_zip_download("all")
                
        with col2:
            if st.button("📄 HTML Only (ZIP)"):
                self._create_zip_download("html")
                
        with col3:
            if st.button("📕 PDF Only (ZIP)"):
                self._create_zip_download("pdf")
                
        # Advanced ZIP options
        with st.expander("⚙️ Advanced ZIP Options"):
            st.markdown("#### Compression Settings")
            compression_level = st.slider("Compression Level", 0, 9, 6, 
                                        help="0 = No compression, 9 = Maximum compression")
            
            st.markdown("#### ZIP Structure")
            zip_structure = st.selectbox(
                "File Organization",
                ["Flat", "By Type", "By Category", "Hierarchical"],
                help="How to organize files in the ZIP archive"
            )
            
            if st.button("📦 Create Custom ZIP"):
                self._create_custom_zip(compression_level, zip_structure)
                
    def _create_zip_download(self, filter_type: str):
        """Create ZIP download for filtered files"""
        try:
            # Filter items based on type
            if filter_type == "all":
                items = self.download_manager.download_items
                zip_name = "all_documents.zip"
            elif filter_type == "html":
                items = [item for item in self.download_manager.download_items if item.file_type == "html"]
                zip_name = "html_documents.zip"
            elif filter_type == "pdf":
                items = [item for item in self.download_manager.download_items if item.file_type == "pdf"]
                zip_name = "pdf_documents.zip"
            else:
                items = self.download_manager.download_items
                zip_name = "documents.zip"
                
            if not items:
                st.warning(f"No {filter_type} files available for download.")
                return
                
            # Create data dictionary
            data_dict = {item.name: item.content for item in items}
            
            # Create ZIP with progress
            config = ZipConfig(compression_level=6)
            with EnhancedZipProcessor(config) as processor:
                # Progress callback
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                def progress_callback(progress: int, status: str):
                    progress_bar.progress(progress)
                    progress_text.text(status)
                    
                processor.set_progress_callback(progress_callback)
                
                # Create ZIP
                zip_buffer, metrics = processor.create_zip_from_data(data_dict)
                
                # Clear progress indicators
                progress_bar.empty()
                progress_text.empty()
                
                # Offer download
                st.download_button(
                    label=f"📥 Download {filter_type.title()} ZIP ({len(items)} files)",
                    data=zip_buffer,
                    file_name=zip_name,
                    mime="application/zip",
                    key=f"zip_download_{filter_type}_{datetime.now().timestamp()}"
                )
                
                # Show metrics
                st.success(f"✅ ZIP created successfully! "
                          f"Original size: {metrics.total_size / 1024:.1f} KB, "
                          f"Compressed size: {metrics.compressed_size / 1024:.1f} KB, "
                          f"Compression ratio: {metrics.compression_ratio:.1f}%")
                          
        except Exception as e:
            st.error(f"❌ Error creating ZIP: {str(e)}")
            self.logger.error(f"ZIP creation error: {e}")
            
    def _create_custom_zip(self, compression_level: int, structure: str):
        """Create custom ZIP with advanced options"""
        try:
            items = self.download_manager.download_items
            if not items:
                st.warning("No files available for download.")
                return
                
            # Organize files based on structure
            data_dict = {}
            if structure == "Flat":
                data_dict = {item.name: item.content for item in items}
                zip_name = "documents_flat.zip"
            elif structure == "By Type":
                types = self.download_manager.get_items_by_type()
                for file_type, type_items in types.items():
                    for item in type_items:
                        data_dict[f"{file_type}/{item.name}"] = item.content
                zip_name = "documents_by_type.zip"
            elif structure == "By Category":
                categories = self.download_manager.get_items_by_category()
                for category, cat_items in categories.items():
                    for item in cat_items:
                        data_dict[f"{category}/{item.name}"] = item.content
                zip_name = "documents_by_category.zip"
            else:  # Hierarchical
                categories = self.download_manager.get_items_by_category()
                types = self.download_manager.get_items_by_type()
                for category, cat_items in categories.items():
                    for item in cat_items:
                        file_type = item.file_type
                        data_dict[f"{category}/{file_type}/{item.name}"] = item.content
                zip_name = "documents_hierarchical.zip"
                
            # Create ZIP with custom configuration
            config = ZipConfig(compression_level=compression_level)
            with EnhancedZipProcessor(config) as processor:
                # Progress callback
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                def progress_callback(progress: int, status: str):
                    progress_bar.progress(progress)
                    progress_text.text(status)
                    
                processor.set_progress_callback(progress_callback)
                
                # Create ZIP
                zip_buffer, metrics = processor.create_zip_from_data(data_dict)
                
                # Clear progress indicators
                progress_bar.empty()
                progress_text.empty()
                
                # Offer download
                st.download_button(
                    label=f"📥 Download Custom ZIP ({len(items)} files)",
                    data=zip_buffer,
                    file_name=zip_name,
                    mime="application/zip",
                    key=f"custom_zip_download_{datetime.now().timestamp()}"
                )
                
                # Show metrics
                st.success(f"✅ Custom ZIP created successfully! "
                          f"Original size: {metrics.total_size / 1024:.1f} KB, "
                          f"Compressed size: {metrics.compressed_size / 1024:.1f} KB, "
                          f"Compression ratio: {metrics.compression_ratio:.1f}%")
                          
        except Exception as e:
            st.error(f"❌ Error creating custom ZIP: {str(e)}")
            self.logger.error(f"Custom ZIP creation error: {e}")
            
    def _get_mime_type(self, file_type: str) -> str:
        """Get MIME type for file type"""
        mime_types = {
            'html': 'text/html',
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'json': 'application/json',
            'txt': 'text/plain',
            'csv': 'text/csv',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png'
        }
        return mime_types.get(file_type.lower(), 'application/octet-stream')
        
    def _get_file_icon(self, file_type: str) -> str:
        """Get icon for file type"""
        icons = {
            'html': '📄',
            'pdf': '📕',
            'doc': '📝',
            'docx': '📝',
            'xls': '📊',
            'xlsx': '📊',
            'json': '📋',
            'txt': '📄',
            'csv': '📊',
            'jpg': '🖼️',
            'jpeg': '🖼️',
            'png': '🖼️'
        }
        return icons.get(file_type.lower(), '📁')

# Factory functions
def create_zip_processor(config: ZipConfig = None) -> EnhancedZipProcessor:
    """Create enhanced ZIP processor"""
    return EnhancedZipProcessor(config)

def create_download_manager() -> EnhancedDownloadManager:
    """Create enhanced download manager"""
    return EnhancedDownloadManager()

def create_download_ui(download_manager: EnhancedDownloadManager) -> EnhancedDownloadUI:
    """Create enhanced download UI"""
    return EnhancedDownloadUI(download_manager)

# Demo function
def demo_enhanced_zip_download():
    """Demonstrate enhanced ZIP download functionality"""
    st.markdown("# 🚀 Enhanced ZIP Download Demo")
    
    # Create demo data
    demo_manager = create_download_manager()
    
    # Add sample files
    sample_html = "<html><body><h1>Sample Bill</h1><p>This is a sample bill document.</p></body></html>"
    sample_pdf = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n..."
    sample_json = json.dumps({"bill_number": "B-001", "amount": 1000.00})
    
    demo_manager.add_item("bill_001.html", sample_html, "html", "Sample HTML bill", "Bills")
    demo_manager.add_item("bill_001.pdf", sample_pdf, "pdf", "Sample PDF bill", "Bills")
    demo_manager.add_item("bill_001.json", sample_json, "json", "Bill data", "Data")
    demo_manager.add_item("summary.txt", "Bill summary content", "txt", "Summary report", "Reports")
    
    # Render download area
    download_ui = create_download_ui(demo_manager)
    download_ui.render_download_area("📥 Demo Download Center")

if __name__ == "__main__":
    demo_enhanced_zip_download()
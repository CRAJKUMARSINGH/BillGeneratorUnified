"""
Enhanced Download UI for BillGeneratorUnified
Provides improved user interface for downloading files with organization and progress tracking
"""

import streamlit as st
from typing import Callable, Optional
import io
from core.utils.download_manager import EnhancedDownloadManager, DownloadCategory, FileType

# Defensive import for ZIP processor to avoid circular import issues
try:
    from core.utils.enhanced_zip_processor import EnhancedZipProcessor, ZipConfig, create_zip_from_dict
except ImportError:
    # Fallback import structure
    EnhancedZipProcessor = None
    ZipConfig = None
    create_zip_from_dict = None
class EnhancedDownloadUI:
    """Enhanced UI for downloading files with better organization and user experience"""
    
    def __init__(self, download_manager: EnhancedDownloadManager):
        self.download_manager = download_manager
        
    def render_download_area(self, title: str = "📥 Download Documents"):
        """Render the enhanced download area"""
        st.markdown(f"### {title}")
        
        # Show statistics
        stats = self.download_manager.get_statistics()
        if stats['total_items'] > 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Files", stats['total_items'])
            with col2:
                st.metric("Total Size", f"{stats['total_size_mb']} MB")
            with col3:
                st.metric("Categories", len(stats['categories']))
        
        # Get categorized items
        categorized_items = self.download_manager.get_items_by_category()
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📁 By Category", "📦 ZIP Downloads", "📊 Statistics"])
        
        with tab1:
            self._render_category_view(categorized_items)
            
        with tab2:
            self._render_zip_downloads()
            
        with tab3:
            self._render_statistics(stats, categorized_items)
            
    def _render_category_view(self, categorized_items: dict):
        """Render downloads organized by category"""
        if not categorized_items:
            st.info("No download items available.")
            return
            
        for category, items in categorized_items.items():
            if items:
                with st.expander(f"{category.value} ({len(items)} files)", expanded=False):
                    cols = st.columns(min(3, len(items)))
                    for idx, item in enumerate(items):
                        with cols[idx % 3]:
                            # File icon based on type
                            icon = "📄"
                            if item.file_type == FileType.PDF:
                                icon = "📕"
                            elif item.file_type == FileType.DOC:
                                icon = "📘"
                            elif item.file_type == FileType.XLSX:
                                icon = "📊"
                                
                            st.markdown(f"**{icon} {item.name}**")
                            if item.description:
                                st.caption(item.description)
                            st.caption(f"Size: {item.size_bytes / 1024:.1f} KB")
                            
                            # Download button
                            st.download_button(
                                label="Download",
                                data=item.content,
                                file_name=item.name,
                                mime=item.file_type.value,
                                key=f"download_{item.name}_{idx}"
                            )
                            
    def _render_zip_downloads(self):
        """Render ZIP download options"""
        st.markdown("#### 📦 Create Custom ZIP Archives")
        
        # Display any pending download buttons from session state
        zip_keys = [key for key in st.session_state.keys() if key.startswith(("enhanced_zip_data_", "categorized_zip_data_"))]
        if zip_keys:
            st.markdown("#### 📥 Available ZIP Downloads")
            for key in zip_keys:
                zip_info = st.session_state[key]
                st.download_button(
                    label=zip_info["label"],
                    data=zip_info["data"],
                    file_name=zip_info["filename"],
                    mime=zip_info["mime"],
                    key=key
                )
            st.markdown("---")
        
        # ZIP configuration options
        col1, col2, col3 = st.columns(3)
        with col1:
            compression_level = st.slider("Compression Level", 0, 9, 6)
        with col2:
            include_structure = st.checkbox("Preserve Directory Structure", True)
        with col3:
            integrity_check = st.checkbox("Verify Integrity", True)
            
        # ZIP creation options
        st.markdown("##### Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📦 Download All Files"):
                self._create_and_download_zip(
                    "all_documents.zip",
                    compression_level=compression_level,
                    preserve_structure=include_structure,
                    integrity_check=integrity_check
                )
                
        with col2:
            if st.button("📄 HTML Documents Only"):
                self._create_and_download_zip(
                    "html_documents.zip",
                    compression_level=compression_level,
                    file_type=FileType.HTML,
                    preserve_structure=include_structure
                )
                
        with col3:
            if st.button("📕 PDF Documents Only"):
                self._create_and_download_zip(
                    "pdf_documents.zip",
                    compression_level=compression_level,
                    file_type=FileType.PDF,
                    preserve_structure=include_structure
                )
                
        # Additional format options
        col4, col5, col6 = st.columns(3)
        
        with col4:
            if st.button("📘 DOC Documents Only"):
                self._create_and_download_zip(
                    "doc_documents.zip",
                    compression_level=compression_level,
                    file_type=FileType.DOC,
                    preserve_structure=include_structure
                )
                
        with col5:
            if st.button("📊 Excel Files Only"):
                self._create_and_download_zip(
                    "excel_files.zip",
                    compression_level=compression_level,
                    file_type=FileType.XLSX,
                    preserve_structure=include_structure
                )
                
        with col6:
            if st.button("🗂️ By Category Structure"):
                self._create_categorized_zip(
                    "documents_by_category.zip",
                    compression_level=compression_level
                )
                
    def _create_and_download_zip(self, filename: str, compression_level: int = 6,
                               file_type: Optional[FileType] = None,
                               preserve_structure: bool = True,
                               integrity_check: bool = True):
        """Create and download a ZIP file"""
        # Check if required imports are available
        if EnhancedZipProcessor is None or ZipConfig is None:
            st.error("ZIP processing is not available. Please check your installation.")
            return
            
        try:
            # Filter items if specific file type requested
            items = self.download_manager.get_all_items()
            if file_type:
                items = self.download_manager.get_items_by_filter(file_type=file_type)
                
            if not items:
                st.warning("No files available for ZIP creation.")
                return
                
            # Prepare data for ZIP creation
            data_dict = {}
            for item in items:
                # Create appropriate path based on settings
                if preserve_structure:
                    # Use category as folder name
                    folder_name = item.category.value.replace(" ", "_").lower()
                    archive_path = f"{folder_name}/{item.name}"
                else:
                    archive_path = item.name
                    
                data_dict[archive_path] = item.content
                
            # Configure ZIP processor
            config = ZipConfig(
                compression_level=compression_level,
                enable_integrity_check=integrity_check,
                preserve_directory_structure=preserve_structure
            )
            
            # Create ZIP with progress tracking
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            def progress_callback(progress: float, message: str):
                progress_bar.progress(int(progress))
                progress_text.text(message)
                
            with EnhancedZipProcessor(config) as processor:
                processor.set_progress_callback(progress_callback)
                
                # Add files to processor
                for path, content in data_dict.items():
                    processor.add_file_from_memory(content, path)
                    
                # Create ZIP
                zip_buffer, metrics = processor.create_zip()
                
            progress_bar.empty()
            progress_text.empty()
            
            # Show metrics
            with st.expander("ZIP Creation Metrics", expanded=False):
                st.json(metrics)
                
            # Store ZIP data in session state for download
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_key = f"enhanced_zip_data_{filename}_{timestamp}"
            
            st.session_state[zip_key] = {
                "data": zip_buffer,
                "filename": filename,
                "label": f"📥 Download {filename}",
                "mime": "application/zip"
            }
            
            st.success(f"✅ ZIP file '{filename}' created successfully! Click the download button below.")
            
        except Exception as e:
            st.error(f"Error creating ZIP: {str(e)}")
            
    def _create_categorized_zip(self, filename: str, compression_level: int = 6):
        """Create a ZIP with files organized by category"""
        # Check if required imports are available
        if create_zip_from_dict is None or ZipConfig is None:
            st.error("ZIP processing is not available. Please check your installation.")
            return
            
        try:
            categorized_items = self.download_manager.get_items_by_category()
            
            if not any(categorized_items.values()):
                st.warning("No files available for ZIP creation.")
                return
                
            # Prepare data with category structure
            data_dict = {}
            for category, items in categorized_items.items():
                if items:
                    folder_name = category.value.replace(" ", "_").lower()
                    for item in items:
                        archive_path = f"{folder_name}/{item.name}"
                        data_dict[archive_path] = item.content
                        
            # Configure ZIP processor
            config = ZipConfig(
                compression_level=compression_level,
                preserve_directory_structure=True
            )
            
            # Create ZIP
            zip_buffer, metrics = create_zip_from_dict(data_dict, config)
            
            # Store ZIP data in session state for download
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_key = f"categorized_zip_data_{filename}_{timestamp}"
            
            st.session_state[zip_key] = {
                "data": zip_buffer,
                "filename": filename,
                "label": f"📥 Download {filename}",
                "mime": "application/zip"
            }
            
            st.success(f"✅ Categorized ZIP file '{filename}' created successfully! Click the download button below.")
            
        except Exception as e:
            st.error(f"Error creating categorized ZIP: {str(e)}")
            
    def _render_statistics(self, stats: dict, categorized_items: dict):
        """Render download statistics"""
        st.markdown("#### 📊 Download Statistics")
        
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Files", stats['total_items'])
        with col2:
            st.metric("Total Size", f"{stats['total_size_mb']} MB")
        with col3:
            st.metric("Categories", len(stats['categories']))
        with col4:
            st.metric("File Types", len(stats['file_types']))
            
        # Category breakdown
        st.markdown("##### 📁 By Category")
        for category, count in stats['categories'].items():
            st.progress(count / max(1, stats['total_items']))
            st.text(f"{category}: {count} files")
            
        # File type breakdown
        st.markdown("##### 📄 By File Type")
        type_mapping = {
            "text/html": "HTML",
            "application/pdf": "PDF",
            "application/msword": "DOC",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "Excel"
        }
        
        for file_type, count in stats['file_types'].items():
            display_name = type_mapping.get(file_type, file_type)
            st.progress(count / max(1, stats['total_items']))
            st.text(f"{display_name}: {count} files")


# Utility function for easy integration
def create_download_manager() -> EnhancedDownloadManager:
    """Create and return a new download manager"""
    return EnhancedDownloadManager()
    
    
def create_enhanced_download_ui(download_manager: EnhancedDownloadManager) -> EnhancedDownloadUI:
    """Create and return an enhanced download UI"""
    return EnhancedDownloadUI(download_manager)
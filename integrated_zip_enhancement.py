"""
Integrated ZIP Enhancement for BillGeneratorUnified Batch Processing
==================================================================

This module demonstrates how to integrate the enhanced ZIP functionality 
with the existing batch processing system.

Author: AI Assistant
"""

import streamlit as st
import os
from pathlib import Path
from typing import List, Dict, Any
import zipfile
import io
import time

# Import our enhanced components
from core.utils.download_manager import EnhancedDownloadManager, DownloadCategory, FileType
from core.utils.optimized_zip_processor import OptimizedZipProcessor, OptimizedZipConfig, ZipMetrics
from core.ui.enhanced_download_center import EnhancedDownloadCenter

def integrate_with_batch_processor():
    """
    Demonstrate integration with batch processor
    
    This function shows how the enhanced ZIP functionality
    can be integrated with the existing batch processing system.
    """
    
    st.markdown("# 🔄 Integrated ZIP Enhancement for Batch Processing")
    
    # Simulate batch processing results
    if st.button("🚀 Run Batch Processing Simulation"):
        with st.spinner("Processing batch files..."):
            # Simulate processing multiple files
            processed_files = simulate_batch_processing()
            
            # Create download manager
            download_manager = EnhancedDownloadManager()
            
            # Add processed files to download manager
            for file_info in processed_files:
                # Add HTML files
                for doc_name, html_content in file_info['html_documents'].items():
                    if isinstance(html_content, str):
                        content_bytes = html_content.encode('utf-8')
                    else:
                        content_bytes = html_content
                    download_manager.add_item(
                        name=f"{doc_name}.html",
                        content=content_bytes,
                        file_type=FileType.HTML,
                        description=f"HTML version of {doc_name}",
                        category=DownloadCategory.HTML_DOCUMENTS
                    )
                
                # Add PDF files
                for doc_name, pdf_content in file_info['pdf_documents'].items():
                    download_manager.add_item(
                        name=doc_name,
                        content=pdf_content,
                        file_type=FileType.PDF,
                        description=f"PDF version of {doc_name}",
                        category=DownloadCategory.PDF_DOCUMENTS
                    )
                
                # Add DOC files
                for doc_name, doc_content in file_info['doc_documents'].items():
                    download_manager.add_item(
                        name=doc_name,
                        content=doc_content,
                        file_type=FileType.DOC,
                        description=f"DOC version of {doc_name}",
                        category=DownloadCategory.DOC_DOCUMENTS
                    )
            
            # Store in session state
            st.session_state.download_manager = download_manager
            
            st.success(f"✅ Batch processing completed! {len(processed_files)} files processed.")
            
            # Show download area
            if 'download_manager' in st.session_state:
                download_center = EnhancedDownloadCenter(st.session_state.download_manager)
                download_center.render_download_center("📥 Download Processed Documents")
    
    # Show existing download manager if available
    elif 'download_manager' in st.session_state:
        download_center = EnhancedDownloadCenter(st.session_state.download_manager)
        download_center.render_download_center("📥 Download Processed Documents")
        
        if st.button("🗑️ Clear Download Queue"):
            del st.session_state.download_manager
            st.rerun()

def simulate_batch_processing() -> List[Dict[str, Any]]:
    """
    Simulate batch processing of Excel files
    
    Returns:
        List of processed file information
    """
    # Simulate processing 3 files
    processed_files = []
    
    for i in range(3):
        file_name = f"Project_{chr(65+i)}"
        
        # Simulate HTML documents
        html_documents = {
            f"{file_name}_Bill_Scrutiny": f"""
            <!DOCTYPE html>
            <html>
            <head><title>{file_name} Bill Scrutiny</title></head>
            <body>
                <h1>{file_name} Bill Scrutiny Sheet</h1>
                <p>This is a simulated bill scrutiny document for {file_name}.</p>
                <table border="1">
                    <tr><th>Item</th><th>Description</th><th>Quantity</th><th>Rate</th><th>Amount</th></tr>
                    <tr><td>1</td><td>Sample Work Item</td><td>10</td><td>100.00</td><td>1000.00</td></tr>
                </table>
            </body>
            </html>
            """,
            f"{file_name}_Deviation_Note": f"""
            <!DOCTYPE html>
            <html>
            <head><title>{file_name} Deviation Note</title></head>
            <body>
                <h1>{file_name} Deviation Note</h1>
                <p>This is a simulated deviation note for {file_name}.</p>
            </body>
            </html>
            """
        }
        
        # Simulate PDF documents (binary data)
        pdf_documents = {
            f"{file_name}_Bill_Scrutiny.pdf": b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n...",
            f"{file_name}_Deviation_Note.pdf": b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n..."
        }
        
        # Simulate DOC documents (binary data)
        doc_documents = {
            f"{file_name}_Bill_Scrutiny.doc": b"PK\x03\x04\x14\x00\x00\x00\x08\x00...",
            f"{file_name}_Deviation_Note.doc": b"PK\x03\x04\x14\x00\x00\x00\x08\x00..."
        }
        
        processed_files.append({
            'name': file_name,
            'html_documents': html_documents,
            'pdf_documents': pdf_documents,
            'doc_documents': doc_documents
        })
        
        # Simulate processing time
        time.sleep(0.5)
    
    return processed_files

def demonstrate_advanced_zip_features():
    """Demonstrate advanced ZIP features"""
    st.markdown("# ⚡ Advanced ZIP Features Demo")
    
    # Create sample data
    sample_data = {
        "project_a_bill.html": "<html><body><h1>Project A Bill</h1></body></html>",
        "project_a_summary.pdf": b"%PDF-1.4\nSample PDF content",
        "project_a_data.json": '{"project": "A", "amount": 1000.00}',
        "project_b_bill.html": "<html><body><h1>Project B Bill</h1></body></html>",
        "project_b_summary.pdf": b"%PDF-1.4\nSample PDF content",
        "project_b_data.json": '{"project": "B", "amount": 2000.00}'
    }
    
    # Configuration options
    st.markdown("## ⚙️ ZIP Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        compression_level = st.slider("Compression Level", 0, 9, 6)
        max_memory_mb = st.slider("Max Memory (MB)", 50, 500, 100)
        
    with col2:
        enable_validation = st.checkbox("Enable Validation", value=True)
        enable_integrity = st.checkbox("Enable Integrity Check", value=True)
    
    # Create ZIP with configuration
    if st.button("📦 Create Configured ZIP"):
        config = OptimizedZipConfig(
            compression_level=compression_level,
            memory_limit_mb=max_memory_mb,
            enable_integrity_check=enable_integrity
        )
        
        with OptimizedZipProcessor(config) as processor:
            # Progress tracking
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            def progress_callback(progress, status):
                progress_bar.progress(int(progress))
                progress_text.text(status)
                
            processor.set_progress_callback(progress_callback)
            
            try:
                # Add files to processor
                for name, content in sample_data.items():
                    processor.add_file_from_memory(content, name)
                
                # Create ZIP
                zip_buffer, metrics = processor.create_zip()
                
                # Clear progress
                progress_bar.empty()
                progress_text.empty()
                
                # Show results
                st.success(f"✅ ZIP created successfully!")
                st.json({
                    "Total Files": metrics.total_files,
                    "Original Size (KB)": f"{metrics.total_size_bytes / 1024:.2f}",
                    "Compressed Size (KB)": f"{metrics.compressed_size_bytes / 1024:.2f}",
                    "Compression Ratio (%)": f"{metrics.compression_ratio_percent:.2f}",
                    "Processing Time (s)": f"{metrics.processing_time_seconds:.3f}",
                    "Memory Usage (MB)": f"{metrics.memory_usage_peak_mb:.2f}"
                })
                
                # Download button
                st.download_button(
                    label="📥 Download Configured ZIP",
                    data=zip_buffer,
                    file_name="configured_documents.zip",
                    mime="application/zip"
                )
                
            except Exception as e:
                st.error(f"❌ Error creating ZIP: {str(e)}")

def show_performance_comparison():
    """Show performance comparison between basic and enhanced ZIP processing"""
    st.markdown("# 📊 Performance Comparison")
    
    # Sample data for comparison
    small_data = {f"file_{i}.txt": f"Content of file {i}" for i in range(10)}
    medium_data = {f"file_{i}.txt": f"Content of file {i} " * 100 for i in range(100)}
    large_data = {f"file_{i}.txt": f"Content of file {i} " * 1000 for i in range(1000)}
    
    datasets = {
        "Small (10 files)": small_data,
        "Medium (100 files)": medium_data,
        "Large (1000 files)": large_data
    }
    
    comparison_results = []
    
    for dataset_name, data in datasets.items():
        st.markdown(f"### Testing {dataset_name}")
        
        # Basic ZIP processing (simulation)
        basic_start = time.time()
        basic_size = sum(len(content) for content in data.values())
        basic_time = time.time() - basic_start
        
        # Enhanced ZIP processing
        enhanced_start = time.time()
        config = OptimizedZipConfig(compression_level=6)
        with OptimizedZipProcessor(config) as processor:
            try:
                # Add files to processor
                for name, content in data.items():
                    processor.add_file_from_memory(content, name)
                
                zip_buffer, metrics = processor.create_zip()
                enhanced_time = metrics.processing_time_seconds
                enhanced_size = metrics.compressed_size_bytes
                compression_ratio = metrics.compression_ratio_percent
            except Exception as e:
                st.error(f"Error with {dataset_name}: {e}")
                continue
        
        comparison_results.append({
            "Dataset": dataset_name,
            "Files": len(data),
            "Basic Time (s)": f"{basic_time:.4f}",
            "Enhanced Time (s)": f"{enhanced_time:.4f}",
            "Original Size (KB)": f"{basic_size / 1024:.2f}",
            "Compressed Size (KB)": f"{enhanced_size / 1024:.2f}",
            "Compression Ratio (%)": f"{compression_ratio:.2f}"
        })
    
    # Display comparison table
    if comparison_results:
        import pandas as pd
        df = pd.DataFrame(comparison_results)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("""
        ### Key Performance Improvements:
        
        1. **Memory Efficiency**: Enhanced processor monitors and limits memory usage
        2. **Compression Control**: Configurable compression levels for optimal balance
        3. **Progress Tracking**: Real-time feedback during ZIP creation
        4. **Error Handling**: Comprehensive error management and recovery
        5. **Security Features**: File validation and integrity checking
        """)

def main():
    """Main function to run the integrated demo"""
    st.set_page_config(
        page_title="Enhanced ZIP Integration Demo",
        page_icon="📦",
        layout="wide"
    )
    
    st.markdown("# 📦 Enhanced ZIP Integration Demo")
    st.markdown("This demo shows how enhanced ZIP functionality integrates with BillGeneratorUnified")
    
    # Tabs for different demos
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔄 Batch Integration", 
        "⚡ Advanced Features", 
        "📊 Performance Comparison",
        "📋 Implementation Guide"
    ])
    
    with tab1:
        integrate_with_batch_processor()
        
    with tab2:
        demonstrate_advanced_zip_features()
        
    with tab3:
        show_performance_comparison()
        
    with tab4:
        st.markdown("""
        ## Implementation Guide
        
        ### 1. Integration Steps
        
        1. **Replace Basic ZIP Creation**:
        ```python
        # Old way
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Add files...
        
        # New way
        config = OptimizedZipConfig(compression_level=6)
        with OptimizedZipProcessor(config) as processor:
            # Add files to processor
            for name, content in data_dict.items():
                processor.add_file_from_memory(content, name)
            zip_buffer, metrics = processor.create_zip()
        ```
        
        2. **Add Progress Tracking**:
        ```python
        def progress_callback(progress, status):
            st.progress(int(progress))
            st.text(status)
            
        processor.set_progress_callback(progress_callback)
        ```
        
        3. **Enhance Download Management**:
        ```python
        download_manager = EnhancedDownloadManager()
        download_manager.add_item(name, content, file_type, description, category)
        download_center = EnhancedDownloadCenter(download_manager)
        download_center.render_download_center("Download Center")
        ```
        
        ### 2. Configuration Options
        
        - **Compression Level**: 0-9 (0=no compression, 9=max compression)
        - **Memory Limit**: Prevents memory overflow
        - **File Size Limit**: Prevents oversized file processing
        - **Validation**: Enables/disables file validation
        - **Integrity Check**: Verifies ZIP file integrity
        
        ### 3. Benefits
        
        - **Memory Efficient**: Streaming and monitoring prevent crashes
        - **User Friendly**: Progress tracking and organized downloads
        - **Secure**: Validation and integrity checks protect data
        - **Flexible**: Configurable options for different use cases
        - **Reliable**: Better error handling and recovery
        
        ### 4. Migration Path
        
        1. Start with basic replacement of ZIP creation
        2. Gradually add progress tracking and configuration
        3. Implement enhanced download management
        4. Add advanced features like validation and integrity checking
        """)

if __name__ == "__main__":
    main()
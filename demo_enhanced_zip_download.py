"""
Demo Application for Enhanced ZIP Processing and Download Center
Showcases the advanced features of the optimized ZIP processor and enhanced download UI
"""

import streamlit as st
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Union

from core.utils.optimized_zip_processor import OptimizedZipProcessor, OptimizedZipConfig, create_zip_from_dict
from core.utils.download_manager import EnhancedDownloadManager, FileType, DownloadCategory
from core.ui.enhanced_download_center import EnhancedDownloadCenter, create_enhanced_download_center

def main():
    st.set_page_config(
        page_title="Enhanced ZIP & Download Demo",
        page_icon="📦",
        layout="wide"
    )
    
    # Custom CSS for better appearance
    st.markdown("""
    <style>
    .stProgress .st-bo {
        background-color: #00b894;
    }
    .stMetric-value {
        color: #00b894 !important;
    }
    .stAlert-info {
        background-color: #d1ecf1;
        border-left: 4px solid #00b894;
    }
    .stAlert-success {
        background-color: #d4edda;
        border-left: 4px solid #00b894;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📦 Enhanced ZIP Processing & Download Center")
    st.markdown("""
    This demo showcases the advanced features of our optimized ZIP processor and enhanced download center.
    
    ## Key Features Demonstrated:
    - **Memory-efficient streaming** for large files
    - **Intelligent caching** for faster repeated operations
    - **Advanced compression** with configurable levels
    - **Real-time progress tracking**
    - **Comprehensive file organization**
    - **Detailed analytics and metrics**
    """)
    
    # Create demo tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 Quick Demo", 
        "🔬 Performance Test", 
        "📊 Analytics Dashboard", 
        "⚙️ Advanced Configuration"
    ])
    
    with tab1:
        show_quick_demo()
        
    with tab2:
        show_performance_test()
        
    with tab3:
        show_analytics_dashboard()
        
    with tab4:
        show_advanced_configuration()

def show_quick_demo():
    """Show quick demo of enhanced ZIP and download features"""
    st.header("🚀 Quick Demo")
    
    # Create demo download manager
    if 'demo_manager' not in st.session_state:
        st.session_state.demo_manager = create_demo_download_manager()
        
    # Show download center
    download_center = create_enhanced_download_center(st.session_state.demo_manager)
    download_center.render_download_center("📥 Demo Download Center")
    
def show_performance_test():
    """Show performance testing capabilities"""
    st.header("🔬 Performance Test")
    
    st.markdown("""
    This section demonstrates the performance capabilities of our optimized ZIP processor.
    You can test with different file sizes and configurations.
    """)
    
    # Test configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Test Configuration")
        file_count = st.slider("Number of Files", 10, 1000, 100)
        file_size_kb = st.slider("File Size (KB)", 1, 1000, 50)
        compression_level = st.slider("Compression Level", 0, 9, 6)
        
    with col2:
        st.subheader("Advanced Settings")
        enable_caching = st.checkbox("Enable Caching", True)
        streaming_threshold = st.slider("Streaming Threshold (MB)", 1, 50, 5)
        memory_limit = st.slider("Memory Limit (MB)", 50, 500, 256)
        
    # Generate test data
    if st.button("🏃 Run Performance Test", type="primary"):
        with st.spinner("Generating test data..."):
            # Create test data
            test_data = {}
            for i in range(file_count):
                content = f"This is test file number {i+1} with content. " * (file_size_kb // 2)
                test_data[f"test_file_{i+1:04d}.txt"] = content
                
        # Configure processor
        config = OptimizedZipConfig(
            compression_level=compression_level,
            streaming_threshold_mb=streaming_threshold,
            memory_limit_mb=memory_limit,
            enable_caching=enable_caching
        )
        
        # Progress indicators
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        def progress_callback(progress: float, message: str):
            progress_bar.progress(int(progress))
            progress_text.text(message)
            
        # Create ZIP
        start_time = time.time()
        with OptimizedZipProcessor(config) as processor:
            processor.set_progress_callback(progress_callback)
            
            # Add files
            for filename, content in test_data.items():
                processor.add_file_from_memory(content, filename)
                
            # Create ZIP
            zip_buffer, metrics = processor.create_zip()
            
        end_time = time.time()
        
        # Clear progress
        progress_bar.empty()
        progress_text.empty()
        
        # Show results
        st.success("✅ Performance test completed!")
        
        # Metrics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Files Processed", metrics.total_files)
        with col2:
            st.metric("Processing Time", f"{metrics.processing_time_seconds:.2f}s")
        with col3:
            st.metric("Compression Ratio", f"{metrics.compression_ratio_percent:.1f}%")
        with col4:
            st.metric("Peak Memory", f"{metrics.memory_usage_peak_mb:.1f} MB")
            
        # Additional metrics
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        with detail_col1:
            st.metric("Original Size", f"{metrics.total_size_bytes / 1024 / 1024:.1f} MB")
        with detail_col2:
            st.metric("Compressed Size", f"{metrics.compressed_size_bytes / 1024 / 1024:.1f} MB")
        with detail_col3:
            st.metric("Streaming Files", metrics.streaming_files_count)
            
        # Download option
        st.download_button(
            label="📥 Download Test ZIP",
            data=zip_buffer,
            file_name=f"performance_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            use_container_width=True
        )
        
        # Cache information
        if metrics.cached_files_count > 0:
            st.info(f"ℹ️ {metrics.cached_files_count} files were loaded from cache")

def show_analytics_dashboard():
    """Show analytics dashboard"""
    st.header("📊 Analytics Dashboard")
    
    # Create or get demo manager
    if 'demo_manager' not in st.session_state:
        st.session_state.demo_manager = create_demo_download_manager()
        
    # Show analytics
    download_center = create_enhanced_download_center(st.session_state.demo_manager)
    stats = st.session_state.demo_manager.get_statistics()
    download_center._render_analytics(stats)

def show_advanced_configuration():
    """Show advanced configuration options"""
    st.header("⚙️ Advanced Configuration")
    
    st.markdown("""
    This section allows you to explore and test advanced configuration options
    for the optimized ZIP processor.
    """)
    
    # Configuration options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance Settings")
        max_workers = st.slider("Max Workers", 1, 8, 4)
        chunk_size = st.slider("Chunk Size (KB)", 1, 128, 16) * 1024
        temp_dir = st.text_input("Temp Directory", "")
        
    with col2:
        st.subheader("Security Settings")
        max_file_size = st.slider("Max File Size (MB)", 10, 200, 100)
        max_total_size = st.slider("Max Total Size (MB)", 100, 1000, 500)
        integrity_check = st.checkbox("Enable Integrity Check", True)
        
    # Test configuration
    if st.button("🧪 Test Configuration", type="primary"):
        config = OptimizedZipConfig(
            max_file_size_mb=max_file_size,
            max_total_size_mb=max_total_size,
            enable_integrity_check=integrity_check,
            chunk_size=chunk_size,
            temp_dir=temp_dir if temp_dir else None
        )
        
        # Create test data
        test_data = {
            "config_test.txt": "This is a test of the configuration.",
            "config_test.html": "<html><body><h1>Configuration Test</h1></body></html>",
            "config_test.json": json.dumps({"test": "configuration", "timestamp": str(datetime.now())})
        }
        
        try:
            with st.spinner("Testing configuration..."):
                # Create processor directly to avoid typing issues
                with OptimizedZipProcessor(config) as processor:
                    for filename, content in test_data.items():
                        processor.add_file_from_memory(content, filename)
                    zip_buffer, metrics = processor.create_zip()
                
            st.success("✅ Configuration test successful!")
            
            # Show metrics
            st.json({
                "total_files": metrics.total_files,
                "total_size_bytes": metrics.total_size_bytes,
                "compressed_size_bytes": metrics.compressed_size_bytes,
                "compression_ratio_percent": round(metrics.compression_ratio_percent, 2),
                "processing_time_seconds": round(metrics.processing_time_seconds, 3),
                "memory_usage_peak_mb": round(metrics.memory_usage_peak_mb, 1),
                "streaming_files_count": metrics.streaming_files_count
            })
            
            # Download option
            st.download_button(
                label="📥 Download Config Test ZIP",
                data=zip_buffer,
                file_name="config_test.zip",
                mime="application/zip",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ Configuration test failed: {str(e)}")

def create_demo_download_manager() -> EnhancedDownloadManager:
    """Create a demo download manager with sample data"""
    manager = EnhancedDownloadManager()
    
    # Sample HTML documents
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Bill Document</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Bill Generation Sample</h1>
        <p>This is a sample HTML document generated by the enhanced system.</p>
        <table>
            <tr><th>Item</th><th>Quantity</th><th>Rate</th><th>Amount</th></tr>
            <tr><td>Sample Item A</td><td>10</td><td>100.00</td><td>1000.00</td></tr>
            <tr><td>Sample Item B</td><td>5</td><td>200.00</td><td>1000.00</td></tr>
        </table>
        <p><strong>Total Amount: ₹2000.00</strong></p>
    </body>
    </html>
    """
    
    # Sample PDF (simulated)
    sample_pdf = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n..."
    
    # Sample JSON data
    sample_json = json.dumps({
        "bill_info": {
            "bill_number": "DEMO-001",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "amount": 2000.00,
            "customer": "Demo Customer"
        },
        "items": [
            {"name": "Sample Item A", "quantity": 10, "rate": 100.00, "amount": 1000.00},
            {"name": "Sample Item B", "quantity": 5, "rate": 200.00, "amount": 1000.00}
        ]
    }, indent=2)
    
    # Sample Excel data (CSV format for simplicity)
    sample_xlsx = """Item,Quantity,Rate,Amount
Sample Item A,10,100.00,1000.00
Sample Item B,5,200.00,1000.00
Total,,,""".encode('utf-8')
    
    # Add demo files to different categories
    manager.add_html_document("sample_bill_001.html", sample_html, "Sample HTML bill document")
    manager.add_html_document("sample_bill_002.html", sample_html, "Another sample HTML bill")
    manager.add_pdf_document("sample_bill_001.pdf", sample_pdf, "Sample PDF bill document")
    manager.add_pdf_document("sample_bill_002.pdf", sample_pdf, "Another sample PDF bill")
    manager.add_item("bill_data.json", sample_json.encode('utf-8'), FileType.JSON, 
                     "Bill data in JSON format", DownloadCategory.GENERAL)
    manager.add_item("items_data.xlsx", sample_xlsx, FileType.XLSX,
                     "Items data in Excel format", DownloadCategory.EXCEL_FILES)
    
    # Add more demo files for better demonstration
    for i in range(5):
        manager.add_html_document(f"demo_document_{i+1:02d}.html", sample_html, 
                                 f"Demo HTML document {i+1}")
        manager.add_pdf_document(f"demo_document_{i+1:02d}.pdf", sample_pdf,
                                f"Demo PDF document {i+1}")
    
    return manager

if __name__ == "__main__":
    main()
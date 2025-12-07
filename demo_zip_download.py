"""
Enhanced ZIP and Download System Demo
Showcases all the new features for zip processing and download management
"""
import streamlit as st
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import io

# Import our enhanced components
from core.ui.download_ui import DownloadManager, EnhancedDownloadUI, create_download_manager, create_download_ui
from core.utils.zip_processor import ZipProcessor, ZipConfig, ZipMetrics, StreamingZipProcessor

def show_zip_download_demo():
    """Show comprehensive demo of enhanced ZIP and download features"""
    st.markdown("# 🚀 Enhanced ZIP & Download System Demo")
    st.markdown("This demo showcases the advanced ZIP processing and download management capabilities.")
    
    # Create demo data
    demo_manager = create_demo_download_manager()
    
    # Demo tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", "⚡ Quick Demo", "🔧 Advanced Features", 
        "📊 Performance Metrics", "🧪 Testing"
    ])
    
    with tab1:
        show_overview()
    
    with tab2:
        show_quick_demo(demo_manager)
    
    with tab3:
        show_advanced_features()
    
    with tab4:
        show_performance_metrics()
    
    with tab5:
        show_testing_tools()

def show_overview():
    """Show overview of the enhanced system"""
    st.markdown("## 📋 System Overview")
    
    st.markdown("""
    ### 🎯 Key Features
    
    **🔒 Security & Validation**
    - File type validation and size limits
    - Secure temporary file handling
    - ZIP integrity verification
    - Memory usage monitoring
    
    **⚡ Performance Optimization**
    - Memory-efficient streaming for large files
    - Configurable compression levels
    - Progress tracking with callbacks
    - Parallel processing support
    
    **🎨 Enhanced User Experience**
    - File preview capabilities
    - Category-based organization
    - Multiple download formats
    - Real-time progress indicators
    
    **📊 Advanced Features**
    - Batch processing with ZIP creation
    - Custom ZIP structures
    - Compression metrics
    - File analysis and statistics
    """)
    
    # Feature comparison
    st.markdown("### 📈 Feature Comparison")
    
    comparison_data = {
        "Feature": ["Basic ZIP", "Enhanced ZIP", "Streaming ZIP"],
        "Memory Usage": ["High", "Controlled", "Very Low"],
        "Progress Tracking": ["❌", "✅", "✅"],
        "File Validation": ["❌", "✅", "✅"],
        "Compression Control": ["Limited", "Full", "Full"],
        "Error Recovery": ["❌", "✅", "✅"],
        "Large File Support": ["❌", "⚠️", "✅"],
        "Security Features": ["❌", "✅", "✅"]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)

def show_quick_demo(demo_manager: DownloadManager):
    """Show quick demo with sample data"""
    st.markdown("## ⚡ Quick Demo")
    
    st.markdown("### 📄 Sample Documents Ready for Download")
    
    # Show demo download area
    download_ui = create_download_ui(demo_manager)
    download_ui.render_download_area("📥 Demo Download Center")
    
    # Demo controls
    st.markdown("---")
    st.markdown("### 🎮 Demo Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Demo Data", type="secondary"):
            st.session_state.demo_refreshed = True
            st.rerun()
    
    with col2:
        if st.button("📊 Show ZIP Metrics", type="secondary"):
            _show_zip_metrics_demo()
    
    with col3:
        if st.button("🧪 Run Performance Test", type="secondary"):
            _run_performance_test()

def show_advanced_features():
    """Show advanced features demo"""
    st.markdown("## 🔧 Advanced Features")
    
    # ZIP Configuration Demo
    st.markdown("### ⚙️ ZIP Configuration Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Compression Levels**")
        compression_demo = st.selectbox(
            "Select Compression Level",
            ["None (0)", "Fast (1)", "Standard (6)", "High (8)", "Maximum (9)"]
        )
        
        st.markdown("**Memory Management**")
        memory_limit = st.slider("Memory Limit (MB)", 50, 500, 100)
        
        st.markdown("**File Structure**")
        zip_structure = st.selectbox(
            "ZIP Structure",
            ["Flat", "Hierarchical", "By Type", "Custom"]
        )
    
    with col2:
        st.markdown("**Security Options**")
        enable_validation = st.checkbox("Enable File Validation", value=True)
        enable_integrity_check = st.checkbox("Enable Integrity Check", value=True)
        
        st.markdown("**Performance Options**")
        enable_streaming = st.checkbox("Enable Streaming for Large Files")
        parallel_workers = st.slider("Parallel Workers", 1, 8, 4)
    
    # Test configuration
    if st.button("🧪 Test Configuration", type="primary"):
        _test_zip_configuration(compression_demo, memory_limit, zip_structure)

def show_performance_metrics():
    """Show performance metrics and analysis"""
    st.markdown("## 📊 Performance Metrics")
    
    # Simulate performance data
    metrics_data = {
        "Operation": ["Small ZIP (1MB)", "Medium ZIP (10MB)", "Large ZIP (100MB)", "Batch Processing"],
        "Processing Time (s)": [0.5, 2.3, 15.7, 8.9],
        "Memory Usage (MB)": [15, 45, 120, 85],
        "Compression Ratio (%)": [65, 72, 68, 70],
        "Files Processed": [10, 50, 200, 150]
    }
    
    df_metrics = pd.DataFrame(metrics_data)
    st.dataframe(df_metrics, use_container_width=True)
    
    # Performance charts
    st.markdown("### 📈 Performance Analysis")
    
    tab1, tab2 = st.tabs(["Processing Time", "Memory Usage"])
    
    with tab1:
        st.bar_chart(df_metrics.set_index("Operation")["Processing Time (s)"])
    
    with tab2:
        st.bar_chart(df_metrics.set_index("Operation")["Memory Usage (MB)"])

def show_testing_tools():
    """Show testing and diagnostic tools"""
    st.markdown("## 🧪 Testing Tools")
    
    # File integrity test
    st.markdown("### 🔍 ZIP Integrity Test")
    
    uploaded_zip = st.file_uploader(
        "Upload ZIP file for integrity check",
        type=['zip'],
        help="Test ZIP file integrity and get detailed information"
    )
    
    if uploaded_zip:
        _analyze_uploaded_zip(uploaded_zip)
    
    # Performance benchmark
    st.markdown("### ⚡ Performance Benchmark")
    
    if st.button("🏃 Run Performance Benchmark", type="primary"):
        _run_performance_benchmark()

def create_demo_download_manager() -> DownloadManager:
    """Create a demo download manager with sample data"""
    manager = create_download_manager()
    
    # Sample HTML documents
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Sample Bill Document</title></head>
    <body>
        <h1>Bill Generation Sample</h1>
        <p>This is a sample HTML document generated by the enhanced system.</p>
        <table border="1">
            <tr><th>Item</th><th>Quantity</th><th>Rate</th><th>Amount</th></tr>
            <tr><td>Sample Item</td><td>10</td><td>100</td><td>1000</td></tr>
        </table>
    </body>
    </html>
    """
    
    # Sample PDF (simulated)
    sample_pdf = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n..."
    
    # Sample JSON data
    sample_json = """
    {
        "bill_info": {
            "bill_number": "DEMO-001",
            "date": "2024-01-15",
            "amount": 1000.00
        },
        "items": [
            {"name": "Sample Item", "quantity": 10, "rate": 100}
        ]
    }
    """
    
    # Add demo files
    manager.add_item("sample_bill.html", sample_html, "html", 
                     "Sample HTML bill document", "Demo/HTML")
    manager.add_item("sample_bill.pdf", sample_pdf, "pdf", 
                     "Sample PDF bill document", "Demo/PDF")
    manager.add_item("bill_data.json", sample_json, "json", 
                     "Bill data in JSON format", "Demo/Data")
    
    # Add more demo files
    for i in range(3):
        manager.add_item(f"demo_document_{i+1}.html", sample_html, "html",
                         f"Demo HTML document {i+1}", "Demo/HTML")
        manager.add_item(f"demo_document_{i+1}.pdf", sample_pdf, "pdf",
                         f"Demo PDF document {i+1}", "Demo/PDF")
    
    return manager

def _show_zip_metrics_demo():
    """Show ZIP metrics demonstration"""
    st.markdown("### 📊 ZIP Metrics Demo")
    
    # Create sample data
    sample_data = {
        "file1.txt": "This is a sample text file for demonstration.",
        "file2.html": "<html><body><h1>Sample HTML</h1></body></html>",
        "file3.json": '{"demo": "data", "version": "1.0"}'
    }
    
    # Test different compression levels
    compression_levels = [0, 6, 9]
    results = []
    
    for level in compression_levels:
        config = ZipConfig(compression_level=level)
        
        with ZipProcessor(config) as processor:
            zip_data, metrics = processor.create_zip_from_data(sample_data)
            results.append({
                "Compression Level": level,
                "Original Size": f"{metrics.total_size} B",
                "Compressed Size": f"{metrics.compressed_size} B",
                "Ratio": f"{metrics.compression_ratio:.1f}%",
                "Time": f"{metrics.processing_time:.3f}s"
            })
    
    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)

def _run_performance_test():
    """Run performance test"""
    st.markdown("### 🏃 Performance Test Results")
    
    with st.spinner("Running performance test..."):
        # Create test data
        test_data = {}
        for i in range(100):
            test_data[f"test_file_{i}.txt"] = f"This is test file number {i} with some content."
        
        # Test with different configurations
        configs = [
            ("Basic", ZipConfig()),
            ("High Compression", ZipConfig(compression_level=9)),
            ("Low Memory", ZipConfig(max_memory_mb=50))
        ]
        
        results = []
        for name, config in configs:
            start_time = time.time()
            
            with ZipProcessor(config) as processor:
                zip_data, metrics = processor.create_zip_from_data(test_data)
            
            end_time = time.time()
            
            results.append({
                "Configuration": name,
                "Files": metrics.total_files,
                "Time (s)": f"{end_time - start_time:.3f}",
                "Memory (MB)": f"{metrics.memory_usage:.1f}",
                "Compression": f"{metrics.compression_ratio:.1f}%"
            })
        
        df_results = pd.DataFrame(results)
        st.dataframe(df_results, use_container_width=True)
        
        st.success("✅ Performance test completed!")

def _test_zip_configuration(compression_demo, memory_limit, zip_structure):
    """Test ZIP configuration"""
    st.markdown("### 🧪 Testing Configuration")
    
    # Parse compression level
    compression_map = {
        "None (0)": 0, "Fast (1)": 1, "Standard (6)": 6,
        "High (8)": 8, "Maximum (9)": 9
    }
    level = compression_map.get(compression_demo, 6)
    
    config = ZipConfig(
        compression_level=level,
        max_memory_mb=memory_limit
    )
    
    # Create test data
    test_data = {
        "config_test.txt": "This is a test for the ZIP configuration.",
        "config_test.html": "<html><body>Configuration Test</body></html>"
    }
    
    try:
        with st.spinner(f"Testing configuration: {compression_demo}, {memory_limit}MB, {zip_structure}"):
            with ZipProcessor(config) as processor:
                zip_data, metrics = processor.create_zip_from_data(test_data)
            
            st.success(f"✅ Configuration test successful!")
            st.markdown(f"""
            **Results:**
            - Compression Level: {level}
            - Memory Limit: {memory_limit}MB
            - Structure: {zip_structure}
            - Files Processed: {metrics.total_files}
            - Compression Ratio: {metrics.compression_ratio:.1f}%
            - Processing Time: {metrics.processing_time:.3f}s
            - Memory Used: {metrics.memory_usage:.1f}MB
            """)
            
            # Provide download
            st.download_button(
                label="📦 Download Test ZIP",
                data=zip_data,
                file_name="config_test.zip",
                mime="application/zip"
            )
            
    except Exception as e:
        st.error(f"❌ Configuration test failed: {str(e)}")

def _analyze_uploaded_zip(uploaded_zip):
    """Analyze uploaded ZIP file"""
    try:
        zip_data = uploaded_zip.read()
        
        # Use our ZIP processor to analyze
        config = ZipConfig()
        with ZipProcessor(config) as processor:
            if processor.validate_zip_integrity(zip_data):
                st.success("✅ ZIP file integrity check passed!")
                
                # Get detailed info
                zip_info = processor.get_zip_info(zip_data)
                
                st.markdown("**ZIP File Information:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Files", zip_info.get('total_files', 0))
                
                with col2:
                    size = zip_info.get('total_size', 0)
                    st.metric("Total Size", f"{size:,} bytes")
                
                with col3:
                    comp_size = zip_info.get('compressed_size', 0)
                    st.metric("Compressed Size", f"{comp_size:,} bytes")
                
                # Show file list
                if 'files' in zip_info:
                    st.markdown("**Files in ZIP:**")
                    files_df = pd.DataFrame(zip_info['files'])
                    st.dataframe(files_df, use_container_width=True)
            else:
                st.error("❌ ZIP file integrity check failed!")
                
    except Exception as e:
        st.error(f"❌ Error analyzing ZIP file: {str(e)}")

def _run_performance_benchmark():
    """Run comprehensive performance benchmark"""
    st.markdown("### 🏃 Performance Benchmark")
    
    with st.spinner("Running comprehensive benchmark..."):
        # Test different data sizes
        test_sizes = [10, 50, 100, 500]
        results = []
        
        for size in test_sizes:
            # Create test data
            test_data = {}
            for i in range(size):
                test_data[f"benchmark_file_{i}.txt"] = f"Benchmark content {i} " * 100
            
            # Test with standard configuration
            config = ZipConfig()
            
            start_time = time.time()
            with ZipProcessor(config) as processor:
                zip_data, metrics = processor.create_zip_from_data(test_data)
            end_time = time.time()
            
            results.append({
                "Files": size,
                "Original Size (KB)": metrics.total_size // 1024,
                "Compressed Size (KB)": metrics.compressed_size // 1024,
                "Compression (%)": f"{metrics.compression_ratio:.1f}",
                "Time (s)": f"{end_time - start_time:.3f}",
                "Memory (MB)": f"{metrics.memory_usage:.1f}",
                "Throughput (files/s)": f"{size / (end_time - start_time):.1f}"
            })
        
        df_benchmark = pd.DataFrame(results)
        st.dataframe(df_benchmark, use_container_width=True)
        
        # Performance insights
        st.markdown("**Performance Insights:**")
        avg_throughput = df_benchmark["Throughput (files/s)"].str.extract(r'(\d+\.?\d*)').astype(float).mean()
        avg_compression = df_benchmark["Compression (%)"].str.extract(r'(\d+\.?\d*)').astype(float).mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Average Throughput", f"{avg_throughput:.1f} files/s")
        with col2:
            st.metric("🗜️ Average Compression", f"{avg_compression:.1f}%")
        
        st.success("✅ Benchmark completed successfully!")

# Main function to run the demo
if __name__ == "__main__":
    show_zip_download_demo()
 

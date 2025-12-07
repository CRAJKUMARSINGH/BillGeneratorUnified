"""
Enhanced Download App for BillGeneratorUnified
Integrated application showcasing advanced ZIP processing and download capabilities
"""

import streamlit as st
import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.utils.download_manager import EnhancedDownloadManager
from core.ui.enhanced_download_center import EnhancedDownloadCenter, create_enhanced_download_center
from demo_enhanced_zip_download import create_demo_download_manager

def main():
    st.set_page_config(
        page_title="Enhanced Download Center",
        page_icon="📥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    
    .stProgress .st-bo {
        background-color: #00b894;
    }
    
    .stMetric-value {
        color: #00b894 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Beautiful header
    st.markdown("""
    <div class="main-header">
        <h1>📥 Enhanced Download Center</h1>
        <p>Advanced ZIP Processing & File Management for BillGeneratorUnified</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📋 Navigation")
        app_mode = st.selectbox(
            "Choose Mode",
            [
                "Download Center",
                "Demo Files",
                "Performance Test",
                "About"
            ]
        )
        
        st.markdown("---")
        st.markdown("## ⚙️ Settings")
        
        # Settings
        if 'settings' not in st.session_state:
            st.session_state.settings = {
                'default_compression': 6,
                'enable_caching': True,
                'streaming_threshold': 5
            }
            
        st.session_state.settings['default_compression'] = st.slider(
            "Default Compression", 0, 9, 
            st.session_state.settings['default_compression']
        )
        
        st.session_state.settings['enable_caching'] = st.checkbox(
            "Enable Caching", 
            st.session_state.settings['enable_caching']
        )
        
        st.session_state.settings['streaming_threshold'] = st.slider(
            "Streaming Threshold (MB)", 1, 50,
            st.session_state.settings['streaming_threshold']
        )
        
        st.markdown("---")
        st.markdown("## 📊 Stats")
        
        # Initialize download manager in session state
        if 'download_manager' not in st.session_state:
            st.session_state.download_manager = EnhancedDownloadManager()
            
        stats = st.session_state.download_manager.get_statistics()
        st.metric("Files", stats['total_items'])
        st.metric("Size", f"{stats['total_size_mb']} MB")
        st.metric("Categories", len(stats['categories']))
    
    # Main content based on mode
    if app_mode == "Download Center":
        show_download_center()
    elif app_mode == "Demo Files":
        show_demo_files()
    elif app_mode == "Performance Test":
        show_performance_test()
    elif app_mode == "About":
        show_about()

def show_download_center():
    """Show the main download center"""
    st.markdown("## 📥 Download Center")
    
    # Create download center
    download_center = create_enhanced_download_center(st.session_state.download_manager)
    download_center.render_download_center()

def show_demo_files():
    """Show demo files section"""
    st.markdown("## 🎮 Demo Files")
    st.markdown("""
    This section provides sample files to demonstrate the download center capabilities.
    
    Click the button below to populate the download center with demo files.
    """)
    
    if st.button("🔄 Load Demo Files", type="primary"):
        # Create demo files
        demo_manager = create_demo_download_manager()
        
        # Transfer files to session manager
        demo_items = demo_manager.get_all_items()
        for item in demo_items:
            st.session_state.download_manager.add_item(
                item.name,
                item.content,
                item.file_type,
                item.description,
                item.category
            )
            
        st.success(f"✅ Loaded {len(demo_items)} demo files!")
        st.info("Navigate to the Download Center to view and download the demo files.")
        
    # Show current demo files
    if st.session_state.download_manager.get_all_items():
        st.markdown("### 📁 Current Demo Files")
        items = st.session_state.download_manager.get_all_items()
        
        # Group by category
        categorized = {}
        for item in items:
            category = item.category.value
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(item)
            
        for category, category_items in categorized.items():
            with st.expander(f"{category} ({len(category_items)} files)"):
                for item in category_items:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{item.name}**")
                        st.caption(item.description)
                    with col2:
                        st.write(f"{item.size_bytes / 1024:.1f} KB")
                    with col3:
                        st.download_button(
                            "📥 Download",
                            item.content,
                            item.name,
                            key=f"demo_{item.name}"
                        )

def show_performance_test():
    """Show performance test section"""
    st.markdown("## 🚀 Performance Test")
    st.markdown("""
    Test the performance of the optimized ZIP processor with different configurations.
    """)
    
    # Import performance test function
    from demo_enhanced_zip_download import show_performance_test
    show_performance_test()

def show_about():
    """Show about section"""
    st.markdown("## ℹ️ About Enhanced Download Center")
    
    st.markdown("""
    ### 🎯 Features
    
    **🔒 Security & Validation**
    - File type validation and size limits
    - Secure temporary file handling
    - ZIP integrity verification
    - Memory usage monitoring
    
    **⚡ Performance Optimization**
    - Memory-efficient streaming for large files
    - Configurable compression levels
    - Progress tracking with callbacks
    - Intelligent caching system
    
    **🎨 Enhanced User Experience**
    - Modern file browser with filtering
    - Category-based organization
    - File preview capabilities
    - Real-time progress indicators
    
    **📊 Advanced Features**
    - Detailed analytics and metrics
    - Batch processing integration
    - Custom ZIP structures
    - Comprehensive error handling
    
    ### 🛠️ Technical Details
    
    **Optimized ZIP Processor**
    - Streaming for files larger than threshold
    - Configurable compression levels (0-9)
    - Memory usage limiting
    - Parallel processing support
    
    **Enhanced Download Manager**
    - Categorization system
    - File type detection
    - Statistics tracking
    - Session persistence
    
    **Enhanced Download Center**
    - Modern UI with Streamlit components
    - Advanced filtering and search
    - Analytics dashboard
    - Performance metrics
    """)

if __name__ == "__main__":
    main()
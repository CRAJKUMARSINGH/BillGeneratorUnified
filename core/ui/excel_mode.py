"""
Excel Upload Mode UI
"""
import streamlit as st
from pathlib import Path

def show_excel_mode(config):
    """Show Excel upload interface"""
    st.markdown("## 📊 Excel Upload Mode")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📝 Instructions
        1. Upload your Excel file
        2. Select configuration options
        3. Generate documents
        4. Download results
        """)
    
    with col2:
        st.info(f"""
        **Max File Size:** {config.processing.max_file_size_mb}MB
        **PDF Engine:** {config.processing.pdf_engine}
        **Caching:** {'Enabled' if config.processing.enable_caching else 'Disabled'}
        """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose Excel File",
        type=['xlsx', 'xls'],
        help="Upload your bill Excel file"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Options
        with st.expander("⚙️ Generation Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                generate_pdf = st.checkbox("Generate PDF", value=True)
                generate_html = st.checkbox("Generate HTML", value=True)
            
            with col2:
                if config.features.advanced_pdf:
                    add_watermark = st.checkbox("Add Watermark", value=False)
                    compress_pdf = st.checkbox("Compress PDF", value=False)
        
        # Generate button
        if st.button("🚀 Generate Documents", type="primary"):
            with st.spinner("Processing..."):
                try:
                    # Import generator
                    from core.generators.document_generator import DocumentGenerator
                    
                    # Process file
                    generator = DocumentGenerator()
                    
                    # Save uploaded file temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    
                    # Generate documents
                    st.info("📄 Generating documents...")
                    # Add your actual generation logic here
                    
                    # Celebrate with balloons! 🎈
                    st.balloons()
                    st.success("🎉 Documents generated successfully!")
                    
                    # Download buttons
                    st.markdown("### 📥 Download Documents")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            "📄 First Page",
                            data="Sample content",
                            file_name="first_page.html",
                            mime="text/html"
                        )
                    
                    with col2:
                        st.download_button(
                            "📊 Deviation Statement",
                            data="Sample content",
                            file_name="deviation.html",
                            mime="text/html"
                        )
                    
                    with col3:
                        st.download_button(
                            "📋 Certificate",
                            data="Sample content",
                            file_name="certificate.html",
                            mime="text/html"
                        )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    if config.ui.show_debug:
                        st.exception(e)

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
    
    # File upload with magenta background to highlight the required action
    st.markdown("""
    <div style='background-color: #ffccff; padding: 20px; border-radius: 10px; border: 2px solid #ff66ff;'>
        <h3 style='color: #cc00cc; margin-top: 0;'>📤 Excel File Required</h3>
        <p style='color: #990099; margin-bottom: 0;'>Please upload your Excel bill file below to continue.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose Excel File",
        type=['xlsx', 'xls'],
        help="Upload your bill Excel file"
    )
    
    if not uploaded_file:
        st.markdown("""
        <div style='background-color: #ffe6ff; padding: 15px; border-radius: 8px; border-left: 5px solid #ff66ff; margin-top: 10px;'>
            <p style='color: #cc00cc; font-weight: bold; margin: 0;'>⚠️ Please upload an Excel file to proceed with document generation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Options
        with st.expander("⚙️ Generation Options"):
            col1, col2, col3 = st.columns(3)
                                
            with col1:
                generate_pdf = st.checkbox("Generate PDF", value=True)
                generate_html = st.checkbox("Generate HTML", value=True)
                                
            with col2:
                generate_doc = st.checkbox("Generate DOC", value=False)
                                    
            with col3:
                if config.features.advanced_pdf:
                    add_watermark = st.checkbox("Add Watermark", value=False)
                    compress_pdf = st.checkbox("Compress PDF", value=False)
        
        # Generate button
        if st.button("🚀 Generate Documents", type="primary"):
            with st.spinner("Processing..."):
                try:
                    # Import processors and generator
                    from core.processors.excel_processor import ExcelProcessor
                    from core.generators.document_generator import DocumentGenerator
                    
                    # Process Excel file
                    excel_processor = ExcelProcessor()
                    processed_data = excel_processor.process_excel(uploaded_file)
                    
                    # Generate documents
                    st.info("📄 Generating documents...")
                    doc_generator = DocumentGenerator(processed_data)
                    html_documents = doc_generator.generate_all_documents()
                    
                    # Generate PDFs if requested
                    if generate_pdf:
                        pdf_documents = doc_generator.create_pdf_documents(html_documents)
                    else:
                        pdf_documents = {}
                    
                    # Generate DOCs if requested
                    if generate_doc:
                        doc_documents = doc_generator.generate_doc_documents()
                    else:
                        doc_documents = {}
                    
                    # Celebrate with balloons! 🎈
                    st.balloons()
                    st.success(f"🎉 Generated {len(html_documents)} HTML documents, {len(pdf_documents)} PDF documents, and {len(doc_documents)} DOC documents!")
                    
                    # Create zip file for all documents
                    import zipfile
                    import io
                    
                    # Create in-memory zip file
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        # Add HTML files to zip
                        for doc_name, html_content in html_documents.items():
                            zip_file.writestr(f"{doc_name}.html", html_content)
                        
                        # Add PDF files to zip (if generated)
                        for doc_name, pdf_content in pdf_documents.items():
                            zip_file.writestr(doc_name, pdf_content)
                        
                        # Add DOC files to zip (if generated)
                        for doc_name, doc_content in doc_documents.items():
                            zip_file.writestr(doc_name, doc_content)
                    
                    zip_buffer.seek(0)
                    
                    # Download buttons
                    st.markdown("### 📥 Download Documents")
                    
                    # Zip download button (always shown)
                    st.download_button(
                        "📦 Download All Documents (ZIP)",
                        data=zip_buffer,
                        file_name="bill_documents.zip",
                        mime="application/zip",
                        key="zip_download"
                    )
                    
                    # Individual downloads
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 📄 HTML Documents")
                        # Create columns for HTML download buttons
                        cols = st.columns(min(3, len(html_documents)))
                        
                        # HTML Downloads
                        for idx, (doc_name, html_content) in enumerate(html_documents.items()):
                            with cols[idx % 3]:
                                st.download_button(
                                    f"📄 {doc_name}",
                                    data=html_content,
                                    file_name=f"{doc_name}.html",
                                    mime="text/html",
                                    key=f"html_{idx}"
                                )
                    
                    # PDF Downloads (if generated)
                    if pdf_documents:
                        with col2:
                            st.markdown("#### 📕 PDF Documents")
                            cols_pdf = st.columns(min(3, len(pdf_documents)))
                            
                            for idx, (doc_name, pdf_content) in enumerate(pdf_documents.items()):
                                with cols_pdf[idx % 3]:
                                    st.download_button(
                                        f"📕 {doc_name}",
                                        data=pdf_content,
                                        file_name=doc_name,
                                        mime="application/pdf",
                                        key=f"pdf_{idx}"
                                    )
                    
                    # DOC Downloads (if generated)
                    if doc_documents:
                        with col3:
                            st.markdown("#### 📝 DOC Documents")
                            cols_doc = st.columns(min(3, len(doc_documents)))
                            
                            for idx, (doc_name, doc_content) in enumerate(doc_documents.items()):
                                with cols_doc[idx % 3]:
                                    st.download_button(
                                        f"📝 {doc_name}",
                                        data=doc_content,
                                        file_name=doc_name,
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key=f"doc_{idx}"
                                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    if config.ui.show_debug:
                        st.exception(e)

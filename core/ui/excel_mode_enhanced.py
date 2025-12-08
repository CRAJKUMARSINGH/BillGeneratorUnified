"""
Enhanced Excel Upload Mode UI with Advanced Download System
"""
import streamlit as st
from pathlib import Path
import pandas as pd
from typing import Dict, Any

from core.utils.download_manager import EnhancedDownloadManager, FileType, DownloadCategory
from core.ui.enhanced_download_ui import EnhancedDownloadUI, create_download_manager, create_enhanced_download_ui

def show_excel_mode(config):
    """Show enhanced Excel upload interface with advanced download system"""
    st.markdown("## 📊 Excel Upload Mode")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📝 Instructions
        1. Upload your Excel file
        2. Select configuration options
        3. Generate documents
        4. Download with enhanced options
        """)
    
    with col2:
        st.info(f"""
        **Max File Size:** {config.processing.max_file_size_mb}MB
        **PDF Engine:** {config.processing.pdf_engine}
        **Caching:** {'Enabled' if config.processing.enable_caching else 'Disabled'}
        """)
    
    # File upload with enhanced styling - Fluorescent Green
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ccffcc 0%, #99ff99 100%); 
                padding: 25px; 
                border-radius: 15px; 
                border: 3px dashed #00ff00; 
                text-align: center;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.4);'>
        <h3 style='color: #006600; margin-top: 0; font-size: 1.8rem;'>
            📤 Fluorescent Green Excel Upload
        </h3>
        <p style='color: #004d00; margin-bottom: 0; font-size: 1.2rem; font-weight: bold;'>
            Please upload your Excel bill file below to continue
        </p>
        <p style='color: #004d00; margin-top: 10px; font-style: italic;'>
            Supported formats: .xlsx, .xls
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose Excel File",
        type=['xlsx', 'xls'],
        help="Upload your bill Excel file"
    )
    
    if not uploaded_file:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ffe6ff 0%, #ffccff 100%); 
                    padding: 15px; 
                    border-radius: 8px; 
                    border-left: 5px solid #ff66ff; 
                    margin-top: 10px;
                    box-shadow: 0 2px 8px rgba(255, 102, 255, 0.2);'>
            <p style='color: #cc00cc; font-weight: bold; margin: 0; font-size: 1.1rem;'>
                ⚠️ Please upload an Excel file to proceed with document generation
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Enhanced options
        with st.expander("⚙️ Generation Options", expanded=True):
            col1, col2, col3 = st.columns(3)
                                
            with col1:
                generate_pdf = st.checkbox("📕 Generate PDF", value=True)
                generate_html = st.checkbox("📄 Generate HTML", value=True)
                                
            with col2:
                generate_doc = st.checkbox("📝 Generate DOC", value=False)
                generate_json = st.checkbox("📋 Generate JSON", value=False)
                                    
            with col3:
                if config.features.advanced_pdf:
                    add_watermark = st.checkbox("💧 Add Watermark", value=False)
                    compress_pdf = st.checkbox("🗜️ Compress PDF", value=False)
                
                # Enhanced ZIP options
                zip_compression = st.selectbox(
                    "🗜️ ZIP Compression",
                    ["Standard", "High", "Maximum", "None"],
                    index=0
                )
                
                zip_structure = st.selectbox(
                    "📁 ZIP Structure",
                    ["Flat", "By Type", "By Document", "Hierarchical"],
                    index=0
                )
        
        # Generate button with enhanced styling
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e6ffe6 0%, #ccffcc 100%); 
                    padding: 20px; 
                    border-radius: 12px; 
                    border: 2px solid #00ff00; 
                    text-align: center;
                    margin-top: 20px;'>
            <h3 style='color: #006600; margin: 0;'>
                🚀 Ready to Generate Documents
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Generate Documents", type="primary", use_container_width=True):
            with st.spinner("Processing and generating documents..."):
                try:
                    # Import processors and generator
                    from core.processors.excel_processor import ExcelProcessor
                    from core.generators.document_generator import DocumentGenerator
                    
                    # Process Excel file
                    excel_processor = ExcelProcessor()
                    processed_data = excel_processor.process_excel(uploaded_file)
                    
                    # Create download manager
                    download_manager = create_download_manager()
                    
                    # Initialize document containers
                    pdf_documents = {}
                    doc_documents = {}
                    
                    # Generate documents
                    st.info("📄 Generating documents...")
                    doc_generator = DocumentGenerator(processed_data)
                    html_documents = doc_generator.generate_all_documents()
                    
                    # Add HTML documents to download manager
                    if generate_html:
                        for doc_name, html_content in html_documents.items():
                            download_manager.add_html_document(
                                name=f"{doc_name}.html",
                                content=html_content,
                                description=f"HTML version of {doc_name}"
                            )
                    
                    # Generate PDFs if requested
                    if generate_pdf:
                        st.info("📕 Generating PDF documents...")
                        pdf_documents = doc_generator.create_pdf_documents(html_documents)
                        
                        for doc_name, pdf_content in pdf_documents.items():
                            download_manager.add_pdf_document(
                                name=doc_name,
                                content=pdf_content,
                                description=f"PDF version of {doc_name}"
                            )
                    
                    # Generate DOCs if requested
                    if generate_doc:
                        st.info("📝 Generating DOC documents...")
                        doc_documents = doc_generator.generate_doc_documents()
                        
                        for doc_name, doc_content in doc_documents.items():
                            download_manager.add_doc_document(
                                name=doc_name,
                                content=doc_content,
                                description=f"DOC version of {doc_name}"
                            )
                    
                    # Generate JSON if requested
                    if generate_json:
                        st.info("📋 Generating JSON data...")
                        json_data = _create_json_export(processed_data, html_documents)
                        
                        # Convert string to bytes for JSON
                        if isinstance(json_data, str):
                            json_bytes = json_data.encode('utf-8')
                        else:
                            json_bytes = json_data
                            
                        download_manager.add_item(
                            name="bill_data.json",
                            content=json_bytes,
                            file_type=FileType.JSON,
                            description="Complete bill data in JSON format",
                            category=DownloadCategory.GENERAL
                        )
                    
                    # Generate summary report
                    summary_data = _create_summary_report(processed_data, download_manager.download_items)
                    
                    # Convert string to bytes for text
                    if isinstance(summary_data, str):
                        summary_bytes = summary_data.encode('utf-8')
                    else:
                        summary_bytes = summary_data
                        
                    download_manager.add_item(
                        name="generation_summary.txt",
                        content=summary_bytes,
                        file_type=FileType.TXT,
                        description="Summary of document generation process",
                        category=DownloadCategory.GENERAL
                    )
                    
                    # Celebrate success!
                    st.balloons()
                    
                    # Show success metrics
                    total_files = len(download_manager.download_items)
                    stats = download_manager.get_statistics()
                    total_size = stats['total_size_bytes']
                    
                    # Initialize document counts
                    pdf_count = len(pdf_documents) if generate_pdf else 0
                    doc_count = len(doc_documents) if generate_doc else 0
                    
                    st.success(f"""
                    🎉 **Document Generation Complete!**
                    
                    **Generated Files:**
                    - 📄 HTML: {len(html_documents)} files
                    - 📕 PDF: {pdf_count} files
                    - 📝 DOC: {doc_count} files
                    - 📋 JSON: 1 file (if requested)
                    
                    **Total:** {total_files} files ({_format_size(total_size)})
                    """)
                    
                    # Store download manager in session state
                    st.session_state.download_manager = download_manager
                    
                    # Show enhanced download area
                    download_ui = create_enhanced_download_ui(download_manager)
                    download_ui.render_download_area("📥 Download Your Documents")
                    
                    # Quick download options
                    st.markdown("---")
                    st.markdown("### ⚡ Quick Downloads")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📦 Download All (ZIP)", type="secondary"):
                            _create_quick_zip(download_manager, "all", zip_compression, zip_structure)
                    
                    with col2:
                        if st.button("📄 HTML Only (ZIP)", type="secondary"):
                            _create_quick_zip(download_manager, "html", zip_compression, zip_structure)
                    
                    with col3:
                        if st.button("📕 PDF Only (ZIP)", type="secondary"):
                            _create_quick_zip(download_manager, "pdf", zip_compression, zip_structure)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    if config.ui.show_debug:
                        st.exception(e)

def _create_json_export(processed_data: Dict[str, Any], html_documents: Dict[str, str]) -> str:
    """Create JSON export of all data"""
    import json
    from datetime import datetime
    
    export_data = {
        "metadata": {
            "export_date": datetime.now().isoformat(),
            "version": "2.0.0",
            "export_type": "bill_generation_data"
        },
        "processed_data": {
            "title_data": processed_data.get("title_data", {}),
            "work_order_count": len(processed_data.get("work_order_data", [])),
            "bill_quantity_count": len(processed_data.get("bill_quantity_data", [])),
            "extra_items_count": len(processed_data.get("extra_items_data", [])),
            "deviation_count": len(processed_data.get("deviation_data", []))
        },
        "generated_documents": list(html_documents.keys()),
        "statistics": {
            "total_documents": len(html_documents),
            "has_extra_items": bool(processed_data.get("extra_items_data", pd.DataFrame()).empty is False),
            "has_deviation": bool(processed_data.get("deviation_data", pd.DataFrame()).empty is False)
        }
    }
    
    return json.dumps(export_data, indent=2, default=str)

def _create_summary_report(processed_data: Dict[str, Any], download_items) -> str:
    """Create a summary report of the generation process"""
    from datetime import datetime
    
    # Count items by category
    categories = {}
    for item in download_items:
        if item.category not in categories:
            categories[item.category] = 0
        categories[item.category] += 1
    
    total_size = sum(item.size_bytes for item in download_items)
    
    report = f"""
BILL GENERATION SUMMARY REPORT
=============================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INPUT DATA SUMMARY:
- Title Sheet Entries: {len(processed_data.get('title_data', {}))}
- Work Order Items: {len(processed_data.get('work_order_data', []))}
- Bill Quantity Items: {len(processed_data.get('bill_quantity_data', []))}
- Extra Items: {len(processed_data.get('extra_items_data', []))}
- Deviation Items: {len(processed_data.get('deviation_data', []))}

GENERATED DOCUMENTS:
"""
    
    for category, count in categories.items():
        report += f"- {category}: {count} files\n"
    
    report += f"""
TOTAL STATISTICS:
- Total Files Generated: {len(download_items)}
- Total Size: {_format_size(total_size)}
- Average File Size: {_format_size(total_size // len(download_items) if download_items else 0)}

PROCESSING INFORMATION:
- Processor: Enhanced Document Generator
- PDF Engine: ReportLab with enhancements
- ZIP Compression: Available
- Memory Management: Enabled

This report was automatically generated by BillGenerator Unified v2.0.0
"""
    
    return report

def _create_quick_zip(download_manager: EnhancedDownloadManager, filter_type: str, compression: str, structure: str):
    """Create quick ZIP download"""
    try:
        from core.utils.zip_processor import ZipProcessor, ZipConfig
        
        # Filter items based on type
        if filter_type == "all":
            items = download_manager.download_items
        elif filter_type == "html":
            items = [item for item in download_manager.download_items if item.file_type == FileType.HTML]
        elif filter_type == "pdf":
            items = [item for item in download_manager.download_items if item.file_type == FileType.PDF]
        else:
            items = download_manager.download_items
        
        if not items:
            st.warning(f"No {filter_type} files to download.")
            return
        
        # Create ZIP with progress
        with st.spinner(f"Creating {filter_type} ZIP archive..."):
            # Configure compression
            compression_map = {
                "None": 0,
                "Standard": 6,
                "High": 8,
                "Maximum": 9
            }
            compression_level = compression_map.get(compression, 6)
            
            config = ZipConfig(compression_level=compression_level)
            
            with ZipProcessor(config) as processor:
                # Create data dictionary
                data_dict = {item.name: item.content for item in items}
                
                # Create ZIP
                zip_data, metrics = processor.create_zip_from_data(data_dict)
                
                # Generate download
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{filter_type}_documents_{timestamp}.zip"
                
                st.download_button(
                    label=f"📦 Download {filter_type.title()} ZIP",
                    data=zip_data,
                    file_name=filename,
                    mime="application/zip",
                    key=f"quick_zip_{filter_type}_{timestamp}"
                )
                
                st.success(f"✅ {filter_type.title()} ZIP created with {metrics.total_files} files!")
                
    except Exception as e:
        st.error(f"❌ Failed to create ZIP: {str(e)}")

def _format_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
        
    return f"{size:.1f} {size_names[i]}"
"""
Online Entry Mode UI
"""
import streamlit as st
from datetime import datetime

def show_online_mode(config):
    """Show online entry interface"""
    st.markdown("## 💻 Online Entry Mode")
    
    # Highlight data entry requirements with magenta theme
    st.markdown("""
    <div style='background-color: #ffe6ff; padding: 15px; border-radius: 8px; border-left: 5px solid #ff66ff; margin-bottom: 20px;'>
        <h3 style='color: #cc00cc; margin-top: 0;'>✏️ Manual Data Entry Required</h3>
        <p style='color: #990099; margin-bottom: 0;'>Please fill in all the required bill details in the forms below to generate documents.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📝 Enter bill details manually through web forms")
    
    # Project Details
    with st.expander("📋 Project Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", placeholder="Enter project name")
            contractor = st.text_input("Contractor Name", placeholder="Enter contractor name")
        
        with col2:
            bill_date = st.date_input("Bill Date", value=datetime.now())
            tender_premium = st.number_input("Tender Premium (%)", min_value=0.0, max_value=100.0, value=4.0)
    
    # Work Items
    with st.expander("🔨 Work Items", expanded=True):
        st.markdown("### Add Work Items")
        
        num_items = st.number_input("Number of Items", min_value=1, max_value=50, value=3)
        
        items = []
        for i in range(int(num_items)):
            st.markdown(f"**Item {i+1}**")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                item_no = st.text_input(f"Item No.", value=f"{i+1:03d}", key=f"item_no_{i}")
            with col2:
                description = st.text_input(f"Description", key=f"desc_{i}")
            with col3:
                quantity = st.number_input(f"Quantity", min_value=0.0, key=f"qty_{i}")
            with col4:
                rate = st.number_input(f"Rate", min_value=0.0, key=f"rate_{i}")
            
            items.append({
                'item_no': item_no,
                'description': description,
                'quantity': quantity,
                'rate': rate
            })
    
    # Generate button
    if st.button("🚀 Generate Documents", type="primary"):
        if not project_name:
            st.error("❌ Please enter project name")
        else:
            with st.spinner("Generating documents..."):
                st.success("✅ Documents generated successfully!")
                
                # Show summary
                st.markdown("### 📊 Summary")
                total = sum(item['quantity'] * item['rate'] for item in items)
                premium_amount = total * (tender_premium / 100)
                net_payable = total + premium_amount
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Amount", f"₹{total:,.2f}")
                col2.metric("Premium", f"₹{premium_amount:,.2f}")
                col3.metric("NET PAYABLE", f"₹{net_payable:,.2f}")
                
                # Generate actual documents
                from core.generators.document_generator import DocumentGenerator
                
                # Prepare data structure similar to Excel processor output
                processed_data = {
                    "title_data": {
                        "Project Name": project_name,
                        "Contractor": contractor,
                        "Bill Date": bill_date.strftime('%d/%m/%Y'),
                        "Tender Premium %": tender_premium
                    },
                    "work_order_data": [],
                    "totals": {
                        "grand_total": total,
                        "premium": {
                            "percent": tender_premium / 100,
                            "amount": premium_amount
                        },
                        "payable": net_payable,
                        "net_payable": net_payable
                    }
                }
                
                # Add items to work order data
                for item in items:
                    if item['quantity'] > 0 and item['rate'] > 0:
                        processed_data["work_order_data"].append({
                            "Item No.": item['item_no'],
                            "Description": item['description'],
                            "Unit": "NOS",
                            "Quantity": item['quantity'],
                            "Rate": item['rate'],
                            "Amount": item['quantity'] * item['rate']
                        })
                
                # Generate documents
                doc_generator = DocumentGenerator(processed_data)
                html_documents = doc_generator.generate_all_documents()
                pdf_documents = doc_generator.create_pdf_documents(html_documents)
                doc_documents = doc_generator.generate_doc_documents()
                
                # Create zip file for all documents
                import zipfile
                import io
                
                # Create in-memory zip file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Add HTML files to zip
                    for doc_name, html_content in html_documents.items():
                        zip_file.writestr(f"{doc_name}.html", html_content)
                    
                    # Add PDF files to zip
                    for doc_name, pdf_content in pdf_documents.items():
                        zip_file.writestr(doc_name, pdf_content)
                    
                    # Add DOC files to zip
                    for doc_name, doc_content in doc_documents.items():
                        zip_file.writestr(doc_name, doc_content)
                
                zip_buffer.seek(0)
                
                # Download section
                st.markdown("### 📥 Download Documents")
                
                # Zip download button
                st.download_button(
                    "📦 Download All Documents (ZIP)",
                    data=zip_buffer,
                    file_name="online_bill_documents.zip",
                    mime="application/zip",
                    key="online_zip_download"
                )
                
                # Individual downloads
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 📄 HTML Documents")
                    cols = st.columns(min(3, len(html_documents)))
                    
                    for idx, (doc_name, html_content) in enumerate(html_documents.items()):
                        with cols[idx % 3]:
                            st.download_button(
                                f"📄 {doc_name}",
                                data=html_content,
                                file_name=f"{doc_name}.html",
                                mime="text/html",
                                key=f"online_html_{idx}"
                            )
                
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
                                key=f"online_pdf_{idx}"
                            )
                
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
                                key=f"online_doc_{idx}"
                            )

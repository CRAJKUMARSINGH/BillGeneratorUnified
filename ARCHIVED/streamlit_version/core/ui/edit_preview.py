import streamlit as st
import pandas as pd
from datetime import datetime

def show_edit_preview(processed_data):
    """
    Displays a premium interactive editor for the processed bill data.
    Allows users to polish S.No, Descriptions, Rates, and Quantities.
    """
    st.markdown("""
    <div style='background: rgba(251, 191, 36, 0.05); 
                padding: 1.5rem; 
                border-radius: 16px; 
                border-left: 4px solid #fbbf24;
                margin-bottom: 2rem;'>
        <h3 style='color: #fbbf24; margin: 0;'>📝 Review & Polish</h3>
        <p style='color: #94a3b8; margin: 0.5rem 0 0 0;'>
            Review the extracted data below. You can edit any cell directly before generating the final documents.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Header Information Section
    with st.expander("🏗️ Header & Project Details", expanded=True):
        col1, col2 = st.columns(2)
        
        # We store these back into processed_data if changed
        processed_data['work_name'] = col1.text_input("Work Name", processed_data.get('work_name', ''))
        processed_data['contractor_name'] = col2.text_input("Contractor Name", processed_data.get('contractor_name', ''))
        
        col3, col4, col5 = st.columns(3)
        processed_data['bill_serial'] = col3.text_input("Bill Serial", processed_data.get('bill_serial', ''))
        processed_data['agreement_no'] = col4.text_input("Agreement No", processed_data.get('agreement_no', ''))
        
        # Premium/Discount if available
        if 'tender_premium' in processed_data:
            processed_data['tender_premium'] = col5.number_input("Tender Premium (%)", value=float(processed_data.get('tender_premium', 0.0)), step=0.01)

    # Bill Items Grid Section
    st.markdown("#### 📊 Bill Items Grid")
    
    if 'items' in processed_data and processed_data['items']:
        # Convert items list to DataFrame for st.data_editor
        df_items = pd.DataFrame(processed_data['items'])
        
        # Ensure column order and friendly names
        column_config = {
            "item_no": st.column_config.TextColumn("S.No", width="small", help="Serial Number"),
            "description": st.column_config.TextColumn("Description", width="large", help="Item Description"),
            "unit": st.column_config.TextColumn("Unit", width="small"),
            "quantity": st.column_config.NumberColumn("Quantity", format="%.3f"),
            "rate": st.column_config.NumberColumn("Rate", format="%.2f"),
        }
        
        # Only show relevant columns in the editor
        display_cols = ["item_no", "description", "unit", "quantity", "rate"]
        
        edited_df = st.data_editor(
            df_items[display_cols],
            column_config=column_config,
            num_rows="dynamic",
            use_container_width=True,
            key="bill_items_editor"
        )
        
        # Sync back to processed_data
        processed_data['items'] = edited_df.to_dict('records')
    else:
        st.warning("⚠️ No bill items found to display.")

    # Extra Items Section (if any)
    if 'extra_items' in processed_data and processed_data['extra_items']:
        with st.expander("➕ Extra Items (Deviations)", expanded=False):
            df_extra = pd.DataFrame(processed_data['extra_items'])
            edited_extra = st.data_editor(
                df_extra,
                num_rows="dynamic",
                use_container_width=True,
                key="extra_items_editor"
            )
            processed_data['extra_items'] = edited_extra.to_dict('records')

    st.markdown("---")
    
    # Validation/Calculation Preview logic can be added here
    total_amount = sum(float(item.get('quantity', 0)) * float(item.get('rate', 0)) for item in processed_data.get('items', []))
    
    st.markdown(f"""
    <div style='text-align: right; padding: 1rem;'>
        <span style='color: #94a3b8; font-size: 0.9rem; text-transform: uppercase;'>Estimated Total</span><br>
        <span style='color: #fbbf24; font-size: 2rem; font-weight: 800;'>₹ {total_amount:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

    return processed_data

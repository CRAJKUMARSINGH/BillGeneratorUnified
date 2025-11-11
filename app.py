#!/usr/bin/env python3
"""
BillGenerator Unified - Enhanced Version
Includes best features from all 5 apps
"""
import os
import sys
from pathlib import Path
import streamlit as st

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

# Load configuration
from core.config.config_loader import ConfigLoader

# Get config from environment or use default
config = ConfigLoader.load_from_env('BILL_CONFIG', 'config/v01.json')

# Page config
st.set_page_config(
    page_title=config.app_name,
    page_icon=config.ui.branding.icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {config.ui.branding.color} 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .feature-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }}
    .stButton>button {{
        width: 100%;
        border-radius: 5px;
        height: 3rem;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <h1>{config.ui.branding.icon} {config.ui.branding.title}</h1>
    <p>Version {config.version} | Mode: {config.mode}</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"### {config.ui.branding.icon} {config.app_name}")
    st.markdown("---")
    
    # Mode selection
    modes = ["📊 Excel Upload", "💻 Online Entry"]
    
    if config.features.is_enabled('batch_processing'):
        modes.append("📦 Batch Processing")
    
    if config.features.is_enabled('analytics'):
        modes.append("📈 Analytics")
    
    selected_mode = st.radio("Select Mode", modes)
    
    st.markdown("---")
    
    # Feature status
    st.markdown("### ✨ Features")
    features_status = {
        "Excel Upload": config.features.excel_upload,
        "Online Entry": config.features.online_entry,
        "Batch Processing": config.features.batch_processing,
        "Advanced PDF": config.features.advanced_pdf,
        "Analytics": config.features.analytics
    }
    
    for feature, enabled in features_status.items():
        icon = "✅" if enabled else "❌"
        st.markdown(f"{icon} {feature}")

# Main content
if "📊 Excel Upload" in selected_mode:
    from core.ui.excel_mode import show_excel_mode
    show_excel_mode(config)

elif "💻 Online Entry" in selected_mode:
    from core.ui.online_mode import show_online_mode
    show_online_mode(config)

elif "📦 Batch Processing" in selected_mode:
    from core.processors.batch_processor import show_batch_mode
    show_batch_mode(config)

elif "📈 Analytics" in selected_mode:
    st.markdown("## 📈 Analytics Dashboard")
    st.info("Analytics dashboard coming soon!")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>BillGenerator Unified | Created by Rajkumar Singh Chauhan</p>
    <p>Configuration: {config.mode} | Features: {sum(features_status.values())}/{len(features_status)} enabled</p>
</div>
""", unsafe_allow_html=True)

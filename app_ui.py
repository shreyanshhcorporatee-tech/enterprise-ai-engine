import streamlit as st
import pandas as pd
import requests
import io

# Page Configuration
st.set_page_config(
    page_title="Enterprise AI Data Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Corporate Look
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .sub-title {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/artificial-intelligence.png", width=50)
    st.markdown("### **Engine Config**")
    st.info("System Status: **Online & Secure**")
    st.markdown("---")
    st.markdown("**Supported Modules:**")
    st.text("• Financial Ledgers\n• Sales & CRM Metrics\n• HR & Payroll Data\n• Operations Logs")

# Main Header Section
st.markdown('<p class="main-title">Enterprise AI Data Cleansing Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Automated unstructured data parser, semantic normalization, and institutional-grade structuring pipeline.</p>', unsafe_allow_html=True)

# Main File Upload Card
uploaded_file = st.file_uploader("Upload Target Dataset", type=["csv", "xlsx", "xls"], help="Drag and drop CSV or Excel files up to 200MB")

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("#### **Dataset Preview**")
    with col2:
        st.metric("Total Rows", len(df))
        
    st.dataframe(df.head(), use_container_width=True)
    
    if st.button("Initiate AI Normalization Pipeline"):
        chunk_size = 50 
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        
        cleaned_chunks = []
        api_url = "https://enterprise-ai-engine.onrender.com/clean-enterprise-data"
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_chunks = len(chunks)
        
        for idx, chunk in enumerate(chunks):
            status_text.text(f"Executing batch pipeline {idx + 1} of {total_chunks}...")
            data_string = chunk.to_string(index=False)
            
            try:
                response = requests.post(api_url, json={"data": data_string})
                if response.status_code == 200:
                    result_json = response.json()
                    cleaned_chunks.append(pd.DataFrame([result_json] if isinstance(result_json, dict) else result_json))
                else:
                    st.error(f"Execution fault in batch {idx + 1}: {response.text}")
            except Exception as e:
                st.error(f"Network Pipeline Error: {e}")
                
            progress_bar.progress((idx + 1) / total_chunks)
            
        status_text.text("Pipeline execution completed successfully.")
        
        if cleaned_chunks:
            final_cleaned_df = pd.concat(cleaned_chunks, ignore_index=True)
            
            st.markdown("#### **Normalized Output Preview**")
            st.dataframe(final_cleaned_df.head(), use_container_width=True)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_cleaned_df.to_excel(writer, index=False, sheet_name='Normalized_Data')
            processed_data = output.getvalue()
            
            st.download_button(
                label="Download Structured Excel Output",
                data=processed_data,
                file_name="enterprise_normalized_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
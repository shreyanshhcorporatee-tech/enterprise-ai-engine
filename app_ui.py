import streamlit as st
import pandas as pd
import requests
import io

# Page Configuration
st.set_page_config(
    page_title="Enterprise AI Data Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS (MNC Grade Styling)
st.markdown("""
    <style>
    .main-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #0f172a;
        letter-spacing: -0.03em;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1e293b;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation & Corporate Branding
with st.sidebar:
    st.markdown("### **MNC Enterprise Hub**")
    st.caption("Secure Cloud Pipeline v2.4")
    st.markdown("---")
    st.markdown("**Compliance & Security:**")
    st.success("SOC2 Type II Certified")
    st.info("Encryption: **AES-256 Bit**")
    st.markdown("---")
    st.markdown("**Active Domain Modules:**")
    st.text("• Financial Consolidation\n• Sales Pipeline Metrics\n• HR Headcount Logs\n• IT Server Event Telemetry")

# Main Header Section
st.markdown('<p class="main-header">Enterprise AI Data Cleansing & Normalization Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Institutional-grade semantic parsing and automated structuring for high-volume cross-functional datasets.</p>', unsafe_allow_html=True)

# File Uploader Section
uploaded_file = st.file_uploader("Upload Target Dataset (CSV, XLSX)", type=["csv", "xlsx", "xls"], help="Maximum threshold: 200MB per dataset file.")

if uploaded_file is not None:
    # Read File
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    # Professional KPI Metrics Layout
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="Total Dataset Rows", value=f"{len(df):,}")
    with c2:
        st.metric(label="Total Columns", value=len(df.columns))
    with c3:
        st.metric(label="Memory Footprint", value=f"{uploaded_file.size / (1024*1024):.2f} MB")
        
    st.markdown("#### **Input Preview (First 5 Rows)**")
    st.dataframe(df.head(), use_container_width=True)
    
    st.markdown("---")
    
    # Execution Button
    if st.button("🚀 Initialize Batch AI Normalization"):
        chunk_size = 1000 
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        
        cleaned_chunks = []
        api_url = "https://enterprise-ai-engine.onrender.com/clean-enterprise-data"
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_chunks = len(chunks)
        
        for idx, chunk in enumerate(chunks):
            status_text.text(f"Processing structural batch {idx + 1} of {total_chunks}...")
            data_string = chunk.to_string(index=False)
            
            try:
                response = requests.post(api_url, json={"data": data_string}, timeout=120)
                if response.status_code == 200:
                    result_json = response.json()
                    cleaned_chunks.append(pd.DataFrame([result_json] if isinstance(result_json, dict) else result_json))
                else:
                    st.error(f"Execution error in batch {idx + 1}: {response.text}")
            except Exception as e:
                st.error(f"Gateway connection timeout: {e}")
                
            progress_bar.progress((idx + 1) / total_chunks)
            
        status_text.text("Pipeline execution successfully completed.")
        
        if cleaned_chunks:
            final_cleaned_df = pd.concat(cleaned_chunks, ignore_index=True)
            
            st.markdown("#### **Normalized Output Preview**")
            st.dataframe(final_cleaned_df.head(), use_container_width=True)
            
            # Export Section
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_cleaned_df.to_excel(writer, index=False, sheet_name='Normalized_Enterprise_Data')
            processed_data = output.getvalue()
            
            st.download_button(
                label="📥 Download Enterprise Excel Report (.xlsx)",
                data=processed_data,
                file_name="enterprise_normalized_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
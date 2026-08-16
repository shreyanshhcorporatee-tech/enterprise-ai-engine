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

# Ultra-Clean Modern Corporate Dark CSS (High Visibility & Sleek Design)
st.markdown("""
    <style>
    /* Global background and text contrast */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Headers */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* File Uploader Box Styling */
    [data-testid="stFileUploader"] {
        background-color: #111827;
        border: 1px dashed #374151;
        border-radius: 10px;
        padding: 1.5rem;
    }
    
    /* Metrics Card Styling */
    div[data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* Professional Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.2rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        color: white;
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.5);
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
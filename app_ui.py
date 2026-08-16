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
    
    # Is logic ko apne code mein update kar lein:
if st.button("Initiate AI Normalization Pipeline"):
    # Bade data ke liye chunk size ko 1000 rows kar diya hai
    chunk_size = 1000 
    chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
    
    cleaned_chunks = []
    api_url = "https://enterprise-ai-engine.onrender.com/clean-enterprise-data"
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_chunks = len(chunks)
    
    for idx, chunk in enumerate(chunks):
        status_text.text(f"Processing massive dataset batch {idx + 1} of {total_chunks} (Total Rows: {len(df)})...")
        data_string = chunk.to_string(index=False)
        
        try:
            response = requests.post(api_url, json={"data": data_string}, timeout=120) # Timeout badha diya hai
            if response.status_code == 200:
                result_json = response.json()
                cleaned_chunks.append(pd.DataFrame([result_json] if isinstance(result_json, dict) else result_json))
            else:
                st.error(f"Fault in batch {idx + 1}: {response.text}")
        except Exception as e:
            st.error(f"Connection timeout on heavy load: {e}")
            
        progress_bar.progress((idx + 1) / total_chunks)
        
    status_text.text("Massive dataset normalization completed successfully!")
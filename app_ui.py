import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Enterprise AI Data Engine", layout="wide")

st.title("⚡ Enterprise AI Data Pipeline & Cleansing Engine")
st.write("Kisi bhi department ka messy data (Finance, Sales, HR, Operations) upload karein, AI use clean karke turant structured Excel download karne ke liye taiyar karega.")

# File upload option (CSV ya Excel)
uploaded_file = st.file_uploader("Apni data file upload karein (CSV ya Excel):", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # File read karna
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("### 📂 Original Uploaded Data Preview:")
    st.dataframe(df.head())
    
    if st.button("🚀 Process & Clean Data with AI"):
        # Bade data ko handle karne ke liye batch/chunk mein baantna (Chunking logic)
        chunk_size = 50  # Ek baar mein 50 rows bhejenge taaki AI overload na ho
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        
        cleaned_chunks = []
        api_url = "https://enterprise-ai-engine.onrender.com/clean-enterprise-data" # Aapka live Render URL
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_chunks = len(chunks)
        
        for idx, chunk in enumerate(chunks):
            status_text.text(f"Processing batch {idx + 1} of {total_chunks}...")
            
            # DataFrame ko text/json format mein convert karke API ko bhejna
            data_string = chunk.to_string(index=False)
            
            try:
                response = requests.post(api_url, json={"data": data_string})
                if response.status_code == 200:
                    result_json = response.json()
                    # Cleaned data ko wapas DataFrame mein convert karna
                    # (Assume kar rahe hain ki API structured format ya json de rahi hai)
                    cleaned_chunks.append(pd.DataFrame([result_json] if isinstance(result_json, dict) else result_json))
                else:
                    st.error(f"Batch {idx + 1} mein error aaya: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
                
            progress_bar.progress((idx + 1) / total_chunks)
            
        status_text.text("Processing complete!")
        
        if cleaned_chunks:
            final_cleaned_df = pd.concat(cleaned_chunks, ignore_index=True)
            
            st.write("### ✨ Cleaned & Structured Data Output:")
            st.dataframe(final_cleaned_df.head())
            
            # Excel Download Button
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_cleaned_df.to_excel(writer, index=False, sheet_name='Cleaned_Data')
            processed_data = output.getvalue()
            
            st.download_button(
                label="📥 Download Cleaned Data as Excel (.xlsx)",
                data=processed_data,
                file_name="enterprise_cleaned_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
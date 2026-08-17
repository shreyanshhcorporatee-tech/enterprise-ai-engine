import streamlit as st
import json
from google import genai

st.set_page_config(page_title="Enterprise AI Data Cleanser", layout="wide")

st.title("🚀 Enterprise AI Data Cleansing Engine - Test Bench")
st.write("Excel add-in ki API ko yahan direct test karte hain!")

# API Key input or fallback to environment
api_key = st.text_input("Enter Gemini API Key (AIzaSy...):", type="password")

raw_data = st.text_area("Paste Raw Messy Data:", value="Client Name, PAN No., Phone Number, Location, Portfolio Value\n   amit  kumar  sharma ,   abcdE1234F  , +91-9876543210 ,   delhi  , INR 25,00,000\nPRIYANKA sen , x y z p 9 8 7 6 a , 09898989898 ,  Kolkata  , 3.5 Million")

if st.button("Run AI Normalization"):
    if not api_key:
        st.error("Pehle apni Gemini API key daalo bhai!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an enterprise-grade institutional data cleaning and normalization engine.
            Clean, parse, normalize, and structure the following raw dataset into a clean JSON array of standardized objects.
            
            Raw Data:
            {raw_data}
            
            CRITICAL: Return ONLY a valid JSON array. Do not include any extra text, markdown commentary, or explanations. Just start with '[' and end with ']'.
            """
            
            with st.spinner("AI is processing and cleaning data..."):
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                )
                
                cleaned_text = response.text.strip()
                if cleaned_text.startswith("```json"):
                    cleaned_text = cleaned_text[7:]
                elif cleaned_text.startswith("```"):
                    cleaned_text = cleaned_text[3:]
                if cleaned_text.endswith("```"):
                    cleaned_text = cleaned_text[:-3]
                    
                parsed_data = json.loads(cleaned_text.strip())
                
                st.success("Data Cleaned Successfully!")
                st.dataframe(parsed_data)
                
        except Exception as e:
            st.error(f"Error aagaya: {str(e)}")
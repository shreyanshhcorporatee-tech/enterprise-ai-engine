import os
import io
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Enterprise AI Engine")

# CORS Middleware (Excel ya kisi bhi web client se access ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class DataPayload(BaseModel):
    data: str

# Gemini Client Initialization (Make sure GEMINI_API_KEY environment variable is set on Render)
client = genai.Client()

@app.get("/")
def read_root():
    return {"status": "Enterprise AI Data Cleansing API is Live"}

@app.post("/clean-enterprise-data")
def clean_enterprise_data(payload: DataPayload):
    try:
        prompt = f"""
        You are an enterprise-grade institutional data cleaning and normalization engine.
        Your task is to take the following raw messy table data from Excel, clean names, standardize PAN numbers, format numbers/amounts properly, fix cities, and return a clean JSON array of objects.
        
        Raw Data:
        {payload.data}
        
        CRITICAL: Return ONLY a valid JSON array. Do not include any extra text, markdown commentary, or explanations. Just start with '[' and end with ']'.
        """
        
        # Using the standard stable model endpoint
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        
        cleaned_text = response.text.strip()
        
        # Clean up any potential markdown code blocks
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        cleaned_text = cleaned_text.strip()
        
        # Parse JSON directly to ensure it's valid before sending back to Excel
        parsed_data = json.loads(cleaned_text)
        return parsed_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# Excel Add-in Taskpane & Manifest Endpoints
# ==========================================
@app.get("/taskpane.html", response_class=HTMLResponse)
async def get_taskpane():
    with open("taskpane.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/manifest.xml")
async def get_manifest():
    return FileResponse("manifest.xml", media_type="application/xml")
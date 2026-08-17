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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataPayload(BaseModel):
    data: str

@app.get("/")
def read_root():
    return {"status": "Enterprise AI Data Cleansing API is Live"}

@app.post("/clean-enterprise-data")
def clean_enterprise_data(payload: DataPayload):
    try:
        # Fetching the token from environment
        token = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")
        
        # Initializing client with explicit token handling for GCP/Vertex tokens
        client = genai.Client(api_key=token)
        
        prompt = f"""
        You are an enterprise-grade institutional data cleaning and normalization engine.
        Clean, parse, normalize, and structure the following raw dataset into a clean JSON array of standardized objects.
        
        Raw Data:
        {payload.data}
        
        CRITICAL: Return ONLY a valid JSON array. Do not include any extra text, markdown commentary, or explanations. Just start with '[' and end with ']'.
        """
        
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
            
        cleaned_text = cleaned_text.strip()
        return json.loads(cleaned_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/taskpane.html", response_class=HTMLResponse)
async def get_taskpane():
    with open("taskpane.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/manifest.xml")
async def get_manifest():
    return FileResponse("manifest.xml", media_type="application/xml")
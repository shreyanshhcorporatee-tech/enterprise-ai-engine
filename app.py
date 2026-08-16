from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import pandas as pd
import json
import io
import os
from google import genai
from typing import List, Dict, Any

app = FastAPI(title="Enterprise AI Data Engine", version="2.0")

class DataRequest(BaseModel):
    raw_text: str

class DataResponse(BaseModel):
    status: str
    columns: List[str]
    total_rows: int
    data: List[Dict[str, Any]]

# Yeh bilkul clean aur safe tarika hai, SDK khud environment variable se key utha lega
ai_client = genai.Client()

@app.post("/clean-enterprise-data", response_model=DataResponse)
async def clean_data(request: DataRequest):
    try:
        prompt = f"""
        You are an elite Enterprise Data Architect and Risk Analyst. Analyze the following raw messy data text.
        Determine the most logical columns (including an added 'risk_level' column as 'High', 'Medium', or 'Low' based on anomalies or financial discrepancies) and extract the cleaned records into rows.
        CRITICAL: Return ONLY a valid JSON array of objects. Do not add any markdown formatting like ```json or ```.
        Data: {request.raw_text}
        """
        
        response = ai_client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
            
        parsed_data = json.loads(clean_text.strip())
        
        if not parsed_data:
            raise HTTPException(status_code=400, detail="No structured data could be extracted.")
            
        df = pd.DataFrame(parsed_data)
        cleaned_records = df.to_dict(orient="records")
        columns = list(df.columns)
        
        return {
            "status": "success",
            "columns": columns,
            "total_rows": len(df),
            "data": cleaned_records
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export-excel")
async def export_excel(request: DataRequest):
    try:
        prompt = f"""
        You are an elite Enterprise Data Architect. Analyze the following raw messy data text and extract cleaned records into structured rows.
        CRITICAL: Return ONLY a valid JSON array of objects. Do not add any markdown formatting like ```json or ```.
        Data: {request.raw_text}
        """
        
        response = ai_client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
            
        parsed_data = json.loads(clean_text.strip())
        df = pd.DataFrame(parsed_data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Cleaned_Enterprise_Data')
        output.seek(0)
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=cleaned_enterprise_data.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
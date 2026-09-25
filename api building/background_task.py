from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()

@app.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        # फाइलको साइज थाहा पाउन यसलाई रिड गर्नुपर्छ
        content = await file.read()
        size = len(content)
        
        results.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": size,
            "verdict": "selroti",
            "spectrum": [1.5, 2.3, 4.8, 5.0]  # यहाँ तपाईं आफ्नो spectrum को लिस्ट राख्न सक्नुहुन्छ
        })
    return {"results": results}
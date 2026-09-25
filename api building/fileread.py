
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile

MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

app = FastAPI()


# -----------------------------
# Helper function
# -----------------------------
async def process_file(file: UploadFile):
    contents = await file.read()

    # Check file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Expected an image, got {file.content_type}"
        )

    # Check file size
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {len(contents)} bytes. Maximum allowed is 5 MB."
        )

    # Fake prediction for now
    spectrum = [
        ["Selroti", 0.99999696016311646],
        ["Sekuwa", 2.9175131203373894e-05],
        ["Dhindo", 9.469994779465196e-07],
        ["Momo", 2.934817473487783e-07],
        ["Kheer", 1.224557255596892e-08],
    ]

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "verdict": "Selroti",
        "spectrum": spectrum,
    }


# -----------------------------
# Upload single image
# -----------------------------
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    return await process_file(file)


# -----------------------------
# Upload multiple images
# -----------------------------
@app.post("/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        result = await process_file(file)
        results.append(result)

    return {
        "count": len(results),
        "files": results,
    }

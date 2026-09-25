from PIL import ImageFile
from fastapi import FastAPI, UploadFile, File
import asyncio
from fastapi.exceptions import HTTPException
from typing import List


MAX_SIZE_BYTES = 5 * 1024 * 1024 # 5 MB

app = FastAPI()

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()    # the actual bytes
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, f"expected an image, got {file.content_type}")



    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(400, f"file too large: {len(contents)} bytes")

    return {"filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
            "verdict":"selroti",
            "spectrum":""}


@app.post("/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        results.append({"filename": file.filename, "size_bytes": len(contents)})
    return {"count": len(results), "files": results}




"""

from io import BytesIO
from PIL import Image

image = Image.open(BytesIO(image_bytes))
image = image.convert("RGB")

"""
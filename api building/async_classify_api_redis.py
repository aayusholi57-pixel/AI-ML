import io
import os
import time
import uuid
import logging
from collections import defaultdict, deque
from contextlib import asynccontextmanager

import fakeredis
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Request, Depends

from redis_job_store import get_redis_client, set_job, get_job, update_job

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("day50")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(BASE_DIR, "cnn_digit_model.npz"))
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
model_state: dict = {}

ARTIFICIAL_DELAY_S = 15


# --- rate limiting, unchanged from Day 49 ---
RATE_LIMIT_MAX_REQUESTS = 3
RATE_LIMIT_WINDOW_S = 10.0
request_log: dict[str, deque] = defaultdict(deque)


def check_rate_limit(request: Request):
    client_id = request.client.host if request.client else "unknown"
    now = time.time()
    timestamps = request_log[client_id]
    while timestamps and now - timestamps[0] > RATE_LIMIT_WINDOW_S:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        retry_after = round(RATE_LIMIT_WINDOW_S - (now - timestamps[0]), 1)
        raise HTTPException(
            status_code=429,
            detail=f"rate limit exceeded: max {RATE_LIMIT_MAX_REQUESTS} requests per {RATE_LIMIT_WINDOW_S:.0f}s",
            headers={"Retry-After": str(max(retry_after, 0.0))},
        )
    timestamps.append(now)


# --- same conv-feature CNN pipeline as Day 41/42/48/49 (unchanged) ---
def conv2d(img, kernel, stride=1, padding=0):
    if padding > 0:
        img = np.pad(img, padding, mode="constant")
    kh, kw = kernel.shape
    h, w = img.shape
    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            region = img[i * stride:i * stride + kh, j * stride:j * stride + kw]
            out[i, j] = np.sum(region * kernel)
    return out


def relu(x):
    return np.maximum(0.0, x)


def max_pool2d(feature_map, size=2, stride=2):
    h, w = feature_map.shape
    out_h = (h - size) // stride + 1
    out_w = (w - size) // stride + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            region = feature_map[i * stride:i * stride + size, j * stride:j * stride + size]
            out[i, j] = np.max(region)
    return out


KERNELS = {
    "vertical":   np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float),
    "horizontal": np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=float),
    "diag_main":  np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]], dtype=float),
    "diag_anti":  np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]], dtype=float),
}


def conv_features(img):
    feats = []
    for kernel in KERNELS.values():
        fmap = relu(conv2d(img, kernel, stride=1, padding=1))
        pooled = max_pool2d(fmap, size=2, stride=2)
        feats.append(pooled.flatten())
    return np.concatenate(feats)


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def preprocess_image(raw_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(raw_bytes)).convert("L").resize((8, 8), Image.LANCZOS)
    arr = np.array(img, dtype=np.float64) / 255.0 * 16.0
    return arr


# --- module-level shared fake Redis server, standing in for a real one ---
# In-class only: every FakeRedis client built against this one server shares
# state, the same way every uvicorn worker would share one real Redis server.
_FAKE_SERVER = fakeredis.FakeServer()


def run_classification_job(redis_client, job_id: str, raw_bytes: bytes, filename: str):
    update_job(redis_client, job_id, status="running")
    logger.info("job %s: started (filename=%s)", job_id, filename)
    try:
        time.sleep(ARTIFICIAL_DELAY_S)

        img_8x8 = preprocess_image(raw_bytes)
        W, b, mu, sigma = model_state["W"], model_state["b"], model_state["mu"], model_state["sigma"]
        feats = conv_features(img_8x8)
        feats_std = (feats - mu) / np.where(sigma == 0, 1.0, sigma)
        probs = softmax(feats_std @ W + b)
        predicted = int(probs.argmax())

        update_job(redis_client, job_id, status="done", result={
            "filename": filename,
            "predicted_digit": predicted,
            "confidence": round(float(probs[predicted]), 4),
        })
        logger.info("job %s: done -> digit %d (%.3f)", job_id, predicted, probs[predicted])
    except Exception as exc:
        update_job(redis_client, job_id, status="error", error=str(exc))
        logger.exception("job %s: failed", job_id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.path.isfile(MODEL_PATH):
        with np.load(MODEL_PATH) as data:
            required = {"W", "b", "mu", "sigma"}
            missing = required.difference(data.files)
            if missing:
                raise RuntimeError(f"Model file is missing arrays: {', '.join(sorted(missing))}")
            model_state.update({key: data[key] for key in required})
    else:
        logger.warning("Model file not found at %s; classification endpoints will return 503", MODEL_PATH)

    redis_url = os.environ.get("REDIS_URL")
    model_state["redis"] = get_redis_client() if redis_url else get_redis_client(fake_server=_FAKE_SERVER)
    yield
    model_state.clear()


app = FastAPI(title="Day 50 — Redis-Backed Job Store", lifespan=lifespan)


@app.post("/classify-async", dependencies=[Depends(check_rate_limit)])
async def classify_async(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if "W" not in model_state:
        raise HTTPException(status_code=503, detail=f"classification model is unavailable: {MODEL_PATH}")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail=f"expected an image, got content_type={file.content_type}")

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="uploaded image is empty")
    if len(raw_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"image exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit")
    try:
        with Image.open(io.BytesIO(raw_bytes)) as image:
            image.verify()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="uploaded file is not a valid image") from exc
    job_id = str(uuid.uuid4())
    redis_client = model_state["redis"]
    set_job(redis_client, job_id, {"status": "queued", "result": None, "error": None})

    background_tasks.add_task(run_classification_job, redis_client, job_id, raw_bytes, file.filename or "upload")

    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def get_job_route(job_id: str):
    job = get_job(model_state["redis"], job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"no job with id {job_id}")
    return {"job_id": job_id, **job}


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": "W" in model_state, "redis_connected": "redis" in model_state}

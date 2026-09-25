from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.exceptions import HTTPException
import time
import logging
import uuid

# Configure basic logging and get a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("background_tasks_login ")

app = FastAPI(description="Background Tasks in FastAPI")

JOBS: dict[str, dict] = {} 

def run_classification_job(job_id: str, raw_bytes: bytes, filename: str):
    JOBS[job_id]["status"] = "running"
    try:
        time.sleep(15.0)   # stands in for a real slow model
        # img = preprocess_image(raw_bytes)                # Day 48's exact preprocessing
        probs = 1      # Day 41/42's exact CNN
        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["result"] = {"predicted_digit": 1}
    except Exception as exc:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error"] = str(exc)

def slow_notify(email: str, subject: str,):
    #print("sending email")
    logger.info("sending emails")
    time.sleep(10.0)  # simulates a slow email API call
    # print("email sent")
    logger.info("sent email")
    print(5/0)


@app.post("/signup-slow")
def signup_slow(email: str):
    slow_notify(email, "Welcome!")      # client waits the full 2s
    return {"status": "created"}

@app.post("/signup-fast")
def signup_fast(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(slow_notify, email, "Welcome!")
    return {"status": "predicting..."}   # returns immediately


JOBS: dict[str, dict] = {}   # in-memory job store

@app.post("/classify-async")
async def classify_async(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    raw_bytes = await file.read()
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "queued", "result": None, "error": None}

    background_tasks.add_task(run_classification_job, job_id, raw_bytes, file.filename)
    return {"job_id": job_id, "status": "queued"}   # instant



@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = JOBS.get(job_id)
    if job is None:
        raise HTTPException(404, f"no job with id {job_id}")
    return {"job_id": job_id, **job}
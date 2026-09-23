from fastapi import FASTAPI
app = FASTAPI()

@app.get("/")
def read_root():
    return {"MESSAGE": "hello"}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}

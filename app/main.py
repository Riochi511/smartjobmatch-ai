from fastapi import FastAPI

from app.api.jobs import router as jobs_router
from app.api.resumes import router as resume_router

app = FastAPI(
    title="SmartJob AI",
    version="0.3.0"
)

app.include_router(jobs_router)
app.include_router(resume_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SmartJob AI"
    }
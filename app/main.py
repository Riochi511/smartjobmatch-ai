from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.jobs import router as jobs_router
from app.api.resumes import router as resume_router
from app.api.career_coach import router as career_router
from app.exceptions.custom_exceptions import SmartJobException
from app.exceptions.handlers import (
    smartjob_exception_handler,
    generic_exception_handler,
)

app = FastAPI(
    title="SmartJob AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(SmartJobException, smartjob_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(jobs_router)
app.include_router(resume_router)
app.include_router(career_router)


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}
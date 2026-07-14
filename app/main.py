from fastapi import FastAPI
from app.api.routes import router as home_router
from app.api.jobs import router as jobs_router

app = FastAPI(
    title="SmartJob AI v2",
    version="1.0.0"
)

app.include_router(home_router)
app.include_router(jobs_router)
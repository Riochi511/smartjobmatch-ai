from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.jobs import router as jobs_router
from app.api.career_coach import router as career_coach_router
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    # Data download is now lazy (happens on first request)
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title="SmartJob AI",
    description="AI-Powered Resume Analysis, Hybrid Job Matching & Career Coaching",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(jobs_router)
app.include_router(career_coach_router)


@app.get("/")
def root():
    return {
        "message": "SmartJob AI is running",
        "version": "1.0.0",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
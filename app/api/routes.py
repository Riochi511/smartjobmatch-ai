from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to SmartJob AI v2",
        "status": "running"
    }
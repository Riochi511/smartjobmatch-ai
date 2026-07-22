import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

HISTORY_FILE = Path("data/resume_history.json")
ANALYSIS_FOLDER = Path("data/analyses")


@router.get("/history")
def resume_history():

    if not HISTORY_FILE.exists():
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


@router.get("/{resume_id}")
def get_resume(resume_id: str):

    file_path = ANALYSIS_FOLDER / f"{resume_id}.json"

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    with open(file_path, "r") as file:
        return json.load(file)
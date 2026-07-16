from fastapi import APIRouter, Query

from app.llm.career_coach import CareerCoach
from app.llm.context_builder import ContextBuilder

from app.services.result_store import ResultStore


router = APIRouter(
    prefix="/career-coach",
    tags=["Career Coach"]
)


@router.post("/")
async def career_coach(
    job_index: int = Query(
        0,
        ge=0,
        description="Index of the matched job."
    )
):

    latest = ResultStore.load()

    if not latest:
        return {
            "success": False,
            "message": (
                "No resume analysis found. "
                "Please upload and match a resume first."
            )
        }

    matches = latest.get(
        "matches",
        []
    )

    if job_index >= len(matches):
        return {
            "success": False,
            "message": "Invalid job index."
        }

    selected_match = matches[job_index]

    context = ContextBuilder.build(
        latest["analysis"],
        latest["skills"],
        selected_match,
        latest["recommendations"]
    )

    advice = CareerCoach.generate(
        context
    )

    return {
        "success": True,
        "resume_id": latest["resume_id"],
        "filename": latest["filename"],
        "selected_job": selected_match["title"],
        "company": selected_match["company"],
        "career_advice": advice
    }
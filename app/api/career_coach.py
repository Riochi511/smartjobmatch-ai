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
    result = ResultStore.load()

    if not result:
        return {
            "success": False,
            "message": (
                "No resume analysis found. "
                "Please upload and match a resume first using /jobs/match."
            )
        }

    matches = result.get("matches", [])

    if job_index >= len(matches):
        return {
            "success": False,
            "message": "Invalid job index."
        }

    selected_match = matches[job_index]

    context = ContextBuilder.build(
        result.get("analysis", ""),
        result.get("skills", []),
        selected_match,
        result.get("recommendations", [])
    )

    advice = CareerCoach.generate(context)

    return {
        "success": True,
        "resume_id": result.get("resume_id"),
        "filename": result.get("filename"),
        "selected_job": selected_match.get("title"),
        "company": selected_match.get("company"),
        "career_advice": advice
    }
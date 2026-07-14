from fastapi import APIRouter, UploadFile, File

from app.services.resume_processing_service import ResumeProcessingService

router = APIRouter(prefix="/jobs", tags=["Jobs"])

resume_service = ResumeProcessingService()


@router.post("/match")
async def match_jobs(file: UploadFile = File(...)):
    return resume_service.process_resume(file)
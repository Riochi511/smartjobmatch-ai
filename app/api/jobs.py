import os
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_parser import DocumentParser
from app.services.text_cleaner import TextCleaner
from app.services.skill_extractor import SkillExtractor
from app.services.resume_analyzer import ResumeAnalyzer
from app.services.job_loader import JobLoader

from app.ai.hybrid_matcher import HybridMatcher

from app.services.recommendation_engine import RecommendationEngine
from app.services.resume_repository import ResumeRepository
from app.services.analysis_repository import AnalysisRepository
from app.services.result_store import ResultStore

from app.utils.logger import logger


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

loader = JobLoader("data/raw/jobs.csv")


@router.post("/match")
async def match_jobs(file: UploadFile = File(...)):

    logger.info(f"Received resume: {file.filename}")

    filename = file.filename or ""
    ext = Path(filename).suffix.lower()

    if ext not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # Read file content
    content = await file.read()

    # Limit file size to 5 MB
    MAX_FILE_SIZE = 5 * 1024 * 1024
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File is too large. Maximum allowed size is 5 MB."
        )

    temp_file = f"temp_{filename}"

    try:
        with open(temp_file, "wb") as buffer:
            buffer.write(content)

        # Save original resume
        resume_record = ResumeRepository.save_resume(
            temp_file,
            filename
        )
        logger.info("Resume saved successfully.")

        # Extract text
        resume_text = DocumentParser.extract_text(temp_file)
        logger.info("Resume text extracted.")

        # Clean text
        cleaned_text = TextCleaner.clean(resume_text)
        logger.info("Resume text cleaned.")

        # Extract skills
        skills = SkillExtractor.extract(cleaned_text)
        logger.info(f"Extracted {len(skills)} skills.")

        # Analyze resume
        analysis = ResumeAnalyzer.analyze(cleaned_text, skills)
        logger.info("Resume analysis completed.")

        # Hybrid Matching
        matched_jobs = HybridMatcher.match(
            cleaned_text,
            skills
        )
        logger.info("Hybrid matching completed.")

        # Recommendations
        recommendations = RecommendationEngine.generate(matched_jobs)
        logger.info("Recommendations generated.")

        response = {
            "resume_id": resume_record["resume_id"],
            "uploaded_at": resume_record["uploaded_at"],
            "filename": filename,
            "analysis": analysis,
            "skills": skills,
            "recommendations": recommendations,
            "total_jobs": len(matched_jobs),
            "matches": matched_jobs
        }

        # Save analysis
        AnalysisRepository.save_analysis(
            resume_record["resume_id"],
            response
        )

        # Save latest result for Career Coach
        ResultStore.save(response)

        logger.info(f"Finished matching for {filename}")

        return response

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
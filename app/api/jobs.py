from fastapi import APIRouter, UploadFile, File

from app.services.document_parser import DocumentParser
from app.services.text_cleaner import TextCleaner
from app.services.skill_extractor import SkillExtractor
from app.services.resume_analyzer import ResumeAnalyzer
from app.services.job_loader import JobLoader
from app.services.matcher import Matcher
from app.services.recommendation_engine import RecommendationEngine
from app.services.resume_repository import ResumeRepository
from app.services.analysis_repository import AnalysisRepository

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

loader = JobLoader("data/jobs.csv")


@router.post("/match")
async def match_jobs(file: UploadFile = File(...)):

    # Save uploaded file temporarily
    temp_file = f"temp_{file.filename}"

    with open(temp_file, "wb") as buffer:
        buffer.write(await file.read())

    # Save permanent copy
    resume_record = ResumeRepository.save_resume(
        temp_file,
        file.filename
    )

    # Extract text
    resume_text = DocumentParser.extract_text(temp_file)

    # Clean text
    cleaned_text = TextCleaner.clean(resume_text)

    # Extract skills
    skills = SkillExtractor.extract(cleaned_text)

    # Resume statistics
    analysis = ResumeAnalyzer.analyze(
        cleaned_text,
        skills
    )

    # Load jobs
    jobs = loader.load_jobs()

    # Match jobs
    matched_jobs = Matcher.match(
        skills,
        jobs
    )

    # Recommendations
    recommendations = RecommendationEngine.generate(
        matched_jobs
    )

    analysis_result = {
        "resume_id": resume_record["resume_id"],
        "filename": file.filename,
        "analysis": analysis,
        "skills": skills,
        "recommendations": recommendations,
        "matches": matched_jobs
    }

    # Save analysis
    AnalysisRepository.save_analysis(
        resume_record["resume_id"],
        analysis_result
    )

    return {
        "resume_id": resume_record["resume_id"],
        "uploaded_at": resume_record["uploaded_at"],
        "filename": file.filename,
        "analysis": analysis,
        "skills": skills,
        "recommendations": recommendations,
        "total_jobs": len(matched_jobs),
        "matches": matched_jobs
    }
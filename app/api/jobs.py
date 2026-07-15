from fastapi import APIRouter, UploadFile, File

from app.services.job_loader import JobLoader
from app.services.document_parser import DocumentParser
from app.services.text_cleaner import TextCleaner
from app.services.skill_extractor import SkillExtractor
from app.services.matcher import Matcher
from app.services.resume_analyzer import ResumeAnalyzer
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

loader = JobLoader("data/jobs.csv")


@router.post("/match")
async def match_jobs(file: UploadFile = File(...)):
    """
    Upload a resume (PDF or DOCX),
    extract text,
    analyze it,
    and rank matching jobs.
    """

    temp_file = f"temp_{file.filename}"

    with open(temp_file, "wb") as buffer:
        buffer.write(await file.read())

    resume_text = DocumentParser.extract_text(temp_file)

    cleaned_text = TextCleaner.clean(resume_text)

    skills = SkillExtractor.extract(cleaned_text)

    analysis = ResumeAnalyzer.analyze(
        cleaned_text,
        skills
    )

    jobs = loader.load_jobs()

    matched_jobs = Matcher.match(
        skills,
        jobs
    )

    recommendations = RecommendationEngine.generate(
        matched_jobs
    )

    return {
        "filename": file.filename,
        "analysis": analysis,
        "skills": skills,
        "recommendations": recommendations,
        "total_jobs": len(matched_jobs),
        "matches": matched_jobs
    }
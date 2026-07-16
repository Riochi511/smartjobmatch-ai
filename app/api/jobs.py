from fastapi import APIRouter, UploadFile, File

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

loader = JobLoader("data/jobs.csv")


@router.post("/match")
async def match_jobs(file: UploadFile = File(...)):

    logger.info(f"Received resume: {file.filename}")

    # Save uploaded file temporarily
    temp_file = f"temp_{file.filename}"

    with open(temp_file, "wb") as buffer:
        buffer.write(await file.read())

    # Save original resume
    resume_record = ResumeRepository.save_resume(
        temp_file,
        file.filename
    )

    logger.info("Resume saved successfully.")

    # Extract text
    resume_text = DocumentParser.extract_text(
        temp_file
    )

    logger.info("Resume text extracted.")

    # Clean text
    cleaned_text = TextCleaner.clean(
        resume_text
    )

    logger.info("Resume text cleaned.")

    # Extract skills
    skills = SkillExtractor.extract(
        cleaned_text
    )

    logger.info(f"Extracted {len(skills)} skills.")

    # Analyze resume
    analysis = ResumeAnalyzer.analyze(
        cleaned_text,
        skills
    )

    logger.info("Resume analysis completed.")

    # Load jobs
    jobs = loader.load_jobs()

    logger.info(f"Loaded {len(jobs)} jobs.")

    # Hybrid Matching
    matched_jobs = HybridMatcher.match(
        cleaned_text,
        skills,
        jobs
    )

    logger.info("Hybrid matching completed.")

    # Recommendations
    recommendations = RecommendationEngine.generate(
        matched_jobs
    )

    logger.info("Recommendations generated.")

    response = {
        "resume_id": resume_record["resume_id"],
        "uploaded_at": resume_record["uploaded_at"],
        "filename": file.filename,
        "analysis": analysis,
        "skills": skills,
        "recommendations": recommendations,
        "total_jobs": len(matched_jobs),
        "matches": matched_jobs
    }

    # Save analysis history
    AnalysisRepository.save_analysis(
        resume_record["resume_id"],
        response
    )

    logger.info(
        f"Analysis saved for resume ID: {resume_record['resume_id']}"
    )

    # Save latest result for Career Coach
    ResultStore.save(response)

    logger.info("Latest analysis saved for Career Coach.")

    logger.info(
        f"Finished matching for {file.filename}"
    )

    return response
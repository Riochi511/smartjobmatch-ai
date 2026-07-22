from app.ai.hybrid_matcher import HybridMatcher


class JobMatchingService:

    def match_jobs(self, resume_text: str, resume_skills: list):
        """
        Run the complete hybrid matching pipeline.
        """

        return HybridMatcher.match(
            resume_text=resume_text,
            resume_skills=resume_skills
        )
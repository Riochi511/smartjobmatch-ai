from app.config import (
    KEYWORD_WEIGHT,
    SEMANTIC_WEIGHT
)

from app.services.matcher import Matcher
from app.ai.semantic_matcher import SemanticMatcher


class HybridMatcher:

    @staticmethod
    def match(resume_text, resume_skills, jobs):

        keyword_results = Matcher.match(
            resume_skills,
            jobs
        )

        semantic_results = SemanticMatcher.match(
            resume_text
        )

        semantic_lookup = {
            (
                job["title"],
                job["company"]
            ): job
            for job in semantic_results
        }

        results = []

        for keyword_job in keyword_results:

            key = (
                keyword_job["title"],
                keyword_job["company"]
            )

            semantic_job = semantic_lookup[key]

            keyword_score = keyword_job["match_score"]
            semantic_score = semantic_job["semantic_score"]

            overall_score = round(
                (
                    keyword_score * KEYWORD_WEIGHT
                ) +
                (
                    semantic_score * SEMANTIC_WEIGHT
                ),
                2
            )

            results.append({
                "title": keyword_job["title"],
                "company": keyword_job["company"],
                "location": keyword_job["location"],

                "required_skills": keyword_job["required_skills"],
                "matched_skills": keyword_job["matched_skills"],
                "missing_skills": keyword_job["missing_skills"],

                "keyword_match": keyword_score,
                "semantic_match": semantic_score,
                "overall_score": overall_score
            })

        results.sort(
            key=lambda x: x["overall_score"],
            reverse=True
        )

        return results
from app.config import (
    KEYWORD_WEIGHT,
    SEMANTIC_WEIGHT
)

from app.services.matcher import Matcher
from app.ai.semantic_matcher import SemanticMatcher


class HybridMatcher:

    @staticmethod
    def match(resume_text, resume_skills, jobs=None):

        # Stage 1: Semantic Retrieval
        semantic_candidates = SemanticMatcher.match(
            resume_text,
            top_k=200
        )

        # Stage 2: Keyword Re-ranking
        keyword_results = Matcher.match(
            resume_skills,
            semantic_candidates
        )

        results = []

        for job in keyword_results:

            keyword_score = job.get(
                "keyword_score",
                0.0
            )

            semantic_score = job.get(
                "semantic_score",
                0.0
            )

            overall_score = round(
                (
                    keyword_score * KEYWORD_WEIGHT
                ) +
                (
                    semantic_score * SEMANTIC_WEIGHT
                ),
                2
            )

            job["overall_score"] = overall_score

            # Confidence Level
            if overall_score >= 90:
                confidence = "Very High"
            elif overall_score >= 80:
                confidence = "High"
            elif overall_score >= 70:
                confidence = "Moderate"
            else:
                confidence = "Low"

            job["confidence"] = confidence

            results.append(job)

        results.sort(
            key=lambda x: x["overall_score"],
            reverse=True
        )

        #Return only the top 10 matches
        return results[:10]
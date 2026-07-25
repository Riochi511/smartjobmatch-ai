from typing import List, Dict, Any


class MatchExplainer:

    @staticmethod
    def explain(
        matched_skills: List[str],
        missing_skills: List[str],
        overall_score: float,
        semantic_score: float = 0.0,
        keyword_score: float = 0.0
    ) -> Dict[str, Any]:

        why_matched = []

        if matched_skills:
            top_skills = matched_skills[:4]
            why_matched.append(
                f"Strong overlap in {', '.join(top_skills)}"
            )

        if semantic_score >= 75:
            why_matched.append(
                "High semantic similarity with the job description"
            )
        elif semantic_score >= 55:
            why_matched.append(
                "Moderate semantic alignment with the role"
            )

        if keyword_score >= 80:
            why_matched.append(
                "Strong keyword match on core requirements"
            )

        if not why_matched:
            why_matched.append(
                "Partial alignment based on available skills"
            )

        # Gap severity
        missing_count = len(missing_skills)
        if missing_count == 0:
            gap_severity = "None"
        elif missing_count <= 2:
            gap_severity = "Low"
        elif missing_count <= 4:
            gap_severity = "Medium"
        else:
            gap_severity = "High"

        # Suggestion
        if not missing_skills:
            suggestion = "You are a strong match for this role. Highlight your relevant experience clearly."
        else:
            top_missing = missing_skills[:2]
            suggestion = (
                f"Focus on {', '.join(top_missing)} "
                f"to significantly improve your fit for this role."
            )

        return {
            "why_matched": why_matched,
            "gap_severity": gap_severity,
            "suggestion": suggestion
        }
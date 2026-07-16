class RecommendationEngine:

    @staticmethod
    def generate(matches):

        if not matches:
            return [
                "No matching jobs were found."
            ]

        best_match = matches[0]

        recommendations = []

        score = best_match["overall_score"]

        if score >= 85:
            recommendations.append(
                "Excellent resume! You are highly qualified for your best matching job."
            )

        elif score >= 70:
            recommendations.append(
                "Good resume. Strengthening a few skills can significantly improve your chances."
            )

        elif score >= 50:
            recommendations.append(
                "Your resume shows potential, but there are noticeable skill gaps that should be addressed."
            )

        else:
            recommendations.append(
                "Your resume needs significant improvement before applying for these roles."
            )

        missing = best_match.get("missing_skills", [])

        if missing:
            recommendations.append(
                "Focus on learning: " +
                ", ".join(missing)
            )

        recommendations.append(
            f"Keyword Match: {best_match['keyword_match']}%"
        )

        recommendations.append(
            f"Semantic Match: {best_match['semantic_match']:.2f}%"
        )

        recommendations.append(
            f"Overall Match Score: {best_match['overall_score']}%"
        )

        return recommendations
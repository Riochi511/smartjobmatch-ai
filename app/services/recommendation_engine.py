class RecommendationEngine:

    @staticmethod
    def generate(matches):

        if not matches:
            return [
                "No matching jobs were found."
            ]

        best_match = matches[0]

        recommendations = []

        score = best_match["match_score"]

        if score >= 80:
            recommendations.append(
                "Excellent resume! You are highly qualified for your best matching job."
            )

        elif score >= 60:
            recommendations.append(
                "Good resume. Learning the missing skills can significantly improve your chances."
            )

        else:
            recommendations.append(
                "Your resume needs improvement before applying for these roles."
            )

        missing = best_match["missing_skills"]

        if missing:
            recommendations.append(
                "Focus on learning: " +
                ", ".join(missing)
            )

        return recommendations
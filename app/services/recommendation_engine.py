class RecommendationEngine:

    @staticmethod
    def generate(matches):

        if not matches:
            return [
                "No matching jobs were found.",
                "Try uploading a resume with more technical experience or different target skills."
            ]

        best = matches[0]

        recommendations = []

        overall = best.get("overall_score", 0)
        keyword = best.get("keyword_score", 0)
        semantic = best.get("semantic_score", 0)
        confidence = best.get("confidence", "Unknown")

        # ----------------------------------------------------
        # Overall Resume Feedback
        # ----------------------------------------------------

        if overall >= 90:
            recommendations.append(
                "Excellent resume. You are highly competitive for this role."
            )

        elif overall >= 80:
            recommendations.append(
                "Strong resume with only minor improvements needed."
            )

        elif overall >= 70:
            recommendations.append(
                "Good resume. Strengthening a few important skills will improve your ranking."
            )

        elif overall >= 50:
            recommendations.append(
                "Your resume has potential but still contains noticeable skill gaps."
            )

        else:
            recommendations.append(
                "Your resume requires significant improvement before applying for similar roles."
            )

        # ----------------------------------------------------
        # Missing Skills
        # ----------------------------------------------------

        missing = best.get("missing_skills", [])

        if missing:

            top_missing = missing[:10]

            recommendations.append(
                "Top missing skills: " +
                ", ".join(top_missing)
            )

        # ----------------------------------------------------
        # Resume Strengths
        # ----------------------------------------------------

        matched = best.get("matched_skills", [])

        if matched:

            recommendations.append(
                "Strongest matching skills: " +
                ", ".join(matched[:10])
            )

        # ----------------------------------------------------
        # Score Breakdown
        # ----------------------------------------------------

        recommendations.append(
            f"Keyword Match: {keyword:.2f}%"
        )

        recommendations.append(
            f"Semantic Similarity: {semantic:.2f}%"
        )

        recommendations.append(
            f"Overall Match: {overall:.2f}%"
        )

        recommendations.append(
            f"Match Confidence: {confidence}"
        )

        # ----------------------------------------------------
        # Practical Advice
        # ----------------------------------------------------

        if overall < 70:

            recommendations.append(
                "Consider tailoring your resume to the job description before applying."
            )

        if keyword < semantic:

            recommendations.append(
                "Your experience aligns with the role, but your resume is missing important keywords."
            )

        elif semantic < keyword:

            recommendations.append(
                "Your resume contains the right keywords, but your overall experience appears less aligned."
            )

        return recommendations
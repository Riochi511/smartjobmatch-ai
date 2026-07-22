from collections import Counter


class ResumeAnalyzer:

    @staticmethod
    def analyze(text, skills):

        words = len(text.split())

        # Support both the old format (list of strings)
        # and the new format (list of dictionaries)

        if skills and isinstance(skills[0], dict):

            skill_names = [
                item["skill"]
                for item in skills
            ]

            categories = [
                item["category"]
                for item in skills
            ]

        else:

            skill_names = skills
            categories = []

        return {

            "word_count": words,

            "skill_count": len(skill_names),

            "category_count": len(
                set(categories)
            ),

            "categories": sorted(
                list(set(categories))
            ),

            "category_breakdown": dict(
                Counter(categories)
            )

        }
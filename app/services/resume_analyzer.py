class ResumeAnalyzer:

    @staticmethod
    def analyze(text, skills):

        words = len(text.split())

        return {
            "word_count": words,
            "skill_count": len(skills)
        }
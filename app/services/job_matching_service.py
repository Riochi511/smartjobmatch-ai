class JobMatchingService:

    def match_jobs(self, resume_text: str):
        return {
            "message": "Resume received successfully!",
            "resume_preview": resume_text[:100],
            "matches": [
                {
                    "title": "Machine Learning Engineer",
                    "company": "OpenAI",
                    "score": 97
                },
                {
                    "title": "AI Engineer",
                    "company": "Google",
                    "score": 94
                },
                {
                    "title": "Data Scientist",
                    "company": "Microsoft",
                    "score": 91
                },
                {
                    "title": "Python Developer",
                    "company": "Amazon",
                    "score": 89
                },
                {
                    "title": "ML Research Engineer",
                    "company": "NVIDIA",
                    "score": 87
                }
            ]
        }
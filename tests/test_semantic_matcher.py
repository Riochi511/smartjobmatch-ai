from app.ai.semantic_matcher import SemanticMatcher

resume = """
Python
FastAPI
Docker
Machine Learning
SQL
"""

jobs = [
    {
        "title": "Machine Learning Engineer",
        "company": "OpenAI",
        "location": "Remote",
        "skills": "Python, Machine Learning, Docker"
    },
    {
        "title": "Backend Developer",
        "company": "Amazon",
        "location": "USA",
        "skills": "Java, Spring Boot"
    }
]

results = SemanticMatcher.match(
    resume,
    jobs
)

for job in results:
    print(job)
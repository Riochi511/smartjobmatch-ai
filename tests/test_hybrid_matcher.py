from app.ai.hybrid_matcher import HybridMatcher

resume = """
Python
Machine Learning
Docker
FastAPI
SQL
"""

skills = [
    "Python",
    "Machine Learning",
    "Docker",
    "FastAPI",
    "SQL"
]

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

results = HybridMatcher.match(
    resume,
    skills,
    jobs
)

for job in results:
    print(job)
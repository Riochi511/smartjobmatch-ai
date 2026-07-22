from app.services.matcher import Matcher

# Sample resume skills
resume_skills = [
    "Python",
    "FastAPI",
    "Docker",
    "SQL"
]

# Sample jobs
jobs = [
    {
        "title": "Machine Learning Engineer",
        "company": "OpenAI",
        "location": "Remote",
        "skills": "Python, Machine Learning, Docker"
    },
    {
        "title": "Data Scientist",
        "company": "Google",
        "location": "USA",
        "skills": "Python, SQL, Pandas"
    },
    {
        "title": "Backend Developer",
        "company": "Amazon",
        "location": "USA",
        "skills": "Java, Spring Boot"
    }
]

results = Matcher.match(resume_skills, jobs)

for result in results:
    print(result)
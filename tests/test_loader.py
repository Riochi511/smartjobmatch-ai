from app.services.job_loader import JobLoader

loader = JobLoader("data/jobs.csv")

jobs = loader.load_jobs()

print(jobs)
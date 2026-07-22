from app.services.job_loader import JobLoader
from app.ai.job_embedding_cache import JobEmbeddingCache

loader = JobLoader("data/jobs.csv")

jobs = loader.load_jobs()

JobEmbeddingCache.build_cache(jobs)

print("Job embedding cache created successfully.")
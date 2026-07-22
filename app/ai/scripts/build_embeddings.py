from app.services.job_loader import JobLoader
from app.ai.job_embedding_cache import JobEmbeddingCache


def main():

    print("\nLoading jobs...\n")

    loader = JobLoader("data/jobs.csv")

    jobs = loader.load_jobs()

    print(f"Loaded {len(jobs):,} jobs.\n")

    JobEmbeddingCache.build_cache(jobs)

    print("\nEmbedding generation complete.\n")


if __name__ == "__main__":
    main()
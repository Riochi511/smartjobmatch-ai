import json
from pathlib import Path

from app.ai.embedding_service import EmbeddingService


class JobEmbeddingCache:

    CACHE_FILE = Path("data/embeddings/jobs_embeddings.json")

    @classmethod
    def build_cache(cls, jobs):

        cls.CACHE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cache = []

        for job in jobs:

            job_text = " ".join([
                job["title"],
                job["skills"],
                job["location"]
            ])

            embedding = EmbeddingService.embed(
                job_text
            ).tolist()

            cache.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "skills": job["skills"],
                "embedding": embedding
            })

        with open(cls.CACHE_FILE, "w") as file:
            json.dump(
                cache,
                file,
                indent=4
            )
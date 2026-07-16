import json
from pathlib import Path

import torch
from sentence_transformers import util

from app.ai.embedding_service import EmbeddingService


class SemanticMatcher:

    CACHE_FILE = Path("data/embeddings/jobs_embeddings.json")

    @staticmethod
    def match(resume_text, jobs=None):

        resume_embedding = EmbeddingService.embed(
            resume_text
        )

        with open(
            SemanticMatcher.CACHE_FILE,
            "r"
        ) as file:

            cached_jobs = json.load(file)

        results = []

        for job in cached_jobs:

            job_embedding = torch.tensor(
                job["embedding"]
            )

            similarity = util.cos_sim(
                resume_embedding,
                job_embedding
            ).item()

            results.append({

                "title": job["title"],

                "company": job["company"],

                "location": job["location"],

                "semantic_score": round(
                    similarity * 100,
                    2
                )
            })

        results.sort(
            key=lambda x: x["semantic_score"],
            reverse=True
        )

        return results
import json
from pathlib import Path

import faiss
import numpy as np

from app.ai.embedding_service import EmbeddingService


class VectorSearch:

    INDEX_FILE = Path("data/embeddings/jobs.index")
    CACHE_FILE = Path("data/embeddings/jobs_embeddings.json")

    @classmethod
    def search(cls, resume_text, top_k=5):

        index = faiss.read_index(str(cls.INDEX_FILE))

        with open(cls.CACHE_FILE, "r") as file:
            jobs = json.load(file)

        query = EmbeddingService.embed(
            resume_text
        )

        query = np.array(
            [query],
            dtype="float32"
        )

        faiss.normalize_L2(query)

        scores, indices = index.search(
            query,
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            job = jobs[idx].copy()

            job["semantic_score"] = round(
                float(score) * 100,
                2
            )

            results.append(job)

        return results
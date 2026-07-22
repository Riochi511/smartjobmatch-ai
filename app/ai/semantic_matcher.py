import faiss
import numpy as np
import pandas as pd

from app.ai.embedding_service import EmbeddingService


class SemanticMatcher:

    INDEX_PATH = "data/embeddings/jobs.index"
    DATA_PATH = "data/raw/jobs.csv"

    _index = None
    _jobs = None

    @classmethod
    def load_resources(cls):

        if cls._index is None:
            cls._index = faiss.read_index(cls.INDEX_PATH)

        if cls._jobs is None:
            cls._jobs = pd.read_csv(cls.DATA_PATH)

    @classmethod
    def match(cls, resume_text, top_k=200):

        cls.load_resources()

        resume_embedding = EmbeddingService.embed(
            resume_text
        ).astype(np.float32)

        resume_embedding = np.expand_dims(
            resume_embedding,
            axis=0
        )

        scores, indices = cls._index.search(
            resume_embedding,
            top_k
        )

        candidates = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            job = cls._jobs.iloc[idx].to_dict()

            job["semantic_score"] = round(
                float(score) * 100,
                2
            )

            candidates.append(job)

        

        return candidates
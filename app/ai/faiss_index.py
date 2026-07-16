import json
from pathlib import Path

import faiss
import numpy as np


class FaissIndex:

    CACHE_FILE = Path(
        "data/embeddings/jobs_embeddings.json"
    )

    INDEX_FILE = Path(
        "data/embeddings/jobs.index"
    )

    @classmethod
    def build_index(cls):

        with open(cls.CACHE_FILE, "r") as file:
            jobs = json.load(file)

        vectors = np.array(
            [
                job["embedding"]
                for job in jobs
            ],
            dtype="float32"
        )

        dimension = vectors.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        faiss.normalize_L2(vectors)

        index.add(vectors)

        faiss.write_index(
            index,
            str(cls.INDEX_FILE)
        )

        print(
            f"Indexed {index.ntotal} jobs."
        )
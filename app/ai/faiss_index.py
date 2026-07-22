import faiss
import numpy as np
from pathlib import Path


class FaissIndex:

    EMBEDDINGS_FILE = Path(
        "data/embeddings/job_embeddings.npy"
    )

    INDEX_FILE = Path(
        "data/embeddings/jobs.index"
    )

    @classmethod
    def build_index(cls):

        print("\nLoading embeddings...\n")

        vectors = np.load(
            cls.EMBEDDINGS_FILE,
            mmap_mode="r"
        ).astype("float32")

        faiss.normalize_L2(vectors)

        dimension = vectors.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(vectors)

        faiss.write_index(
            index,
            str(cls.INDEX_FILE)
        )

        print("\n===============================")
        print(f"Indexed {index.ntotal:,} jobs.")
        print("===============================\n")
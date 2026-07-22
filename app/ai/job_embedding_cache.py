import math
from pathlib import Path

import numpy as np
from numpy.lib.format import open_memmap
from tqdm import tqdm

from app.ai.model_manager import ModelManager


class JobEmbeddingCache:

    EMBEDDINGS_FILE = Path(
        "data/embeddings/job_embeddings.npy"
    )

    BATCH_SIZE = 512

    @classmethod
    def build_cache(cls, jobs):

        cls.EMBEDDINGS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        total_jobs = len(jobs)

        print(f"\nPreparing {total_jobs:,} jobs...\n")

        model = ModelManager.get_model()

        print("Generating first batch...\n")

        sample_text = cls._build_text(
            jobs[0]
        )

        sample_embedding = model.encode(
            sample_text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        dimension = sample_embedding.shape[0]

        # Create a valid .npy memory-mapped file
        embeddings = open_memmap(
            cls.EMBEDDINGS_FILE,
            mode="w+",
            dtype="float32",
            shape=(
                total_jobs,
                dimension
            )
        )

        total_batches = math.ceil(
            total_jobs / cls.BATCH_SIZE
        )

        write_position = 0

        for batch in tqdm(
            range(total_batches),
            desc="Embedding batches"
        ):

            start = batch * cls.BATCH_SIZE
            end = min(
                start + cls.BATCH_SIZE,
                total_jobs
            )

            batch_jobs = jobs[start:end]

            texts = [
                cls._build_text(job)
                for job in batch_jobs
            ]

            batch_embeddings = model.encode(
                texts,
                batch_size=64,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False
            )

            embeddings[
                write_position:
                write_position + len(batch_embeddings)
            ] = batch_embeddings

            write_position += len(
                batch_embeddings
            )

        embeddings.flush()

        print("\n=================================")
        print(
            f"Saved {total_jobs:,} embeddings."
        )
        print(
            f"Embedding dimension: {dimension}"
        )
        print("=================================\n")

    @staticmethod
    def _build_text(job):

        return f"""
Title: {job.get("title", "")}

Company: {job.get("company_name", "")}

Location: {job.get("location", "")}

Industry: {job.get("industry_name", "")}

Employment Type: {job.get("formatted_work_type", "")}

Experience Level: {job.get("formatted_experience_level", "")}

Description:
{job.get("description", "")}
"""
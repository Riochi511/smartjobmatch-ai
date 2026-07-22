import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from app.services.job_skill_extractor import JobSkillExtractor


RAW_DATA = Path("data/raw/jobs.csv")

PROCESSED_DIR = Path("data/processed")

PROCESSED_CSV = PROCESSED_DIR / "jobs_processed.csv"

PROCESSED_PARQUET = (
    PROCESSED_DIR / "jobs_processed.parquet"
)


def main():

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 70)
    print("Loading raw jobs...")
    print("=" * 70)

    df = pd.read_csv(RAW_DATA)

    print(f"Loaded {len(df):,} jobs.\n")

    required_skills = []

    required_categories = []

    for i, description in enumerate(
        df["description"].fillna(""),
        start=1
    ):

        if i % 1000 == 0:

            print(
                f"Processed {i:,}/{len(df):,} jobs..."
            )

        extracted = JobSkillExtractor.extract(
            description
        )

        required_skills.append(
            extracted["required_skills"]
        )

        required_categories.append(
            extracted[
                "required_skill_categories"
            ]
        )

    df["required_skills"] = required_skills

    df["required_skill_categories"] = (
        required_categories
    )

    print("\nSaving processed CSV...")

    df.to_csv(
        PROCESSED_CSV,
        index=False
    )

    print("Saving Parquet...")

    df.to_parquet(
        PROCESSED_PARQUET,
        index=False
    )

    print("\nDone.")

    print(f"CSV: {PROCESSED_CSV}")

    print(f"Parquet: {PROCESSED_PARQUET}")


if __name__ == "__main__":

    main()
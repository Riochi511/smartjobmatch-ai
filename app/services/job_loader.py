import pandas as pd
from pathlib import Path

from app.services.job_skill_extractor import JobSkillExtractor
from app.exceptions.custom_exceptions import JobLoadingException


class JobLoader:

    def __init__(self, csv_path: str = "data/raw/jobs.csv"):
        self.csv_path = Path(csv_path)

    def _ensure_file_exists(self):
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Job file '{self.csv_path}' was not found."
            )

    def load_jobs(self):
        try:
            self._ensure_file_exists()

            df = pd.read_csv(self.csv_path)

            jobs = df.to_dict(orient="records")

            for job in jobs:
                description = str(job.get("description", ""))
                extracted = JobSkillExtractor.extract(description)

                job["required_skills"] = extracted["required_skills"]
                job["required_skill_categories"] = extracted[
                    "required_skill_categories"
                ]

            return jobs

        except FileNotFoundError:
            raise JobLoadingException(
                f"Job file '{self.csv_path}' was not found."
            )
        except Exception as e:
            raise JobLoadingException(
                f"Unable to load jobs: {str(e)}"
            )
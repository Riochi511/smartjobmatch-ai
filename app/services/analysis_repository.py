import json
from pathlib import Path


class AnalysisRepository:

    ANALYSIS_FOLDER = Path("data/analyses")

    @classmethod
    def save_analysis(cls, resume_id, analysis):

        cls.ANALYSIS_FOLDER.mkdir(parents=True, exist_ok=True)

        file_path = cls.ANALYSIS_FOLDER / f"{resume_id}.json"

        with open(file_path, "w") as file:
            json.dump(
                analysis,
                file,
                indent=4
            )
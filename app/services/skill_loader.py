from pathlib import Path

import pandas as pd


class SkillLoader:

    def __init__(self, skills_directory="data/skills"):
        self.skills_directory = Path(skills_directory)

    def load_skills(self):

        skills = {}

        for csv_file in self.skills_directory.glob("*.csv"):

            category = self._format_category(
                csv_file.stem
            )

            df = pd.read_csv(csv_file)

            if "skill" not in df.columns:
                continue

            for skill in df["skill"].dropna():

                skill = str(skill).strip()

                if not skill:
                    continue

                skills[skill] = category

        return skills

    def _format_category(self, filename):

        return (
            filename
            .replace("_", " ")
            .replace("-", " ")
            .title()
        )
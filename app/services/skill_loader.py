import pandas as pd


class SkillLoader:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.skills = None

    def load_skills(self):
        """
        Load skills only once.
        """

        if self.skills is None:
            df = pd.read_csv(self.file_path)
            self.skills = (
                df["skill"]
                .dropna()
                .tolist()
            )

        return self.skills
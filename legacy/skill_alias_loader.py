import pandas as pd


class SkillAliasLoader:

    def __init__(self, path):
        self.path = path

    def load_aliases(self):

        df = pd.read_csv(self.path)

        return {
            row["alias"].lower(): row["canonical"]
            for _, row in df.iterrows()
        }
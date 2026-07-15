import pandas as pd


class JobLoader:

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_jobs(self):
        df = pd.read_csv(self.csv_path)
        return df.to_dict(orient="records")
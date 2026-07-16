import pandas as pd

from app.exceptions.custom_exceptions import (
    JobLoadingException
)


class JobLoader:

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_jobs(self):

        try:

            df = pd.read_csv(self.csv_path)

            return df.to_dict(
                orient="records"
            )

        except FileNotFoundError:

            raise JobLoadingException(
                f"Job file '{self.csv_path}' was not found."
            )

        except Exception as e:

            raise JobLoadingException(
                f"Unable to load jobs: {str(e)}"
            )
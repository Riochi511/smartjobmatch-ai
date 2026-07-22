import json
import os


class ResultStore:

    FILE_PATH = "data/cache/latest_result.json"

    @staticmethod
    def save(result):

        with open(ResultStore.FILE_PATH, "w") as file:
            json.dump(
                result,
                file,
                indent=4
            )

    @staticmethod
    def load():

        if not os.path.exists(ResultStore.FILE_PATH):
            return None

        with open(ResultStore.FILE_PATH, "r") as file:
            return json.load(file)
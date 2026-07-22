import json
from pathlib import Path


class ResultStore:

    FILE_PATH = "data/cache/latest_result.json"

    @staticmethod
    def save(result):
        path = Path(ResultStore.FILE_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as file:
            json.dump(result, file, indent=4)

    @staticmethod
    def load():
        path = Path(ResultStore.FILE_PATH)

        if not path.exists():
            return None

        with open(path, "r") as file:
            return json.load(file)
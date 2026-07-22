import json
import shutil
import uuid

from datetime import datetime
from pathlib import Path


class ResumeRepository:

    HISTORY_FILE = Path("data/cache/resume_history.json")
    RESUME_FOLDER = Path("data/resumes")

    @classmethod
    def save_resume(cls, temp_file, original_filename):

        # Create required directories
        cls.RESUME_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not cls.HISTORY_FILE.exists():
            cls.HISTORY_FILE.write_text("[]")

        resume_id = str(uuid.uuid4())

        extension = Path(original_filename).suffix
        stored_filename = f"{resume_id}{extension}"
        destination = cls.RESUME_FOLDER / stored_filename

        shutil.copy(temp_file, destination)

        with open(cls.HISTORY_FILE, "r") as file:
            history = json.load(file)

        record = {
            "resume_id": resume_id,
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "uploaded_at": datetime.now().isoformat()
        }

        history.append(record)

        with open(cls.HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)

        return record
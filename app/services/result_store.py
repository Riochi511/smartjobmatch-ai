import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

class ResultStore:
    # Use /tmp on Cloud Run (always writable) + fallback to data/cache
    PRIMARY_PATH = Path("/tmp/latest_result.json")
    FALLBACK_PATH = Path("data/cache/latest_result.json")

    @staticmethod
    def _get_path() -> Path:
        # Prefer /tmp on Cloud Run
        if os.getenv("K_SERVICE"):  # Cloud Run sets this
            return ResultStore.PRIMARY_PATH
        return ResultStore.FALLBACK_PATH

    @staticmethod
    def save(result: Dict[str, Any]) -> None:
        path = ResultStore._get_path()
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Also try to save to the fallback location
        try:
            ResultStore.FALLBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(ResultStore.FALLBACK_PATH, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # non-critical

    @staticmethod
    def load() -> Optional[Dict[str, Any]]:
        # Try primary first, then fallback
        for path in [ResultStore._get_path(), ResultStore.FALLBACK_PATH]:
            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    continue
        return None
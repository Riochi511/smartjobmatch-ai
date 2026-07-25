import os
from pathlib import Path

try:
    from google.cloud import storage
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False

GCS_BUCKET = os.getenv("GCS_BUCKET", "smartjob-ai-data")
GCS_PREFIX = os.getenv("GCS_PREFIX", "")

REQUIRED_FILES = {
    "data/raw/jobs.csv": "raw/jobs.csv",
    "data/embeddings/jobs.index": "embeddings/jobs.index",
    "data/embeddings/job_embeddings.npy": "embeddings/job_embeddings.npy",
}

SKILL_DIRS = [
    "data/skills",
    "data/cache",
    "data/resumes",
    "data/analyses",
    "data/raw",
    "data/embeddings",
]


def ensure_data_directories():
    for directory in SKILL_DIRS:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Directory ready: {directory}")


def download_from_gcs(bucket_name: str, source_blob: str, destination: str):
    local_path = Path(destination)

    if local_path.exists() and local_path.stat().st_size > 0:
        print(f"Already exists, skipping: {destination}")
        return

    print(f"Downloading gs://{bucket_name}/{source_blob} → {destination}")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob)

    local_path.parent.mkdir(parents=True, exist_ok=True)
    blob.download_to_filename(str(local_path))

    print(f"Download complete: {destination} ({local_path.stat().st_size} bytes)")


def ensure_data_ready():
    print("=== Starting data preparation ===")
    print(f"GCS_BUCKET = {GCS_BUCKET}")
    print(f"GCS_AVAILABLE = {GCS_AVAILABLE}")

    ensure_data_directories()

    if not GCS_AVAILABLE:
        print("google-cloud-storage not installed. Skipping download.")
        return

    if not GCS_BUCKET:
        print("GCS_BUCKET is empty. Skipping download.")
        return

    try:
        for local_path, gcs_path in REQUIRED_FILES.items():
            full_gcs_path = f"{GCS_PREFIX}/{gcs_path}".lstrip("/")
            download_from_gcs(GCS_BUCKET, full_gcs_path, local_path)

        print("=== All required data files are ready ===")
    except Exception as e:
        print(f"ERROR while downloading: {type(e).__name__}: {e}")
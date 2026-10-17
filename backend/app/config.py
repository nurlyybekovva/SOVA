from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/


class Settings(BaseSettings):
    api_key: str = "dev-key"
    use_stub: bool = True
    upload_dir: Path = BASE_DIR / "storage" / "uploads"
    db_path: Path = BASE_DIR / "storage" / "jobs.db"
    allowed_extensions: tuple = (".mov", ".mp4", ".avi")

    # video preprocessing (tune with ML teammate)
    segment_len_sec: float = 10.0
    segment_overlap_sec: float = 2.0
    frames_per_segment: int = 6

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)


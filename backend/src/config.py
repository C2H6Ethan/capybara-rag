from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
FILTERED_DIR = DATA_DIR / "filtered"
CHUNKS_DIR = DATA_DIR / "chunks"
ENV_PATH = PROJECT_ROOT / ".env"

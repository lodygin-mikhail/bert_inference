from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "prediction_project"
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA = DATA_DIR / "raw" / "reviews.csv"
PROCESSED_DATA = DATA_DIR / "processed" / "processed_reviews.csv"
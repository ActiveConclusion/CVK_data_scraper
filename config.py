from pathlib import Path

DATA_DIR = "data"
CANDIDATES_RAW_FILE_CSV = "01_01_candidates.csv"
ELECTED_RAW_FILE_CSV = "01_02_elected.csv"

CANDIDATES_RAW_FILE_CSV_PATH = Path(DATA_DIR, CANDIDATES_RAW_FILE_CSV)
ELECTED_RAW_FILE_CSV_PATH = Path(DATA_DIR, ELECTED_RAW_FILE_CSV)

REGIONS = ["Вінницька область", "Волинська область", "Дніпропетровська область"]
TYPES_OF_COUNCILS = ["Міські"]
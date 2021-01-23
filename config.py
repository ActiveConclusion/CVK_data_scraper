from pathlib import Path

DATA_DIR = "data"
CANDIDATES_RAW_FILE_CSV = "01_01_all_candidates.csv"
ELECTED_RAW_FILE_CSV = "01_02_elected_candidates.csv"
MERGED_FILE_CSV = "02_01_merged_candidates.csv"

CANDIDATES_RAW_FILE_CSV_PATH = Path(DATA_DIR, CANDIDATES_RAW_FILE_CSV)
ELECTED_RAW_FILE_CSV_PATH = Path(DATA_DIR, ELECTED_RAW_FILE_CSV)
MERGED_FILE_CSV_PATH = Path(DATA_DIR, MERGED_FILE_CSV)

REGIONS = ["Вінницька область", "Волинська область", "Дніпропетровська область"]
TYPES_OF_COUNCILS = ["Міські"]
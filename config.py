from pathlib import Path

DATA_DIR = "data"
ALL_CANDIDATES_RAW_FILE_CSV = "01_01_all_candidates.csv"
ELECTED_CANDIDATES_RAW_FILE_CSV = "01_02_elected_candidates.csv"
MERGED_FILE_CSV = "02_01_merged_candidates.csv"
AGGREGATED_FILE_CSV = "03_01_aggregated_data.csv"

CANDIDATES_RAW_FILE_CSV_PATH = {
    "all": Path(DATA_DIR, ALL_CANDIDATES_RAW_FILE_CSV),
    "elected": Path(DATA_DIR, ELECTED_CANDIDATES_RAW_FILE_CSV),
}
MERGED_FILE_CSV_PATH = Path(DATA_DIR, MERGED_FILE_CSV)
AGGREGATED_FILE_CSV_PATH = Path(DATA_DIR, AGGREGATED_FILE_CSV)

REGIONS = ["Вінницька область", "Волинська область", "Дніпропетровська область"]
TYPES_OF_COUNCILS = ["Міські"]
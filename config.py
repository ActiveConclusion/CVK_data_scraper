from pathlib import Path

# директорія для збереження даних
DATA_DIR = "data"
# назва файлу даних про висунутих кандидатів
ALL_CANDIDATES_RAW_FILE_CSV = "01_01_all_candidates.csv"
# назва файлу даних про обраних кандидатів
ELECTED_CANDIDATES_RAW_FILE_CSV = "01_02_elected_candidates.csv"
# назва файлу зведених даних про обраних та висунутих кандидатів
MERGED_FILE_CSV = "02_01_merged_candidates.csv"
# назва файлу даних про висунутих і обраних кандидатів по партіям, регіонам та радам
AGGREGATED_FILE_CSV = "03_01_aggregated_data.csv"

CANDIDATES_RAW_FILE_CSV_PATH = {
    "all": Path(DATA_DIR, ALL_CANDIDATES_RAW_FILE_CSV),
    "elected": Path(DATA_DIR, ELECTED_CANDIDATES_RAW_FILE_CSV),
}
MERGED_FILE_CSV_PATH = Path(DATA_DIR, MERGED_FILE_CSV)
AGGREGATED_FILE_CSV_PATH = Path(DATA_DIR, AGGREGATED_FILE_CSV)

# Регіони для опрацювання.
# Якщо поставити значення None, то будуть опрацьовані всі можливі регіони
REGIONS = ["Вінницька область", "Волинська область", "Дніпропетровська область"]
# Типи рад для опрацювання.
# Можливі опції: "Обласні", "Міські", "Районні", "Районні у містах"
TYPES_OF_COUNCILS = ["Міські"]
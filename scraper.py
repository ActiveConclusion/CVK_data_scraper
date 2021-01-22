from CVK_scraper import *
from config import *


def run():
    # get candidates info for specified regions and types of councils
    candidates_data = get_candidates_info(
        category="candidates",
        regions=REGIONS,
        types_of_councils=TYPES_OF_COUNCILS,
    )
    # get elected people info for specified regions and types of councils
    elected_data = get_candidates_info(
        category="elected",
        regions=REGIONS,
        types_of_councils=TYPES_OF_COUNCILS,
    )
    # write DataFrame to specified CSV file
    candidates_data.to_csv(CANDIDATES_RAW_FILE_CSV_PATH, index=False)
    elected_data.to_csv(ELECTED_RAW_FILE_CSV_PATH, index=False)


if __name__ == "__main__":
    run()

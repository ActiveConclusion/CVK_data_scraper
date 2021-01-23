from CVK_scraper import *
from config import *


def run():
    # get candidates info for specified regions and types of councils
    all_candidates_data = get_candidates_info(
        category="all",
        regions=REGIONS,
        types_of_councils=TYPES_OF_COUNCILS,
    )
    # get elected people info for specified regions and types of councils
    elected_candidates_data = get_candidates_info(
        category="elected",
        regions=REGIONS,
        types_of_councils=TYPES_OF_COUNCILS,
    )

    # merge candidates data
    merged_candidates_data = merge_candidates_info(
        all_candidates_data, elected_candidates_data
    )
    # write DataFrames to CSV files
    all_candidates_data.to_csv(CANDIDATES_RAW_FILE_CSV_PATH, index=False)
    elected_candidates_data.to_csv(ELECTED_RAW_FILE_CSV_PATH, index=False)
    merged_candidates_data.to_csv(MERGED_FILE_CSV_PATH, index=False)


if __name__ == "__main__":
    run()

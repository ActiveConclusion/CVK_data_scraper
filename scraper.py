from CVK_scraper import *
from config import *

import click


@click.group(help="Local election data scraper")
def cli():
    pass


@cli.command(help="Scrape data about candidates")
@click.option("--verbose", is_flag=True, help="Will print process messages")
@click.argument(
    "categories",
    nargs=-1,
)
def scrape(verbose, categories):
    """Scrape data about candidates

    Args:
        verbose (bool): will print process messages
        categories (list): Сategories of candidates to scrape. Possible options: "all", "elected".

    Returns:
        dict: dict of DataFrames with scraped data. Key is category of candidates
    """
    # define an ad-hoc print function for verbose option
    verboseprint = print if verbose else lambda *a, **k: None
    # define all possible categories
    all_categories = ("all", "elected")
    # init return dictionary
    candidates_data = {}
    # if no categories are provided or they provided incorrectly, scrape data for all categories
    if len(categories) == 0 or (
        "all" not in categories and "elected" not in categories
    ):
        categories = all_categories
    for category in categories:
        if category in all_categories:
            verboseprint("Scraping data about {} candidates".format(category))
            candidates_data[category] = get_candidates_info(
                category=category,
                regions=REGIONS,
                types_of_councils=TYPES_OF_COUNCILS,
            )
            verboseprint("Data successfully scraped! Writing data...")
            # write DataFrame to CSV file
            candidates_data[category].to_csv(
                CANDIDATES_RAW_FILE_CSV_PATH[category], index=False
            )
            verboseprint("Data successfully written.")
    return candidates_data


@cli.command(help="Merge data of all and elected candidates")
@click.option("--verbose", is_flag=True, help="Will print process messages")
def merge(verbose, candidates_data=None):
    """Merge data of all and elected candidates

    Args:
        verbose (bool): will print process messages
        candidates_data (dict, optional): dict of DataFrames with scraped data where Key is category of candidates.
        Defaults to None.

    Returns:
        DataFrame: merged data of all and elected candidates
    """
    # define an ad-hoc print function for verbose option
    verboseprint = print if verbose else lambda *a, **k: None
    # if DataFrame isn't provided, read data from files
    if candidates_data is None:
        verboseprint("Reading data from files...")
        candidates_data = {}
        candidates_data["all"] = pd.read_csv(
            CANDIDATES_RAW_FILE_CSV_PATH["all"], low_memory=False
        )
        candidates_data["elected"] = pd.read_csv(
            CANDIDATES_RAW_FILE_CSV_PATH["elected"], low_memory=False
        )
    verboseprint("Merging data...")
    # merge candidates data
    merged_candidates_data = merge_candidates_info(
        candidates_data["all"], candidates_data["elected"]
    )
    verboseprint("Data succesfully merged! Writing merged data...")
    # write DataFrame to CSV file
    merged_candidates_data.to_csv(MERGED_FILE_CSV_PATH, index=False)
    verboseprint("Data successfully written.")
    return merged_candidates_data


@cli.command(help="Aggregate data about candidates")
@click.option("--verbose", is_flag=True, help="Will print process messages")
def aggregate(verbose, merged_candidates_data=None):
    """Aggregate candidates info data by party, region and council

    Args:
        verbose (bool): will print process messages
        merged_candidates_data (DataFrame, optional): merged data of all and elected candidates.
        Defaults to None.

    Returns:
        DataFrame: aggregated data
    """
    # define an ad-hoc print function for verbose option
    verboseprint = print if verbose else lambda *a, **k: None
    # if DataFrame isn't provided, read data from files
    if merged_candidates_data is None:
        verboseprint("Reading data from files...")
        merged_candidates_data = pd.read_csv(MERGED_FILE_CSV_PATH, low_memory=False)
    # aggregate data
    verboseprint("Data aggregating")
    aggregated_data = aggregate_by_party_region_council(merged_candidates_data)
    verboseprint("Writing aggregated data...")
    # write DataFrame to CSV file
    aggregated_data.to_csv(AGGREGATED_FILE_CSV_PATH, index=False)
    verboseprint("Data successfully written.")
    return aggregated_data


@cli.command(help="Run full pipeline")
@click.option("--verbose", is_flag=True, help="Will print process messages")
@click.pass_context
def run_all(ctx, verbose):
    """Scrape, merge and aggregate candidates info data

    Args:
        ctx: helper argument for CLI
        verbose (bool): will print process messages
    """
    candidates_data = ctx.forward(scrape)
    merged_candidates_data = ctx.invoke(
        merge, verbose=verbose, candidates_data=candidates_data
    )
    ctx.invoke(
        aggregate, verbose=verbose, merged_candidates_data=merged_candidates_data
    )


if __name__ == "__main__":
    cli()

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
    verboseprint = print if verbose else lambda *a, **k: None
    candidates_data = {}
    # if no categories are provided or they provided incorrectly, scrape data for all categories
    if len(categories) == 0 or (
        "all" not in categories and "elected" not in categories
    ):
        categories = ("all", "elected")
    if "all" in categories:
        # get all candidates info for specified regions and types of councils
        verboseprint("Scraping data about all candidates")
        all_candidates_data = get_candidates_info(
            category="all",
            regions=REGIONS,
            types_of_councils=TYPES_OF_COUNCILS,
        )
        verboseprint("Data successfully scraped! Writing data...")
        all_candidates_data.to_csv(CANDIDATES_RAW_FILE_CSV_PATH, index=False)
        verboseprint("Data successfully written.")
        candidates_data["all"] = all_candidates_data
    if "elected" in categories:
        # get elected candidates info for specified regions and types of councils
        verboseprint("Scraping data about elected candidates")
        elected_candidates_data = get_candidates_info(
            category="elected",
            regions=REGIONS,
            types_of_councils=TYPES_OF_COUNCILS,
        )
        verboseprint("Data successfully scraped! Writing data...")
        elected_candidates_data.to_csv(ELECTED_RAW_FILE_CSV_PATH, index=False)
        verboseprint("Data successfully written.")
        candidates_data["elected"] = elected_candidates_data
    return candidates_data


@cli.command(help="Merge data of all and elected candidates")
@click.option("--verbose", is_flag=True, help="Will print process messages")
def merge(verbose, candidates_data=None):
    verboseprint = print if verbose else lambda *a, **k: None
    if candidates_data is None:
        verboseprint("Reading data from files...")
        candidates_data = {}
        candidates_data["all"] = pd.read_csv(
            CANDIDATES_RAW_FILE_CSV_PATH, low_memory=False
        )
        candidates_data["elected"] = pd.read_csv(
            ELECTED_RAW_FILE_CSV_PATH, low_memory=False
        )
    verboseprint("Merging data...")
    # merge candidates data
    merged_candidates_data = merge_candidates_info(
        candidates_data["all"], candidates_data["elected"]
    )
    verboseprint("Data succesfully merged! Writing merged data...")
    merged_candidates_data.to_csv(MERGED_FILE_CSV_PATH, index=False)
    verboseprint("Data successfully written.")
    return merged_candidates_data


@cli.command(help="Aggregate data about candidates")
@click.option("--verbose", is_flag=True, help="Will print process messages")
def aggregate(verbose, merged_candidates_data=None):
    verboseprint = print if verbose else lambda *a, **k: None
    if merged_candidates_data is None:
        verboseprint("Reading data from files...")
        merged_candidates_data = pd.read_csv(MERGED_FILE_CSV_PATH, low_memory=False)
    # aggregate data
    verboseprint("Data aggregating")
    aggregated_data = aggregate_by_party_region_council(merged_candidates_data)
    verboseprint("Writing aggregated data...")
    aggregated_data.to_csv(AGGREGATED_FILE_CSV_PATH, index=False)
    verboseprint("Data successfully written.")
    return aggregated_data


@cli.command(help="Run full pipeline")
@click.option("--verbose", is_flag=True, help="Will print process messages")
@click.pass_context
def run_all(ctx, verbose):
    candidates_data = ctx.forward(scrape)
    merged_candidates_data = ctx.invoke(
        merge, verbose=verbose, candidates_data=candidates_data
    )
    ctx.invoke(
        aggregate, verbose=verbose, merged_candidates_data=merged_candidates_data
    )


if __name__ == "__main__":
    cli()

import requests
from bs4 import BeautifulSoup
import pandas as pd

CVK_BASE_URL = "https://www.cvk.gov.ua/pls/vm2020/"
REGIONS_PATH = {
    "all": "pvm008pt001f01=695pt00_t001f01=695.html",
    "elected": "pvm002pt001f01=695pt00_t001f01=695.html",
}


def _get_regional_council_paths(URL, category):
    """Get link paths for each type of council for each region.

    Args:
        URL (str): link to a page with a table with a breakdown by region and type of a council
        category (str): category of candidates. Possible options: "all", "elected".

    Raises:
        ValueError: invalid category provided

    Returns:
        dict: a dict where keys are regions and values are nested dictionary with a corresponding type of council and link path.
        Example:
            {
        "Вінницька область": {
            "Обласні": "pvm035pt001f01=695pt00_t001f01=695pid112=12pid100=5rej=0.html",
            "Міські": "pvm035pt001f01=695pt00_t001f01=695pid112=31pid100=5rej=0.html",
            "Районні": "pvm035pt001f01=695pt00_t001f01=695pid112=21pid100=5rej=0.html",
            "Районні у містах": None,
            "Сільські, селищні": "pvm035pt001f01=695pt00_t001f01=695pid112=61pid100=5rej=0.html",
        },
        "Волинська область": ...

    """
    # retrieve the source page
    page = requests.get(URL)
    # parse the page code
    soup = BeautifulSoup(page.content, "lxml")
    # extract the table of interest
    table = soup.find_all("table", {"class": "t2"})[1]
    # get rows
    rows = table.find_all("tr")
    # get headers
    col_names = [td.get_text() for td in rows[0].find_all("td")]
    # some replacements in headers
    if category == "all":
        col_names[2] = "Міські"
    elif category == "elected":
        col_names = list(map(lambda x: x.replace(" ради", ""), col_names))
    else:
        raise ValueError("Некоректна категорія")
    # scrape data from the table
    # init output dictionary
    regional_council_paths = {}
    # start from the third row (first 2 are headers) to the end before the total row
    for row in rows[2:-1]:
        cols = row.find_all("td")
        # get region name
        region = cols[0].get_text()
        # init path list for region
        path_list = []
        start_col = 1 if category == "all" else 2
        # iterate over columns in a row where paths can be located
        for col in cols[start_col::2]:
            # get path if it exists
            a_tag = col.find("a")
            path = None
            if a_tag:
                path = a_tag["href"] if a_tag.has_attr("href") else None
            path_list.append(path)
        # add dictionary of paths for each type of council
        regional_council_paths[region] = dict(zip(col_names[1:-1], path_list[:-1]))
    return regional_council_paths


def _get_council_paths(URL, category):
    """Get link paths for each council

    Args:
        URL (str): link to a page with a table with councils
        category (str): category of candidates. Possible options: "all", "elected".

    Returns:
        dict: a dict where keys are regions and values are paths link
        Example:
            {
        "Барська міська рада": "pvm056pid102=12644pf7691=64740pt001f01=695rej=0pt00_t001f01=695.html",
        "Бершадська міська рада": "pvm056pid102=6499pf7691=63705pt001f01=695rej=0pt00_t001f01=695.html",
        "Вінницька міська рада": ...,
        }

    """
    # retrieve the source page
    page = requests.get(URL)
    # parse the page code
    soup = BeautifulSoup(page.content, "lxml")
    # extract the table of interest
    table = soup.find("table", {"class": "t2"})
    # get rows
    rows = table.find_all("tr")
    # scrape data from the table
    # init output dictionary
    council_paths = {}
    for row in rows[1:]:
        col = row.find("td")
        a_tag = col.find("a")
        # get council name
        council_name = a_tag.get_text()
        # remove region part from a name if it's a section for elected
        if category == "elected":
            council_name = [x.strip() for x in council_name.split(",")][1]
        # get path if it exists
        path = a_tag["href"] if a_tag.has_attr("href") else None
        # match path for the corresponding council
        council_paths[council_name] = path
    return council_paths


def _get_council_people_data(URL):
    """Get personal data about candidates or elected people for a council

    Args:
        URL (str): link to a page with a table with candidates or elected people for council

    Returns:
        DataFrame: DataFrame with scraped data
    """
    # retrieve the source page
    page = requests.get(URL)
    # parse the page code
    soup = BeautifulSoup(page.content, "lxml")
    # get all tables
    tables = soup.find_all("table", {"class": "t2"})
    # edge case when a page is empty
    if len(tables) == 0:
        return pd.DataFrame()
    # extract the table of interest
    table = tables[-1]
    # get rows
    rows = table.find_all("tr")
    # get headers
    col_names = ["Партія"] + [td.get_text() for td in rows[0].find_all("td")]
    # scrape data from the table
    data = []
    party = None
    for row in rows[1:]:
        cols = row.find_all("td")
        # scrape party line
        if len(cols) == 1:
            party = cols[0].find("b").get_text()
        else:
            # scrape personal info
            person_info = [party] + [
                ele.get_text(separator=" ").strip() for ele in cols
            ]
            data.append(person_info)
    # convert to DataFrame
    people_data = pd.DataFrame(data, columns=col_names)
    # if there are no separate lines with parties, they are contained in personal info
    if party is None:
        people_data.drop(columns="Партія", inplace=True)
    return people_data


def get_candidates_info(category="all", regions=None, types_of_councils=None):
    """Get info about all or elected candidates for specified regions and types of councils

    Args:
        category (str, optional): category of candidates. Possible options: "all", "elected". Defaults to "all".
        regions (list, optional): list of regions. If provided None, all regions will be scraped. Defaults to None.
        types_of_councils (list, optional): list of types of councils. If provided None, all types of councils will be scraped.
        Defaults to None.

    Raises:
        ValueError: invalid category provided

    Returns:
        DataFrame: scraped DataFrame with candidates info
    """
    # check that the category is correct
    if category != "all" and category != "elected":
        raise ValueError("Некоректна категорія")
    # get all link paths for provided category
    regional_council_paths = _get_regional_council_paths(
        CVK_BASE_URL + REGIONS_PATH[category], category
    )
    # get all available regions
    all_regions = list(regional_council_paths.keys())
    # if regions argument is empty, scrape all regions
    if regions is None:
        regions = all_regions
    # if there are no types of councils, scrape all
    # TO DO: add support for 'сільскі' та 'селищні'
    if types_of_councils is None:
        types_of_councils = list(regional_council_paths[all_regions[0]].keys())
    # init final DataFrame
    candidates_full = pd.DataFrame()
    # scrape data for each region
    for region in regions:
        # init DataFrame for region
        candidates_region = pd.DataFrame()
        # scrape data for each provided council
        for type_of_council in types_of_councils:
            # get link path for corresponding region and type of council
            regional_councils_path = regional_council_paths[region][type_of_council]
            # if path exist, get all council paths
            if regional_councils_path:
                councils_paths = _get_council_paths(
                    CVK_BASE_URL + regional_councils_path, category
                )
                # scrape candidates info for each council
                for council, path in councils_paths.items():
                    candidates = _get_council_people_data(CVK_BASE_URL + path)
                    # rename some columns
                    candidates.rename(
                        columns={
                            "№ ОВО": "ТВО/ОВО",
                            "№ ТВО, за яким закріплено": "ТВО/ОВО",
                            "Прізвище, ім'я, по батькові": "Прізвище, ім’я, по батькові",
                            "Висування": "Партія",
                            "% від квоти": "% голосів від квоти",
                        },
                        inplace=True,
                    )
                    # add column "Рада" і "Тип ради"
                    candidates.insert(0, "Рада", council)
                    candidates.insert(1, "Тип ради", type_of_council)
                    # append to regional DataFrame
                    candidates_region = candidates_region.append(candidates)
        # add region column
        candidates_region.insert(0, "Регіон", region)
        # append to full DataFrame
        candidates_full = candidates_full.append(candidates_region)
    # change comma delimeter to decimal point
    candidates_full["% голосів від квоти"] = candidates_full[
        "% голосів від квоти"
    ].str.replace(",", ".")
    # convert columns to numeric type where possible
    candidates_full = candidates_full.apply(pd.to_numeric, errors="ignore")
    return candidates_full
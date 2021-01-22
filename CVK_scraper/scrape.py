import requests
from bs4 import BeautifulSoup
import pandas as pd

CVK_BASE_URL = "https://www.cvk.gov.ua/pls/vm2020/"
CANDIDATES_REGIONS_PATH = "pvm008pt001f01=695pt00_t001f01=695.html"


def get_regional_councils_paths(URL, category):
    """Get link paths for each type of council for each region.

    Args:
        URL (str): link to a page with a table with a breakdown by region and type of a council
        category (str): category of candidates. Possible options: "candidates", "elected".

    Raises:
        ValueError: invalid category provided

    Returns:
        dict: a dict where keys are regions and values are nested dictionary with a corresponding type of council and link path.
        Example of return:
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
    if category == "candidates":
        col_names[2] = "Міські"
    elif category == "elected":
        col_names = list(map(lambda x: x.replace(" ради", ""), col_names))
    else:
        raise ValueError("Некоректна категорія")
    # scrape data from the table
    # init output dictionary
    regional_councils_paths = {}
    # start from the third row (first 2 are headers) to the end before the total row
    for row in rows[2:-1]:
        cols = row.find_all("td")
        # get region name
        region = cols[0].get_text()
        # init path list for region
        path_list = []
        start_col = 1 if category == "candidates" else 2
        # iterate over columns in a row where paths can be located
        for col in cols[start_col::2]:
            # get path if it exists
            a_tag = col.find("a")
            path = None
            if a_tag:
                path = a_tag["href"] if a_tag.has_attr("href") else None
            path_list.append(path)
        # add dictionary of paths for each type of council
        regional_councils_paths[region] = dict(zip(col_names[1:-1], path_list[:-1]))
    return regional_councils_paths


regional_councils_paths = get_regional_councils_paths(
    CVK_BASE_URL + CANDIDATES_REGIONS_PATH, "candidates"
)
print(regional_councils_paths)

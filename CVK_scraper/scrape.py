import requests
from bs4 import BeautifulSoup
import pandas as pd

CVK_BASE_URL = "https://www.cvk.gov.ua/pls/vm2020/"
CANDIDATES_REGIONS_PATH = "pvm008pt001f01=695pt00_t001f01=695.html"


def get_regional_council_paths(URL, category):
    """Get link paths for each type of council for each region.

    Args:
        URL (str): link to a page with a table with a breakdown by region and type of a council
        category (str): category of candidates. Possible options: "candidates", "elected".

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
    if category == "candidates":
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
        regional_council_paths[region] = dict(zip(col_names[1:-1], path_list[:-1]))
    return regional_council_paths


def get_council_paths(URL, category):
    """Get link paths for each council

    Args:
        URL (str): link to a page with a table with councils
        category (str): category of candidates. Possible options: "candidates", "elected".

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


regional_council_paths = get_regional_council_paths(
    CVK_BASE_URL + CANDIDATES_REGIONS_PATH, "candidates"
)
# print(regional_councils_paths)
vinnytsya_city_councils_path = regional_council_paths["Вінницька область"]["Міські"]
vinnytsya_city_council_paths = get_council_paths(
    CVK_BASE_URL + vinnytsya_city_councils_path, "candidates"
)
print(vinnytsya_city_council_paths)

d = {
    "Барська міська рада": "pvm056pid102=12644pf7691=64740pt001f01=695rej=0pt00_t001f01=695.html",
    "Бершадська міська рада": "pvm056pid102=6499pf7691=63705pt001f01=695rej=0pt00_t001f01=695.html",
    "Вінницька міська рада": "pvm056pid102=7199pf7691=65096pt001f01=695rej=0pt00_t001f01=695.html",
}

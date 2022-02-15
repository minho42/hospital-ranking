import json
import os
from typing import Tuple, Union

import xlrd
# https://stackoverflow.com/questions/64264563/attributeerror-elementtree-object-has-no-attribute-getiterator-when-trying
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

RAW_DATA_FILE = "all_hospitals.xlsx"
EXTRACTED_DATA_FILE = "all_hospitals.json"
RATING_FILE = "rating.json"
RANKING_FILE = "./frontend/ranking.json"
WEBDRIVER_TIMEOUT_SECOND = 5
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")


def get_chromedriver(headless: bool = True) -> object:
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    if headless:
        options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_experimental_option("prefs", prefs)

    try:
        driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    except WebDriverException as e:
        driver = None

    return driver


def extract_all_hospitals_from_data() -> None:
    print("extract_all_hospitals_from_data()")

    assert RAW_DATA_FILE

    wb = xlrd.open_workbook(RAW_DATA_FILE)
    sh = wb.sheet_by_index(0)
    all_hospitals = []
    for rownum in range(1, sh.nrows):
        row_values = sh.row_values(rownum)
        sector = row_values[0]
        state = row_values[1]
        name = row_values[2]

        all_hospitals.append({"sector": sector, "state": state, "name": name})

    with open(EXTRACTED_DATA_FILE, "w") as file:
        file.write(json.dumps(all_hospitals))


def get_weighted_ranking(R, v, m, C):
    # https://www.quora.com/How-does-IMDbs-rating-system-work
    # IMDB formula, true 'Bayesian estimate'
    # weighted rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
    # R = average for the movie (mean) = (Rating)
    # v = number of votes for the movie = (votes)
    # m = minimum votes required to be listed in the Top 250 (currently 25000)
    # C = the mean vote across the whole report (currently 7.0)
    return (v / (v + m)) * R + (m / (v + m)) * C


def make_weighted_ranking_file():
    print("make_weighted_ranking_file()")

    assert RATING_FILE

    with open(RATING_FILE, "r") as file:
        data = json.load(file)
    total_review_count = 0
    for row in data:
        total_review_count += int(row["reviews"])

    stars_x_reviews = 0
    for row in data:
        stars_x_reviews += float(row["stars"]) * int(row["reviews"])
    average_stars = stars_x_reviews / total_review_count

    new_data = []
    for row in data:
        R = float(row["stars"])
        v = int(row["reviews"])
        m = 1
        C = average_stars
        row["ranking"] = str(get_weighted_ranking(R, v, m, C))
        new_data.append(row)

    with open(RANKING_FILE, "w") as file:
        file.write(json.dumps(new_data))


class GoogleReviewReader:
    def __init__(self):
        self.driver = get_chromedriver(headless=True)
        assert self.driver
        self.base_url = "https://www.google.com.au/search?q="
        self.review_class_name = "Ob2kfd"

    def get(self, name: str, state: str) -> Union[Tuple[str, str], Tuple[None, None]]:

        name_for_url = f"{name}+{state}".replace(" ", "+")
        url = f"{self.base_url}{name_for_url}"

        try:
            self.driver.get(url)
        except TimeoutException:
            return None, None

        try:
            el = WebDriverWait(self.driver, WEBDRIVER_TIMEOUT_SECOND).until(
                # EC.presence_of_element_located((By.ID, "footcnt"))
                EC.presence_of_element_located((By.CLASS_NAME, self.review_class_name))
            )
        except TimeoutException:
            return None, None
        else:
            try:
                reviews = self.driver.find_element_by_class_name(self.review_class_name).text
            except NoSuchElementException:
                return None, None
            else:
                try:
                    stars, reviews = reviews.split("\n")
                except:
                    print(reviews)
                    print(reviews.split("\n"))

                reviews = reviews.split()[0]
                return stars, reviews

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self.driver:
            self.driver.quit()


def scrape_stars_and_reviews() -> None:
    print("scrape_stars_and_reviews()")

    assert EXTRACTED_DATA_FILE

    with open(EXTRACTED_DATA_FILE, "r") as file:
        data = json.load(file)
        new_data = []
        with GoogleReviewReader() as grr:
            for row in data:
                name = row["name"]
                state = row["state"]
                stars, reviews = grr.get(name, state)
                if stars and reviews:
                    print(name, stars, reviews)
                    row["stars"] = stars
                    row["reviews"] = reviews
                    new_data.append(row)

        with open(RATING_FILE, "w") as file:
            file.write(json.dumps(new_data))


if __name__ == "__main__":
    extract_all_hospitals_from_data()
    scrape_stars_and_reviews()
    make_weighted_ranking_file()

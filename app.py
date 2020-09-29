import json
import os
from typing import Tuple, Union

import xlrd
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

RAW_DATA_FILE = "all hospitals.xlsx"
EXTRACTED_DATA_FILE = "all hospitals.json"
RANKING_FILE = "ranking.json"
WEBDRIVER_TIMEOUT_SECOND = 5


def get_chromedriver(headless: bool = True) -> object:
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    if headless:
        options.add_argument("headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "--remote-debugging-port=9222"
        )  # Trying to fix WebDriverException("unknown error: DevToolsActivePort file doesn't exist", None, None)
    options.add_experimental_option("prefs", prefs)

    try:
        driver = webdriver.Chrome(os.environ.get("CHROME_DRIVER_PATH"), options=options)
    except WebDriverException as e:
        driver = None

    return driver


def prep_get_hospitals(filename: str = RAW_DATA_FILE) -> None:
    wb = xlrd.open_workbook(filename)
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


class GoogleReviewReader:
    def __init__(self):
        self.driver = get_chromedriver(headless=True)
        assert self.driver
        self.base_url = "https://www.google.com.au/search?q="
        self.review_class_name = "Ob2kfd"

    def get(self, name: str) -> Union[Tuple[str, str], Tuple[None, None]]:
        name_for_url = name.replace(" ", "+")
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
                reviews = self.driver.find_element_by_class_name(
                    self.review_class_name
                ).text
            except NoSuchElementException:
                return None, None
            else:
                score, count = reviews.split("\n")
                count = count.split()[0]
                return score, count

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    with open(EXTRACTED_DATA_FILE) as file:
        data = json.load(file)
        new_data = []
        with GoogleReviewReader() as grr:
            for row in data:
                name = row["name"]
                score, count = grr.get(name)
                if score and count:
                    print(name, score, count)
                    row["score"] = score
                    row["count"] = count
                    new_data.append(row)

        with open(RANKING_FILE, "w") as file:
            file.write(json.dumps(new_data))


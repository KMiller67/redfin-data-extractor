import glob
import os.path
import requests

import pandas as pd

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class RedfinDataPuller:
    def __init__(self):
        pass

    def pull_data(self, city: str, state: str, delete_csv: bool = False):
        """
        Attempts to download csv of Redfin real estat data using the provided city and state params as search criteria
        :param city: Name of the city to pull data from
        :param state: Name of the state to pull data from; can be full name of the state or abbreviation
        :param delete_csv: When set to True, deletes the CSV file that is downloaded as part of the data pulling process
        :return: Pandas DataFrame containing real estate data from Redfin for the desired city & state
        """
        # Get the location used by the manager and initialize the driver using Chrome
        service = Service(executable_path=ChromeDriverManager().install())

        # Specify options to run in headless mode for efficiency and to allow downloading files while in headless mode
        options = Options()
        options.add_argument("--headless")

        # Specify downloads folder and file type
        home = str(Path.home())
        downloads_dir = home + r"\Downloads"
        file_type = "\*csv"

        # Open Chrome web browser
        driver = webdriver.Chrome(service=service, options=options)

        # Enable Chromium driver to download files while in headless mode
        params = {"behavior": "allow", "downloadPath": downloads_dir}
        driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

        # Navigate to Redfin website
        driver.get("http://www.redfin.com")
        driver.implicitly_wait(1)

        # Identify search bar on home page for entering a real estate search location and search for input city/state
        # Finds first search bar on the home page, which is the one we're looking for
        driver.find_element(By.CLASS_NAME, "search-input-box").send_keys(f"{city}, {state}" + Keys.ENTER)
        driver.implicitly_wait(1)

        # Click the (Download All) link at the bottom of results page to download a CSV with data from all real estate
        # listings for every page of the search results
        wait_secs = 5
        driver.find_element(By.ID, "download-and-save").click()
        driver.implicitly_wait(wait_secs)

        # Experimenting with waiting for href response to return 200 before continuing, signifying download is complete
        # download_url = \
        #     "https://www.redfin.com/stingray/api/gis-csv?al=1&include_pending_homes=true&isRentals=false&market=twincities&num_homes=350&ord=redfin-recommended-asc&page_number=1&region_id=14201&region_type=6&sf=1,2,5,6,7&status=9&uipt=1,2,3,4,5,6,7,8&v=8"
        # print(requests.get())

        # Grab all files in downloads_dir that are CSVs and pick the last one (which was just downloaded)
        csv_files = glob.glob(downloads_dir + file_type)
        latest_file = max(csv_files, key=os.path.getctime)

        re_data = pd.read_csv(latest_file)

        # if delete_csv:
        #     try:
        #         # Grab all files in downloads_dir that are CSVs and pick the last one (which was just downloaded)
        #         csv_files = glob.glob(downloads_dir + file_type)
        #         latest_file = max(csv_files, key=os.path.getctime)
        #
        #         re_data = pd.read_csv(latest_file)
        #
        #     except:

        # Close browser
        driver.quit()

        return re_data

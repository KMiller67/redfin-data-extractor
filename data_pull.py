import os
import glob
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def download_wait(download_path: str, files_in_path: int, timeout: int) -> bool:
    """
    Continually checks the given download path to see if a new file was added, waiting one second between checks
    :param download_path: Path where downloaded file is expected to appear
    :param files_in_path: Number of files in download_path prior to attempting download of real estate data
    :param timeout: Max number of seconds to wait for downloaded file to appear
    :return: If a new CSV was added to the directory then True, otherwise False
    """
    seconds = 0
    while seconds < timeout:
        new_num_files = len(os.listdir(download_path))  # Check number of files in download path after download start
        if new_num_files == files_in_path:
            time.sleep(1)
            seconds += 1
        else:
            break

    if seconds < timeout:   # File was downloaded prior to timeout period
        return True
    else:                   # File was not downloaded before timeout period
        return False


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

        # Define directory where data will be downloaded and file type
        dirname = os.path.abspath(os.path.dirname(__file__))
        download_dir = os.path.join(dirname, "data", "")
        file_type = "*.csv"

        # Open Chrome web browser
        driver = webdriver.Chrome(service=service, options=options)

        # Enable Chromium driver to download files while in headless mode
        params = {"behavior": "allow", "downloadPath": download_dir}
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
        # wait_secs = 5
        old_num_files = len(os.listdir(download_dir))  # Check number of files in download path prior to download
        driver.find_element(By.ID, "download-and-save").click()
        # driver.implicitly_wait(wait_secs)

        try:
            # Wait for data file to finish downloading
            download_wait(download_path=download_dir, files_in_path=old_num_files, timeout=10)

            # Grab all files in downloads_dir that are CSVs and pick the last one (which was just downloaded)
            csv_files = glob.glob(download_dir + file_type)
            latest_file = max(csv_files, key=os.path.getctime)
            re_data = pd.read_csv(latest_file)

            if delete_csv:
                os.remove(latest_file)

            # Close browser
            driver.quit()

            return re_data

        except Exception as e:
            print(e)

            # Close browser
            driver.quit()

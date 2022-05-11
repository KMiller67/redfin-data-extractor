import os
import time
import glob
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait


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

    return seconds < timeout


class DataExtractor:
    def __init__(self, driver: WebDriver, download_directory: str, homepage_url: str = "https://www.redfin.com"):
        self.driver = driver
        self.download_directory = download_directory
        self.homepage_url = homepage_url

    def go_to_homepage(self):
        self.driver.get(self.homepage_url)

    def searchLocation(self, search_criteria: str):
        self.driver.find_element(By.CLASS_NAME, 'search-input-box').send_keys(f'{search_criteria}' + Keys.ENTER)
        time.sleep(1.5)

    def downloadData(self):
        # Click the (Download All) link at the bottom of results page to download a CSV with data from all real estate
        # listings for every page of the search results
        old_num_files = len(os.listdir(self.download_directory))  # Check number of files in download path prior to download
        self.driver.find_element(By.ID, 'download-and-save').click()

        try:
            # Wait for data file to finish downloading
            download_wait(download_path=self.download_directory, files_in_path=old_num_files, timeout=60)

        except Exception as e:
            print(e)

    def readDownloadedData(self, delete_csv: bool):
        # Grab all files in downloads_dir that are CSVs and pick the last one (which was just downloaded)
        file_type = '*.csv'
        csv_files = glob.glob(self.download_directory + file_type)
        try:
            latest_file = max(csv_files, key=os.path.getctime)
            re_data = pd.read_csv(latest_file)

            if delete_csv:
                os.remove(latest_file)

            return re_data

        except ValueError:
            print('No CSV in directory')


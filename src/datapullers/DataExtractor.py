import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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
    def __init__(self, driver: webdriver, download_directory: str, homepage_url: str = 'https://www.redfin.com'):
        self.driver = driver
        self.download_directory = download_directory
        self.homepage_url = homepage_url

    def go_to_homepage(self):
        self.driver.get(self.homepage_url)

    def search_location(self, search_criteria: str):
        self.driver.find_element(By.CLASS_NAME, 'search-input-box').send_keys(f'{search_criteria}' + Keys.ENTER)
        time.sleep(1.5)

    def read_data(self):
        data_url = self.driver.find_element(By.ID, 'download-and-save').get_attribute('href')
        storage_options = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

        return pd.read_csv(data_url, storage_options=storage_options)

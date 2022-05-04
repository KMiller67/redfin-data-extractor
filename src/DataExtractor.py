import os
import time
import glob
import pandas as pd

from selenium import webdriver
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
    def __init__(self, driver: webdriver):
        self.driver = driver

    def searchLocation(self, search_criteria: str):
        self.driver.find_element(By.CLASS_NAME, 'search-input-box').send_keys(f'{search_criteria}' + Keys.ENTER)
        time.sleep(1.5)

    def downloadData(self, download_dir: str, delete_csv: bool):
        # Click the (Download All) link at the bottom of results page to download a CSV with data from all real estate
        # listings for every page of the search results
        old_num_files = len(os.listdir(download_dir))  # Check number of files in download path prior to download
        file_type = '*.csv'
        self.driver.find_element(By.ID, 'download-and-save').click()

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
            self.driver.quit()

            return re_data

        except Exception as e:
            print(e)

            # Close browser
            self.driver.quit()

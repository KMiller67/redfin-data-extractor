import os
import glob
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from typing import Union


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


def home_type_select(home_types: list, driver: webdriver):
    """
    Helper function to select the home type(s) the user desires to pull data for; this function is intended to be used
    AFTER the 'All Filters' dropdown has been clicked
    :param home_types: List of all home types the user desires to pull data for; Options include: house, townhouse,
    condo, land, multi-family, mobile, co-op, and other
    :param driver: Webdriver used for webscraping
    :return: N/A; used only to select desired home types on Redfin website
    """
    # Ensure home types are lowercase
    home_types = map(lambda x: x.lower(), home_types)

    # Dictionary with key being house type and value being the appropriate XPATH from Redfin site
    type_xpaths = {'house': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[1]/div',
                   'townhouse': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[2]/div',
                   'condo': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[3]/div',
                   'land': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[4]/div',
                   'multi-family': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[5]/div',
                   'mobile': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[6]/div',
                   'co-op': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[7]/div',
                   'other': '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[8]/div'}

    # Select desired home types within the Redfin 'All Filters' dropdown
    for type in home_types:
        driver.find_element(By.XPATH, type_xpaths[type]).click()


class RedfinDataPuller:
    def __init__(self):
        pass

    def pull_data(self, search_criteria: str, home_types: Union[str, list], delete_csv: bool = False):
        """
        Attempts to download csv of Redfin real estat data using the provided city and state params as search criteria
        :param search_criteria: Search criteria to be entered into Redfin search bar (city, state, address, etc.)
        :param home_types: Type(s) of home of which to pull data for. Options include: house, townhouse, condo, land,
        multi-family, mobile, co-op, and other. If selecting more than one home type, initialize param as a list
        :param delete_csv: When set to True, deletes the CSV file that is downloaded as part of the data pulling process
        :return: Pandas DataFrame containing real estate data from Redfin for the desired city & state
        """
        # Get the location used by the manager and initialize the driver using Chrome
        service = Service(executable_path=ChromeDriverManager().install())

        # Specify options to run in headless mode for efficiency and to allow downloading files while in headless mode
        options = Options()
        # options.add_argument("--headless")

        # Define directory where data will be downloaded and file type
        dirname = os.path.abspath(os.path.dirname(__file__))
        download_dir = os.path.join(dirname, 'data', '')
        file_type = '*.csv'

        # Open Chrome web browser
        driver = webdriver.Chrome(service=service, options=options)

        # Enable Chromium driver to download files while in headless mode
        params = {'behavior': 'allow', 'downloadPath': download_dir}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

        # Navigate to Redfin website
        driver.get('http://www.redfin.com')
        driver.implicitly_wait(1)

        # Identify search bar on home page for entering a real estate search location and search for input city/state
        # Finds first search bar on the home page, which is the one we're looking for
        driver.find_element(By.CLASS_NAME, 'search-input-box').send_keys(f'{search_criteria}' + Keys.ENTER)
        driver.implicitly_wait(1)

        # Click 'All Filters'; Set to show 'For Sale' listings only by default
        driver.find_element(By.XPATH, '//*[@id="sidepane-header"]/div/div[1]/form/div[5]/div').click()
        # driver.implicitly_wait(1)

        # Select desired 'Home Type'
        home_type_header = driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[5]/div[1]/div/span')
        driver.execute_script("return arguments[0].scrollIntoView();", home_type_header)

        if type(home_types) == str:     # If user selects single home type (string), convert it to a list
            home_types = [home_types]
        home_type_select(home_types=home_types, driver=driver)
        # driver.implicitly_wait(1)

        # Listing status set to both 'Coming Soon' and 'Active' by default; Uncheck 'Coming Soon'
        driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[6]/div[1]/div/div[2]/span[1]/label/span[1]').click()
        # driver.implicitly_wait(1)

        # Set to only include listings from the last 3 days (reduces # of homes to download; need to keep < 350)
        # Typing '3' after selecting dropdown selects the 'Less the 3 days' option
        select = Select(driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[6]/div[2]/div[2]/span/span/select'))
        select.select_by_visible_text('Less than 7 days')
        # driver.implicitly_wait(1)

        # Turn off 'Foreclosures' listing type
        listing_type_header = driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[1]/div/span')
        driver.execute_script('return arguments[0].scrollIntoView()', listing_type_header)

        driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[2]/div/div[1]/div[2]/span/label/span[1]').click()
        # driver.implicitly_wait(1)

        # Close 'All Filters' menu
        driver.find_element(By.XPATH, '//*[@id="right-container"]/div[6]/div/aside/header/button').click()
        # driver.implicitly_wait(1)

        # Click the (Download All) link at the bottom of results page to download a CSV with data from all real estate
        # listings for every page of the search results
        # wait_secs = 5
        old_num_files = len(os.listdir(download_dir))  # Check number of files in download path prior to download
        driver.find_element(By.ID, 'download-and-save').click()
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


re = RedfinDataPuller()

search_criteria = 'Rochester, MN'
home_types = ['house', 'townhouse', 'condo', 'multi-family']
data = re.pull_data(search_criteria=search_criteria, home_types=home_types)

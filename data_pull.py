import pandas as pd

from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from pytz import timezone
from dateutil.relativedelta import relativedelta


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

        # Specify downloads folder
        home = str(Path.home())
        downloads_dir = home + r"\Downloads"

        # Open Chrome web browser
        driver = webdriver.Chrome(service=service, options=options)

        # Enable Chromium driver to download files while in headless mode
        params = {"behavior": "allow", "downloadPath": downloads_dir}
        driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

        # Navigate to Redfin website
        driver.get("http://www.redfin.com")
        driver.implicitly_wait(1)

        # Identify the search bar on the home page for entering a real estate search location and search for Rochester, MN
        # Finds first search bar on the home page, which is the one we're looking for
        driver.find_element(By.CLASS_NAME, "search-input-box").send_keys(f"{city}, {state}" + Keys.ENTER)
        driver.implicitly_wait(1)

        # Click the (Download All) link at the bottom of the results page to download a CSV with data from all real estate
        # listings for every page of the search results
        wait_secs = 3
        driver.find_element(By.ID, "download-and-save").click()
        driver.implicitly_wait(wait_secs)

        # Close browser
        driver.quit()

        # May need to reference PST timezone to grab specific file name of downloaded data; add try/except for
        # delete_csv param
        tz = timezone("US/Pacific")
        now = datetime.now(tz) + relativedelta(seconds=wait_secs)

        # Convert datetime attributes to strings for filename
        cur_year, cur_month, cur_day, cur_hour, cur_min, cur_sec = \
            now.year, now.month, now.day, now.hour, now.minute, now.second

        cur_attributes = [cur_year, cur_month, cur_day, cur_hour, cur_min, cur_sec]
        cur_attr_str = []
        for cur_att in cur_attributes:
            if cur_att < 10:
                cur_att = "".join(["0", str(cur_att)])
            else:
                cur_att = str(cur_att)
            cur_attr_str.append(cur_att)

        # Current mismatch between time on downloaded file name and 'now' variable; NOT CURRENTLY WORKING
        data_filename = f"redfin_{cur_attr_str[0]}-{cur_attr_str[1]}-{cur_attr_str[2]}-{cur_attr_str[3]}-{cur_attr_str[4]}-{cur_attr_str[5]}.csv"
        data_dir = downloads_dir + rf"\{data_filename}"
        re_data = pd.read_csv(data_dir)

        return re_data

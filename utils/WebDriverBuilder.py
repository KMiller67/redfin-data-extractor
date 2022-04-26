from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os


class WebDriverBuilder:
    def __init__(self):
        dirname = os.path.abspath(os.path.dirname(__file__))
        self.download_dir = os.path.join(dirname, 'src/data', '')

    def build(self):
        """
        Sets up a Chrome webdriver and opens up the Redfin website on the home screen; downloaded CSVs are set to
        src/data folder by default
        """
        # Get the location used by the manager and initialize the driver using Chrome
        service = Service(executable_path=ChromeDriverManager().install())

        # Specify options to run in headless mode for efficiency and to allow downloading files while in headless mode
        options = Options().add_argument("--headless")

        # Open Chrome web browser
        driver = webdriver.Chrome(service=service, options=options)

        # Enable Chromium driver to download files while in headless mode
        params = {'behavior': 'allow', 'downloadPath': self.download_dir}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

        # Navigate to Redfin website
        driver.get('http://www.redfin.com')
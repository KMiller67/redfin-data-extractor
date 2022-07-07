import os
from typing import Dict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_default_download_destination():
    # Default directory based on RedfinDataExtractor's needs
    directory_name = os.path.join(os.getcwd(), './src/data', '')
    return os.path.abspath(directory_name)


def get_default_headless_driver_options():
    # Specify options to run in headless mode for efficiency and to allow downloading files while in headless mode
    options = Options()
    options.add_argument('--headless')
    return options


def create_headless_chrome_driver(
        options: Options = None,
        devtools_command_to_params_dict: Dict[str, Dict] = dict) -> webdriver:

    driver = webdriver.Chrome(
        service=Service(executable_path=ChromeDriverManager().install()),
        options=get_default_headless_driver_options() if options is None else options
    )

    for command, command_arguments in devtools_command_to_params_dict.items():
        driver.execute_cdp_cmd(command, command_arguments)

    return driver


class SeleniumWebDriverBuilder:
    def build_default_devtool_commands(self):
        # Enable Chromium driver to download files while in headless mode
        return {'Page.setDownloadBehavior': {'behavior': 'allow', 'downloadPath': self.download_directory}}

    def __init__(self):
        """
        Sets up a Chrome webdriver; downloaded CSVs are set to src/data folder by default
        """
        self.download_directory = get_default_download_destination()
        chrome_devtool_commands = self.build_default_devtool_commands()
        # Open Chrome web browser
        self.driver: webdriver = create_headless_chrome_driver(devtools_command_to_params_dict=chrome_devtool_commands)

    def open_url(self, website_url: str):
        self.driver.get(website_url)

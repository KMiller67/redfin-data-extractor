import time

from selenium.webdriver.chrome import webdriver

from dataloaders.DataExtractor import DataExtractor
from pages.FilterMenu import FilterMenu


class ListingDataExtractor(DataExtractor):
    def __init__(self, driver: webdriver, download_directory: str):
        super().__init__(driver, download_directory)

    def getData(self, search_criteria: str, home_types: list, time_on_redfin: str, delete_csv: bool):
        super().go_to_homepage()
        super().searchLocation(search_criteria)

        filter_menu = FilterMenu(self.driver)
        filter_menu.openMenu()
        filter_menu.selectHomeTypes(home_types)
        filter_menu.selectComingSoonCheckbox()
        filter_menu.selectTimeOnRedfin(time_on_redfin)
        filter_menu.selectForeclosuresCheckbox()
        filter_menu.closeMenu()

        super().downloadData()

        time.sleep(3)
        super().readDownloadedData(delete_csv)

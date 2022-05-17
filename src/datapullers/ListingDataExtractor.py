import time

from selenium import webdriver
from src.datapullers.DataExtractor import DataExtractor
from src.FilterMenu import FilterMenu


class ListingDataExtractor(DataExtractor):
    def __init__(self, driver: webdriver, download_dir: str, dictionary: dict[str, str]):
        super().__init__(driver, download_dir)
        self.dictionary = dictionary

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

        time.sleep(30)
        super().readDownloadedData(delete_csv)

from selenium import webdriver

from DataExtractor import DataExtractor
from FilterMenu import FilterMenu


class ListingDataExtractor(DataExtractor):
    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def getListingData(self, search_criteria: str, home_types: list, time_on_redfin: str):
        super().searchLocation(search_criteria)

        filter_menu = FilterMenu(self.driver)
        filter_menu.openMenu()
        filter_menu.selectHomeTypes(home_types)
        filter_menu.selectComingSoonCheckbox()
        filter_menu.selectTimeOnRedfin(time_on_redfin)
        filter_menu.selectForeclosuresCheckbox()
        filter_menu.closeMenu()

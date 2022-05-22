import time

from selenium import webdriver

from src.datapullers.DataExtractor import DataExtractor
from src.pages.FilterMenu import FilterMenu


class SalesDataExtractor(DataExtractor):
    def __init__(self, driver: webdriver, download_directory: str):
        super().__init__(driver, download_directory)

    def get_data(self, search_criteria: str, home_types: list, sold_within: str, delete_csv: bool):
        super().go_to_homepage()
        super().search_location(search_criteria)

        filter_menu = FilterMenu(self.driver)
        filter_menu.open_menu()
        filter_menu.select_sold_data()
        filter_menu.select_home_types(home_types)
        filter_menu.select_sold_within(sold_within)
        filter_menu.select_foreclosures_checkbox()
        filter_menu.close_menu()

        data = super().read_data()
        return data

from src.utils.SeleniumWebDriverBuilder import SeleniumWebDriverBuilder
from src.datapullers.ListingDataExtractor import ListingDataExtractor
from src.datapullers.SalesDataExtractor import SalesDataExtractor


class RedfinDataExtractor:
    def __init__(self):
        driver_builder = SeleniumWebDriverBuilder()
        self.driver = driver_builder.driver
        download_dir = driver_builder.download_directory
        self.listing_data_extractor = ListingDataExtractor(self.driver, download_dir)
        self.sales_data_extractor = SalesDataExtractor(self.driver, download_dir)

    def get_listing_data(self, search_criteria: str, home_types: list, time_on_redfin: str):
        return self.listing_data_extractor.get_data(search_criteria, home_types, time_on_redfin)

    def get_sales_data(self, search_criteria: str, home_types: list, sold_within: str):
        return self.sales_data_extractor.get_data(search_criteria, home_types, sold_within)

    def close_browser(self):
        self.driver.quit()

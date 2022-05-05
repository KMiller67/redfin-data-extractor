import time

from src.DataExtractor import DataExtractor
from src.FilterMenu import FilterMenu


class ListingDataExtractor(DataExtractor):
    # def __init__(self):
    #     super().__init__(self.driver)

    def getData(self, search_criteria: str, home_types: list, time_on_redfin: str, delete_csv: bool):
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

        self.driver.quit()
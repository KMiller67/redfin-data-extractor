import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait

import Page
from src.data.HomeTypes import HomeTypes


class FilterMenu(Page):
    filter_menu_element_path = '//*[@id="sidepane-header"]/div/div[1]/form/div[5]/div'
    sold_data_element_path = '//*[@id="filterContent"]/div/div[1]/div/div/div/div/div/div/div[3]'
    home_type_header_path = '//*[@id="filterContent"]/div/div[5]/div[1]/div/span'
    coming_soon_checkbox_element_path = '//*[@id="filterContent"]/div/div[6]/div[1]/div/div[2]/span[1]/label/span[1]'
    time_on_redfin_path = '//*[@id="filterContent"]/div/div[6]/div[2]/div[2]/span/span/select'
    listing_type_header_path = '//*[@id="filterContent"]/div/div[10]/div[1]/div/span'
    foreclosures_checkbox_path = '//*[@id="filterContent"]/div/div[10]/div[2]/div/div[1]/div[2]/span/label/span[1]'
    close_menu_button_path = '//*[@id="right-container"]/div[6]/div/aside/header/button'

    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def open_menu(self):
        # Click 'All Filters'; Set to show 'For Sale' listings only by default
        super().click(self.filter_menu_element_path)
        # time.sleep(1.5)

    def select_sold_data(self):
        super().click(self.sold_data_element_path)
        # time.sleep(1.5)

    def home_type_select(self, home_types: list):
        """
        Helper function to select the home type(s) the user desires to pull data for; this function is intended to be used
        AFTER the 'All Filters' dropdown has been clicked
        :param home_types: List of all home types the user desires to pull data for; Options include: house, townhouse,
        condo, land, multi-family, mobile, co-op, and other
        :return: N/A; used only to select desired home types on Redfin website
        """
        # Ensure home types are uppercase and dashes are removed
        home_types = map(lambda x: x.upper().replace('-', ''), home_types)

        # Select desired home types within the Redfin 'All Filters' dropdown
        for home_type in home_types:
            try:
                super().click(HomeTypes[home_type].value)

            except KeyError:
                print(f'Home type {home_type} is not an available filter option. {home_type} not selected.')
                continue

    def select_home_types(self, home_types: list):
        home_type_header = super().find_element(self.home_type_header_path)
        self.driver.execute_script("return arguments[0].scrollIntoView();", home_type_header)   # Find Home Type header
        # time.sleep(1.5)

        if type(home_types) == str:  # If user selects single home type (string), convert it to a list
            home_types = [home_types]
        self.home_type_select(home_types=home_types)
        # time.sleep(1.5)

    def select_coming_soon_checkbox(self):
        # Listing status set to both 'Coming Soon' and 'Active' by default; First click unchecks 'Coming Soon'
        super().click(self.coming_soon_checkbox_element_path)
        # time.sleep(1.5)

    def select_time_on_redfin(self, time_on_redfin_dropdown_option: str):
        # Set to only include listings from the last 7 days (reduces # of homes to download; need to keep < 350)
        select = Select(super().find_element(self.time_on_redfin_path))
        select.select_by_visible_text(time_on_redfin_dropdown_option)   # Enter time_on_redfin as in dropdown; ex. 'Less than 7 days'
        # time.sleep(1.5)

    def select_foreclosures_checkbox(self):
        # Turn off 'Foreclosures' listing type; checked by default
        listing_type_header = super().find_element(self.listing_type_header_path)
        self.driver.execute_script('return arguments[0].scrollIntoView()', listing_type_header)     # Find Listing Type header
        super().click(self.foreclosures_checkbox_path)
        # time.sleep(1.5)

    def close_menu(self):
        super().click(self.close_menu_button_path)
        time.sleep(1.5)

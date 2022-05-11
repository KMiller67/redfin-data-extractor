from src.utils.SeleniumWebDriverBuilder import SeleniumWebDriverBuilder
from dataloaders.ListingDataExtractor import ListingDataExtractor
from dataloaders.SalesDataExtractor import SalesDataExtractor


class RedfinDataExtractor:
    def __init__(self):
        self.driver = SeleniumWebDriverBuilder()
        download_dir = self.driver.download_directory
        self.listing_data_extractor = ListingDataExtractor(self.driver, download_dir)
        self.sales_data_extractor = SalesDataExtractor(self.driver, download_dir)

    def getListingData(self, search_criteria: str, home_types: list, time_on_redfin: str, delete_csv: bool):
        return self.listing_data_extractor.getData(search_criteria, home_types, time_on_redfin, delete_csv)

    def getSalesData(self, search_criteria: str, home_types: list, time_on_redfin: str, delete_csv: bool):
        return self.sales_data_extractor.getData(search_criteria, home_types, time_on_redfin, delete_csv)

    def closeBrowser(self):
        self.driver.quit()



    # def listing_data(self, driver: webdriver, download_dir: str, search_criteria: str, home_types: Union[str, list],
    #                  delete_csv: bool = False):
    #     """
    #     Attempts to download csv of Redfin real estate listing data for a specified search area
    #     :param driver: Webdriver used to connect to Redfin website
    #     :param download_dir: Directory where downloaded CSV files will go
    #     :param search_criteria: Search criteria to be entered into Redfin search bar (city, state, address, etc.)
    #     :param home_types: Type(s) of home of which to pull data for. Options include: house, townhouse, condo, land,
    #     multi-family, mobile, co-op, and other. If selecting more than one home type, initialize param as a list
    #     :param delete_csv: When set to True, deletes the CSV file that is downloaded as part of the data pulling process
    #     :return: Pandas DataFrame containing real estate data from Redfin for the desired city & state
    #     """
    #     # Identify search bar on home page for entering a real estate search location and search for input city/state
    #     # Finds first search bar on the home page, which is the one we're looking for
    #     driver.find_element(By.CLASS_NAME, 'search-input-box').send_keys(f'{search_criteria}' + Keys.ENTER)
    #     time.sleep(1.5)
    #
    #     # Click 'All Filters'; Set to show 'For Sale' listings only by default
    #     driver.find_element(By.XPATH, '//*[@id="sidepane-header"]/div/div[1]/form/div[5]/div').click()
    #     # time.sleep(1.5)
    #
    #     # Select desired 'Home Type'
    #     home_type_header = driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[5]/div[1]/div/span')
    #     driver.execute_script("return arguments[0].scrollIntoView();", home_type_header)
    #     # time.sleep(1.5)
    #
    #     if type(home_types) == str:     # If user selects single home type (string), convert it to a list
    #         home_types = [home_types]
    #     home_type_select(home_types=home_types, driver=driver)
    #     # time.sleep(1.5)
    #
    #     # Listing status set to both 'Coming Soon' and 'Active' by default; Uncheck 'Coming Soon'
    #     driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[6]/div[1]/div/div[2]/span[1]/label/span[1]').click()
    #     # time.sleep(1.5)
    #
    #     # Set to only include listings from the last 7 days (reduces # of homes to download; need to keep < 350)
    #     select = Select(driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[6]/div[2]/div[2]/span/span/select'))
    #     select.select_by_visible_text('Less than 7 days')
    #     # time.sleep(1.5)
    #
    #     # Turn off 'Foreclosures' listing type
    #     listing_type_header = driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[1]/div/span')
    #     driver.execute_script('return arguments[0].scrollIntoView()', listing_type_header)
    #     # time.sleep(1.5)
    #
    #     driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[2]/div/div[1]/div[2]/span/label/span[1]').click()
    #     # time.sleep(1.5)
    #
    #     # Close 'All Filters' menu
    #     driver.find_element(By.XPATH, '//*[@id="right-container"]/div[6]/div/aside/header/button').click()
    #     time.sleep(1.5)
    #
    #     # Click the (Download All) link at the bottom of results page to download a CSV with data from all real estate
    #     # listings for every page of the search results
    #     old_num_files = len(os.listdir(download_dir))  # Check number of files in download path prior to download
    #     file_type = '*.csv'
    #     driver.find_element(By.ID, 'download-and-save').click()
    #
    #     try:
    #         # Wait for data file to finish downloading
    #         download_wait(download_path=download_dir, files_in_path=old_num_files, timeout=10)
    #
    #         # Grab all files in downloads_dir that are CSVs and pick the last one (which was just downloaded)
    #         csv_files = glob.glob(download_dir + file_type)
    #         latest_file = max(csv_files, key=os.path.getctime)
    #         re_data = pd.read_csv(latest_file)
    #
    #         if delete_csv:
    #             os.remove(latest_file)
    #
    #         # Close browser
    #         driver.quit()
    #
    #         return re_data
    #
    #     except Exception as e:
    #         print(e)
    #
    #         # Close browser
    #         driver.quit()
    #
    # def sale_data(self, driver: webdriver, download_dir: str, search_criteria: str, home_types: Union[str, list],
    #               delete_csv: bool = False):
    #     """
    #     Attempts to download csv of Redfin real estate sale data for a specified search area
    #     :param driver: Webdriver used to connect to Redfin website
    #     :param download_dir: Directory where downloaded CSV files will go
    #     :param search_criteria: Search criteria to be entered into Redfin search bar (city, state, address, etc.)
    #     :param home_types: Type(s) of home of which to pull data for. Options include: house, townhouse, condo, land,
    #     multi-family, mobile, co-op, and other. If selecting more than one home type, initialize param as a list
    #     :param delete_csv: When set to True, deletes the CSV file that is downloaded as part of the data pulling process
    #     :return: Pandas DataFrame containing real estate data from Redfin for the desired city & state
    #     """
    #     # Identify search bar on home page for entering a real estate search location and search for input city/state
    #     # Finds first search bar on the home page, which is the one we're looking for
    #     driver.find_element(By.CLASS_NAME, 'search-input-box').send_keys(f'{search_criteria}' + Keys.ENTER)
    #     # time.sleep(1.5)
    #
    #     # Click 'All Filters' and select 'Sold' filter
    #     driver.find_element(By.XPATH, '//*[@id="sidepane-header"]/div/div[1]/form/div[5]/div').click()
    #     driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[1]/div/div/div/div/div/div/div[3]').click()
    #     # time.sleep(1.5)
    #
    #     # Select desired 'Home Type'
    #     home_type_header = driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[5]/div[1]/div/span')
    #     driver.execute_script("return arguments[0].scrollIntoView();", home_type_header)
    #     # time.sleep(1.5)
    #
    #     if type(home_types) == str:     # If user selects single home type (string), convert it to a list
    #         home_types = [home_types]
    #     home_type_select(home_types=home_types, driver=driver)
    #     # time.sleep(1.5)
    #
    #     # Set to only include sales from the last week (reduces # of homes to download; need to keep < 350)
    #     select = Select(driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[6]/div[2]/span/span/select'))
    #     select.select_by_visible_text('Last 1 week')
    #     # time.sleep(1.5)
    #
    #     # Turn off 'Foreclosures' listing type
    #     listing_type_header = driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[1]/div/span')
    #     driver.execute_script('return arguments[0].scrollIntoView()', listing_type_header)
    #     # time.sleep(1.5)
    #
    #     driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[2]/div/div[1]/div[2]/span/label/span[1]').click()
    #     # time.sleep(1.5)
    #
    #     # Close 'All Filters' menu
    #     driver.find_element(By.XPATH, '//*[@id="right-container"]/div[6]/div/aside/header/button').click()
    #     time.sleep(1.5)
    #
    #     # Click the (Download All) link at the bottom of results page to download a CSV with data from all real estate
    #     # listings for every page of the search results
    #     old_num_files = len(os.listdir(download_dir))  # Check number of files in download path prior to download
    #     file_type = '*.csv'
    #     driver.find_element(By.ID, 'download-and-save').click()
    #
    #     try:
    #         # Wait for data file to finish downloading
    #         download_wait(download_path=download_dir, files_in_path=old_num_files, timeout=10)
    #
    #         # Grab all files in downloads_dir that are CSVs and pick the last one (which was just downloaded)
    #         csv_files = glob.glob(download_dir + file_type)
    #         latest_file = max(csv_files, key=os.path.getctime)
    #         re_data = pd.read_csv(latest_file)
    #
    #         if delete_csv:
    #             os.remove(latest_file)
    #
    #         # Close browser
    #         driver.quit()
    #
    #         return re_data
    #
    #     except Exception as e:
    #         print(e)
    #
    #         # Close browser
    #         driver.quit()


re = RedfinDataExtractor()
search_criteria = 'Rochester, MN'
home_types = ['house', 'townhouse', 'dog-house', 'tree-House', 'multi-family']
time_on_redfin = 'Less than 3 days'
delete_csv = False
data = re.getListingData(search_criteria, home_types, time_on_redfin, delete_csv)
re.closeBrowser()

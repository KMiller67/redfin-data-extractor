from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class Page:

    def __init__(self, driver: WebDriver):
        self.web_driver = driver

    def click(self, xpath: str):
        self.find_element(xpath).click()

    def find_element(self, xpath: str):
        return self.web_driver.find_element(By.XPATH, xpath)

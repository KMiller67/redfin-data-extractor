from selenium import webdriver
from selenium.webdriver.common.by import By


class Page:
    def __init__(self, driver: webdriver):
        self.web_driver = driver

    def find_element(self, xpath: str):
        return self.web_driver.find_element(By.XPATH, xpath)

    def click(self, xpath: str):
        self.find_element(xpath).click()

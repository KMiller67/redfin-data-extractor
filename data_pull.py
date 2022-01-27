from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Get the location used by the manager and initialize the driver using Chrome
service = Service(executable_path=ChromeDriverManager().install())
options = Options()
# options.headless = True

# Open Chrome web browser
driver = webdriver.Chrome(service=service, options=options)

# Navigate to Redfin website
driver.get("http://www.redfin.com")
driver.implicitly_wait(0.5)

# Identify the search bar on the home page for entering a real estate search location and search for Rochester, MN
# Finds first search bar on the home page, which is the one we're looking for
driver.find_element(By.CLASS_NAME, "search-input-box").send_keys("Rochester, MN" + Keys.ENTER)
driver.implicitly_wait(0.5)

# Click the (Download All) link at the bottom of the results page to download a CSV with data from all real estate
# listings for every page of the search results
driver.find_element(By.ID, "download-and-save").click()
driver.implicitly_wait(0.5)

# Close browser
driver.quit()

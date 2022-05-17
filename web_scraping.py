import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# load chrome driver
PATH = "/Users/s2124052/Downloads/chromedriver"
driver = webdriver.Chrome(PATH)

# load webpage
driver.get("https://wormguides.org/")
resources_tab = driver.find_element(
    by=By.XPATH, value='//a[@href="'+"https://wormguides.org/resources/"+'"]')
resources_tab.click()

time.sleep(10)

neuron_specific_marker_genes = driver.find_element(
    by=By.XPATH, value='//a[@title="Neuron-Specific Marker Genes"]')

time.sleep(10)
neuron_specific_marker_genes.click()
time.sleep(10)


promoters = driver.find_element(
    by=By.XPATH, value='//a[@href="'+"http://promoters.wormguides.org/"+'"]')
promoters.click()

time.sleep(5)

search = driver.find_element(by=By.NAME, value="q")
search.clear()
search.send_keys("*")
search.send_keys(Keys.RETURN)

try:
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "result_container")))
    expression_detail_links = []
    for element in elements:
        expression_detail = element.find_element(by=By.TAG_NAME, value="span")
        expression_detail_link = expression_detail.get_attribute("href")
        expression_detail_links.append(expression_detail_link)

except:
    driver.quit()

class Scrapper:

    def __init__ (self, driver, address):
        self.address = address
        self.driver = driver
        

    def click(self, element):
        pass

    def next_page():
        pass

    def search():
        pass




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

    def __init__ (self, url, address, PATH):
        self.address = address
        self.url = url
        self.PATH = PATH
        self.driver = webdriver.Chrome(self.PATH)

    def load_webpage(self):
        return self.driver.get(self.url)

    def find_element(self, by=None, value=None):
        try:
            element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_all_elements_located((by, value)))

        except:
            self.driver.quit()

    def generate_element_list(
        self, by=By.CLASS_NAME, value=None, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value)))

        except:
            self.driver.quit()

        return elements

    def extract_elements_from_list(self, list, by=None, value=None, attribute=None, timeout=10):
        links = []
        for element in list:
            try:
                expression_detail = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value)))
                link = expression_detail.get_attribute(attribute)
                links.append(link)

            except:
                self.driver.quit()
            
        return links




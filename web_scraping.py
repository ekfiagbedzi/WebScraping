import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# load chrome driver
PATH = "/Users/s2124052/Downloads/chromedriver"

class Scrapper:

    
    def __init__ (self, url, PATH):
        self.PATH = PATH
        self.url = url
        self.driver = webdriver.Chrome(self.PATH)

    def load_webpage(self):
        self.driver.get(self.url)

    def click(self, by=None, value=None, attribute=None):
        element = self.find_element(by, value, attribute)
        element.click()

    def search(self, input_text="", by=None, value=None):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(input_text)
        element.send_keys(Keys.RETURN)

    def get_element_attribute(self, element, attribute):
        return element.get_attribute(attribute)


    def find_element(self, by=None, value=None, attribute=None, timeout=10):
        if by == By.XPATH:
            value = '//a[@{}="{}"]'.format(attribute, value)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value)))

        except:
            self.driver.quit()

        return element

    def find_elements(self, by=None, value=None, attribute=None, timeout=10):
        if by == By.XPATH:
            value = '//a[@{}="{}"]'.format(attribute, value)
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value)))

        except:
            self.driver.quit()

        return elements

    def extract_elements_from_list(self, list=None, by=None, value=None, attribute=None):
        links = []
        if by == By.XPATH:
            value = '//a[@{}="{}"]'.format(attribute, value)
        for element in list:
            link = element.find_element(by, value).get_attribute(attribute)
            links.append(link)
            
        return links

def scrape_worm_guides():
    worm_scrapper = Scrapper(url="https://wormguides.org/", PATH=PATH)
    worm_scrapper.load_webpage()
    worm_scrapper.click(By.XPATH, "https://wormguides.org/resources/", "href")
    worm_scrapper.click(By.XPATH, "Neuron-Specific Marker Genes", attribute="title")
    worm_scrapper.click(By.XPATH, "http://promoters.wormguides.org/", attribute="href")
    worm_scrapper.search("*", By.NAME, "q")
    lists = worm_scrapper.find_elements(By.CLASS_NAME, "result_container")
    print(lists[0])
    lll = worm_scrapper.extract_elements_from_list(lists, By.TAG_NAME, "span", attribute="href")
    print(lll)

if __name__ == "__main__":
    scrape_worm_guides()
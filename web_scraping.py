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

    def click(self, by=None, value=None):
        element = self.find_element(by, value)
        element.click()

    def search(self, input_text="", by=None, value=None):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(input_text)
        element.send_keys(Keys.RETURN)

    def find_element(self, by=None, value=None):
        try:
            element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((by, value)))

        except:
            self.driver.quit()

        return element

    def find_elements(
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
                member = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value)))
                link = member.get_attribute(attribute)
                links.append(link)

            except:
                self.driver.quit()
            
        return links

if __name__ == "__main__":
    worm_scrapper = Scrapper(url="https://wormguides.org/", PATH=PATH)
    
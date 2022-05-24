# python in-built libraries
import time

import uuid

# selenium functions
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

    def forward(self):
        self.driver.forward()

    def back(self):
        self.driver.back()

    def get_element_attribute(self, element, attribute):
        return element.get_attribute(attribute)

    def get_element_attribute_from_list(self, list, attribute):
        attribute_list = []
        for member in list:
            link = self.get_element_attribute(member, attribute)
            attribute_list.append(link)

        return attribute_list


    def find_element(self, by=None, value=None, attribute=None, timeout=20):
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
            link = element.find_element(by, value)
            links.append(link)
            
        return links

def navigate_to_results_page():
    worm_scrapper = Scrapper(url="https://wormguides.org/", PATH=PATH)
    worm_scrapper.load_webpage()
    worm_scrapper.click(By.XPATH, "https://wormguides.org/resources/", "href")
    worm_scrapper.click(By.XPATH, "Neuron-Specific Marker Genes", attribute="title")
    worm_scrapper.click(By.XPATH, "http://promoters.wormguides.org/", attribute="href")
    worm_scrapper.search("*", By.NAME, "q")
    worm_scrapper.click(By.TAG_NAME, "a")
    
    return worm_scrapper

def get_promoter_preview_info():
    promoter_previews = []
    worm_scrapper = navigate_to_results_page()
    result_bodies = worm_scrapper.find_elements(By.CLASS_NAME, "result_body")
    for detail in result_bodies:
        promoter_previews.append(detail.text)
    return promoter_previews


def get_links_to_all_details_pages():
    worm_scrapper = navigate_to_results_page()
    details_list = worm_scrapper.find_elements(By.TAG_NAME, "span")
    expression_details_list = worm_scrapper.extract_elements_from_list(details_list, By.TAG_NAME, "a")
    expression_details_links = worm_scrapper.get_element_attribute_from_list(expression_details_list, "href")
    unique_ids = []
    uuids = []
    for expression_details_link in expression_details_links:
        unique_ids.append(expression_details_link.split("?pid=")[1])
        uuids.append(str(uuid.uuid4()))
    return expression_details_links, expression_details_list, unique_ids, uuids





if __name__ == "__main__":
    get_promoter_preview_info()
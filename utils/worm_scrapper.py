from utils.scrapper import Scrapper

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WormScrapper(Scrapper):
    @staticmethod
    def get_element_attribute(element, attribute: str) -> object:
        """Find a particular attribute from an element
           Args:
                element (WebElement): Element to be searched
                attribute (str): Attribute to be found from element
           Return:
                Attribute
        """
        return element.get_attribute(attribute) 


    def get_element_attribute_from_list(
        self, list: list, attribute: str) -> list:
        """Find a particular attribute from a list of elements
           Args:
                list (list): List of elements
                attribute (str): Attribute to be found from element
           Return:
                List of attributes
        """
        return [
            self.get_element_attribute(member, attribute) for member in list]
        
    
    def find_element(
        self, by, value : str, attribute=None, timeout=10) -> object:
        """Find elements by tags and/or attributes
           Args:
                by (tag): Element tag
                value: Element
                attribute: attribute of interest of element
                timeout: Wait time to ensure element is found
           Return:
                WebElement
        """
        if by == By.XPATH: # special case for XPATH tags
            value = '//a[@{}="{}"]'.format(attribute, value)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value)))
        except:
            print("Element ERROR!!!")
            self.driver.quit()

        return element


    def find_elements(self, by, value: str, attribute=None, timeout=10) -> list:
        """Find several similar elements by tags and/or attributes
           Args:
                by (tag): Element tag
                value: Element
                attribute: attribute of interest of element
                timeout: Wait time to ensure element is found
           Return:
                List of WebElements
        """
        if by == By.XPATH: # special case for XPATH tags
            value = '//a[@{}="{}"]'.format(attribute, value)
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value)))
        except:
            print("Element ERROR!!!")
            self.driver.quit()

        return elements


    @staticmethod
    def extract_elements_from_list(
        list: list, by, value: str, attribute=None) -> list:
        """Extract elements from a list of elements
           Args:
                list (list): List of WebElements
                by (tag): Element tag
                value (str): Element
                attribute (str): attribute of interest of element
           Return:
                List of WebElements
        """
        if by == By.XPATH: # special case for XPATH tags
            value = '//a[@{}="{}"]'.format(attribute, value)
        
        links = [element.find_element(by, value) for element in list]
        return links
import re
import json
import urllib.request as req

import uuid


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# set path to chrome driver
PATH = "/home/biopythoncodepc/Documents/chromedriver"

class Scrapper:
    """Wraps all essential web _scraping funcitons into a single object

    Parameters:
    ----------
    url: str
        Website to be scrapped
    
    Attributes:
    ----------
    driver: obj
        Webdriver used to connect website to python
    ----------

    Methods:
    ----------
    load_webpage()
        Loads the page associated with the passed url
    switch_driver(PATH)
        Changes current driver to a new value
    click(by, value, attribute)
        Finds and clicks an attribute
    search(input_text, by, value)
        Access a search bar and search for a particular input
    forward()
        Goes to the next cached page
    back()
        Go to the previous cached page
    get_element_attribute(element, attribute)
        Access attribute of a passed element
    get_element_attribute_from_list(list, attribute)
        Get attributes from all elements of a list
    find_element(by, value, attribute, timeout)
        Find an element
    find_elements(by, value, attribute, timeout)
        Find several elements
    extract_elements_from_list(list, by, value, attribute)
        Extract elements from a list of elements
    """

    # web driver
    driver = webdriver.Chrome(PATH)
    
    def __init__ (self, url: str) -> None:
        self.url = url
        

    def load_webpage(self) -> None:
        """Open the website of interest in browser"""
        self.driver.get(self.url)

    @classmethod
    def switch_driver(cls, PATH: str) -> None:
        """Change the current webdriver
           Args:
                PATH (str): File path to the webdriver
           Return:
                None
        """
        cls.driver = webdriver.Chrome(PATH)


    def click(self, by, value: str, attribute: str) -> None:
        """Click a webelement
           Args:
                by (Any): Element tag
                value (str): Element
                attribute (str): Specific attribute of the element
           Return:
                None
        """
        element = self.find_element(by, value, attribute)
        element.click()


    def search(self, input_text: str, by, value: str) -> None:
        """Search for an input
           Args:
                input_text (str): Item to be searched
                by (Any): Search bar tag
                value: Element value
           Return:
                None
        """
        element = self.find_element(by, value)
        element.clear() # clear the search bar field
        element.send_keys(input_text)
        element.send_keys(Keys.RETURN)

    @classmethod
    def forward(cls) -> None:
        """Move to next cached page"""
        cls.driver.forward()

    @classmethod
    def back(cls) -> None:
        """Go back to previous cached page"""
        cls.driver.back()
    
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

    def get_element_attribute_from_list(self, list: list, attribute: str) -> list:
        """Find a particular attribute from a list of elements
           Args:
                list (list): List of elements
                attribute (str): Attribute to be found from element
           Return:
                List of attributes
        """
        return [self.get_element_attribute(member, attribute) for member in list]
        
    
    def find_element(self, by, value : str, attribute=None, timeout=10) -> object:
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
                EC.presence_of_element_located((by, value))) # wait till the element is found

        except:
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
                EC.presence_of_all_elements_located((by, value))) # wait till the element is found


        except:
            self.driver.quit()

        return elements

    @staticmethod
    def extract_elements_from_list(list: list, by, value: str, attribute=None) -> list:
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

    @staticmethod
    def generate_uuids(num_of_ids):
        """Generate unique IDs for each promoter
            Args:
             num_of_ids (int): Number of uuids to generate
            Return:
             uuids (list): List of UUIDS
        """
        return [str(uuid.uuid4()) for i in range(num_of_ids)]

    @staticmethod
    def download_images(image_urls, file_path, uuids):
        """Download associated images of each promoter
           Args:
            image_urls (list): Links to retrieve images
            file_path (str): Path to memory where images should be stored
            uuids (list): List of unique IDs to be assigned to each promoter image
           Return:
            File paths of downloaded images (list)
        """
        index_count = 0
        for url in image_urls:
            req.urlretrieve(url, "{}/{}_{}.gif".format(file_path, uuids[index_count], index_count))
            index_count+=1

        return "{}/{}_{}.gif".format(file_path, uuids[index_count-1], index_count-1)


if __name__ == "__main__":
    

    # navigate to results page
    worm_scrapper = Scrapper(url="https://wormguides.org/")
    worm_scrapper.load_webpage()
    worm_scrapper.click(By.XPATH, "https://wormguides.org/resources/", "href")
    worm_scrapper.click(By.XPATH, "Neuron-Specific Marker Genes", attribute="title")
    worm_scrapper.click(By.XPATH, "http://promoters.wormguides.org/", attribute="href")
    worm_scrapper.search("*", By.NAME, "q")

    # get needed elements on results page
    promoter_previews = worm_scrapper.find_elements(By.CLASS_NAME, "result_body")
    promoter_details_links = worm_scrapper.find_elements(By.TAG_NAME, "span")
    expression_details_elements = worm_scrapper.extract_elements_from_list(promoter_details_links, By.TAG_NAME, "a")
    expression_details_links = worm_scrapper.get_element_attribute_from_list(expression_details_elements, "href")


    # get expression details
    promoters = []
    begining = []
    termination = []
    detailed_expression_patterns = []
    for url in expression_details_links:
        worm_scrapper = Scrapper(url)
        worm_scrapper.load_webpage()
        result_body = worm_scrapper.find_element(By.CLASS_NAME, "result_body")
        info = re.split("Promoter|Temporal\sexpression\spattern|Detailed\sexpression\spatterns|\n", str(result_body.text))
        detailed_expression_patterns.append((re.split("Detailed\sexpression\spatterns", str(result_body.text))[1]).strip(":\n"))
        info_list = [info[i] for i in [2, 7, 9]]
        promoters.append(info_list[0])
        begining.append(info_list[1])
        termination.append(info_list[2])
    

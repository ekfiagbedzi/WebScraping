from utils.worm_scrapper import WormScrapper
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScrapperTestCase(unittest.TestCase):
    
    def test_load_webpage(self): # load correct webpage
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = None
        actual_value = scrapper.load_webpage()
        self.assertEqual(expected_value, actual_value)


    def test_switch_driver(self): # driver has been switched
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = None
        actual_value = scrapper.switch_driver("/home/biopythoncodepc/Documents/chromedriver")
        self.assertEqual(expected_value, actual_value)

    
    def test_click(self): # click a different button
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = None
        scrapper.load_webpage()
        actual_value = scrapper.click(By.XPATH, "https://wormguides.org/technologies/", "href")
        self.assertEqual(expected_value, actual_value)
        

    def test_search(self):
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = None
        scrapper.load_webpage()
        scrapper.click(By.XPATH, "https://wormguides.org/resources/", "href")
        scrapper.click(By.XPATH, "Neuron-Specific Marker Genes", attribute="title")
        scrapper.click(By.XPATH, "http://promoters.wormguides.org/", attribute="href")
        actual_value = scrapper.search("rab-3", By.NAME, "q")

        self.assertEqual(expected_value, actual_value)


    def test_forward(self):
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = None
        scrapper.load_webpage()
        scrapper.click(By.XPATH, "https://wormguides.org/technologies/", "href")
        actual_value = scrapper.forward()
        self.assertEqual(expected_value, actual_value)


    def test_back(self):
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = None
        scrapper.load_webpage()
        scrapper.click(By.XPATH, "https://wormguides.org/technologies/", "href")
        actual_value = scrapper.back()
        self.assertEqual(expected_value, actual_value)

    def test_get_element_attribute(self):
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = str
        scrapper.load_webpage()
        element = scrapper.find_element(By.XPATH, "https://wormguides.org/wormguides-data/", "href")
        actual_value = type(scrapper.get_element_attribute(element, "href"))
        self.assertEqual(expected_value, actual_value)
    
    def test_get_element_attribute_from_list(self):
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = list
        scrapper.load_webpage()
        element = scrapper.find_elements(By.TAG_NAME, "script")
        actual_value = type(scrapper.get_element_attribute_from_list(element, "type"))
        self.assertEqual(expected_value, actual_value)

    def test_generate_uuids(self):
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = 5
        actual_value = len(scrapper.generate_uuids(5))
        self.assertEqual(expected_value, actual_value)

    def test_download_image(self):
        scrapper = WormScrapper("https://wormguides.org/")
        expected_value = "/home/biopythoncodepc/Downloads/0d2fb674-4b6d-420b-a0e7-38c09869e5dd.gif"
        actual_value = scrapper.download_image("http://promoters.wormguides.org/showImage.php?image_id=128", "/home/biopythoncodepc/Downloads/", "0d2fb674-4b6d-420b-a0e7-38c09869e5dd")
        self.assertEqual(expected_value, actual_value)    

"/home/biopythoncodepc/Documents/git_repositories/Data_Collection_Pipeline/raw_data/images/0d2fb674-4b6d-420b-a0e7-38c09869e5dd.gif"
unittest.main(argv=[''], verbosity=2, exit=False)
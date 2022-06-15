from web_scraping import Scrapper
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScrapperTestCase(unittest.TestCase):
    
    def test_load_webpage(self): # load correct webpage
        scrapper = Scrapper("https://wormguides.org/")
        expected_value = None
        actual_value = scrapper.load_webpage()
        self.assertEqual(expected_value, actual_value)


    def test_switch_driver(self): # driver has been switched
        scrapper = Scrapper("https://wormguides.org/")
        expected_value = None
        actual_value = scrapper.switch_driver("/home/biopythoncodepc/Documents/chromedriver")
        self.assertEqual(expected_value, actual_value)

    
    def test_click(self): # click a button
        scrapper = Scrapper("https://wormguides.org/")
        expected_value = None
        scrapper.load_webpage()
        actual_value = scrapper.click(By.XPATH, "https://wormguides.org/technologies/", "href")
        self.assertEqual(expected_value, actual_value)
        

unittest.main(argv=[''], verbosity=1, exit=False)
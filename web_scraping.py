from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# load chrome driver
PATH = "/Users/s2124052/Downloads/chromedriver"
driver = webdriver.Chrome(PATH)

# load webpage
driver.get("http://promoters.wormguides.org/search.php")
search = driver.find_element_by_name("q")
search.send_keys("*")
search.send_keys(Keys.RETURN)

time.sleep(10)

class Scrapper:

    def __init__ (self):
        pass

    def scroll():
        pass

    def next_page():
        pass

    def search():
        pass




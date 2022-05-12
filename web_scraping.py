from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# load chrome driver
PATH = "/Users/s2124052/Downloads/chromedriver"
driver = webdriver.Chrome(PATH)

# load webpage
driver.get("https://wormguides.org/")
resources_tab = driver.find_element_by_xpath('//a[@href="'+"https://wormguides.org/resources/"+'"]')
resources_tab.click()

time.sleep(10)

neuron_specific_marker_genes = driver.find_element_by_xpath('//a[@href="'+"https://wormguides.org/neuron-specific-marker-genes/"+'"]')
time.sleep()
neuron_specific_marker_genes.click()

time.sleep(10)


#search = driver.find_element_by_name("q")
#search.clear()
#search.send_keys("*")
#search.send_keys(Keys.RETURN)

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




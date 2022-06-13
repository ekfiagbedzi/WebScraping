# python in-built libraries
import re
import json
import urllib.request as req

import uuid

# selenium functions
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


    driver = webdriver.Chrome(PATH)
    
    def __init__ (self, url):
        """Initializes """
        self.url = url

    def load_webpage(self):
        self.driver.get(self.url)

    @classmethod
    def switch_driver(cls, PATH):
        cls.driver = webdriver.Chrome(PATH)


    def click(self, by=None, value=None, attribute=None):
        element = self.find_element(by, value, attribute)
        element.click()

    def search(self, input_text="", by=None, value=None):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(input_text)
        element.send_keys(Keys.RETURN)

    @classmethod
    def forward(cls):
        cls.driver.forward()

    @classmethod
    def back(cls):
        cls.driver.back()
    
    @staticmethod
    def get_element_attribute(element, attribute):
        return element.get_attribute(attribute)

    def get_element_attribute_from_list(self, list=None, attribute=None):
        attribute_list = [self.get_element_attribute(member, attribute) for member in list]
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

    @staticmethod
    def extract_elements_from_list(list=None, by=None, value=None, attribute=None):
        if by == By.XPATH:
            value = '//a[@{}="{}"]'.format(attribute, value)
        links = [element.find_element(by, value) for element in list]
        return links

def navigate_to_results_page():
    worm_scrapper = Scrapper(url="https://wormguides.org/")
    worm_scrapper.load_webpage()
    worm_scrapper.click(By.XPATH, "https://wormguides.org/resources/", "href")
    worm_scrapper.click(By.XPATH, "Neuron-Specific Marker Genes", attribute="title")
    worm_scrapper.click(By.XPATH, "http://promoters.wormguides.org/", attribute="href")
    worm_scrapper.search("*", By.NAME, "q")
    
    return worm_scrapper

def get_promoter_preview_info():
    gene_function = []
    spatial_expression_patterns = []
    cellular_expression_patterns = []
    worm_scrapper = navigate_to_results_page()
    result_bodies = worm_scrapper.find_elements(By.CLASS_NAME, "result_body")
    promoter_previews = [detail.text for detail in result_bodies]
    for preview in promoter_previews:
        info = re.split("Gene function:|Temporal\sexpression\spattern:\s|Spatial\sexpression\spatterns:\nGeneral\slocations:|Cellular\sexpression\spattern:", preview)
        gene_function.append(info[1].strip("\n"))
        spatial_expression_patterns.append(info[3].strip("\n"))
        cellular_expression_patterns.append(info[4].strip("\n"))
    return gene_function, spatial_expression_patterns, cellular_expression_patterns

def get_expression_details():
    expression_details_links, _, = get_links_to_all_details_pages()
    expression_details = []
    promoters = []
    begining = []
    termination = []
    detailed_expression_patterns = []
    for url in expression_details_links:
        worm_scrapper = Scrapper(url)
        worm_scrapper.load_webpage()
        result_body = worm_scrapper.find_element(By.CLASS_NAME, "result_body")
        expression_details.append(result_body.text)
    for detail in expression_details:
        info = re.split("Promoter|Temporal\sexpression\spattern|Detailed\sexpression\spatterns|\n", str(detail))
        detailed_expression_patterns.append((re.split("Detailed\sexpression\spatterns", str(detail))[1]).strip(":\n"))
        info_list = [info[i] for i in [2, 7, 9]]
        promoters.append(info_list[0])
        begining.append(info_list[1])
        termination.append(info_list[2])
    return begining, termination, detailed_expression_patterns

def get_strain_info():
    expression_details_links, _, = get_links_to_all_details_pages()
    strain_info = []
    promoter = []
    strain_information = []
    strain_name = []
    date_created = []
    source = []
    reporter = []
    lineage = []
    construct = []
    created_by = []
    construct_info = []
    plasmid_name = []
    gene = []
    transcript = []
    promoter_length = []
    left = []
    forward = []
    right = []
    reverse = []
    vector = []
    expressing_strains = []
    for url in expression_details_links:
        url = url.replace("detailedExpression", "strainInfo")
        worm_scrapper = Scrapper(url)
        worm_scrapper.load_webpage()
        result_body = worm_scrapper.find_element(By.CLASS_NAME, "result_body")
        strain_info.append(result_body.text)
    for info in strain_info:
        string_list = re.split("Promoter:|Strain\sInformation:|Strain\sname:|Date\screated:|Source\sof\sgenotype:|Reporter\sallele:|Lineage\sallele:|Reporter\sconstruct:|Created\sby:|Construct\sInformation:|Plasmid\sname:|Gene:|Transcript:|Promoter\slength:|Left\sprimer:|Forward:|Right\sprimer:\s|Reverse:|Vector:|Integrated, Expressing Strains:|Expression Details", info)
        stripped = [i.strip() for i in string_list]
        promoter.append(stripped[1])
        strain_information.append(stripped[2])
        strain_name.append(stripped[3])
        date_created.append(stripped[4])
        source.append(stripped[5])
        reporter.append(stripped[6])
        lineage.append(stripped[7])
        construct.append(stripped[8])
        created_by.append(stripped[9])
        construct_info.append(stripped[10])
        plasmid_name.append(stripped[11])
        gene.append(stripped[12])
        transcript.append(stripped[13])
        promoter_length.append(stripped[14])
        left.append(stripped[15])
        forward.append(stripped[16])
        right.append(stripped[17])
        reverse.append(stripped[18])
        vector.append(stripped[19])
        expressing_strains.append(stripped[-2])


    return promoter, strain_information, strain_name, date_created, source, reporter, lineage, construct, created_by, construct_info, plasmid_name, gene, transcript, promoter_length, left, forward, right, reverse, vector, expressing_strains

def get_links_to_all_details_pages():
    worm_scrapper = navigate_to_results_page()
    details_list = worm_scrapper.find_elements(By.TAG_NAME, "span")
    expression_details_list = worm_scrapper.extract_elements_from_list(details_list, By.TAG_NAME, "a")
    expression_details_links = worm_scrapper.get_element_attribute_from_list(expression_details_list, "href")
    uuids = [str(uuid.uuid4()) for expression_details_link in expression_details_links]
    return expression_details_links, uuids

def download_images(uuids=None):
    image_urls = []
    index_count = 0
    worm_scrapper = navigate_to_results_page()
    image_tags = worm_scrapper.find_elements(By.TAG_NAME, "img")
    for tag in image_tags:
        image_url = str(tag.get_attribute("src"))
        req.urlretrieve(
            image_url, "/home/biopythoncodepc/Documents/git_repositories/Data_Collection_Pipeline/raw_data/images/{}.gif".format(uuids[index_count]))
        image_urls.append(image_url)
        index_count += 1
    return image_urls





if __name__ == "__main__":
    gene_function, spatial_expression_patterns, cellular_expression_patterns= get_promoter_preview_info()
    begining, termination, detailed_expression_patterns = get_expression_details()
    promoters, strain_information, strain_name, date_created, source, reporter, lineage, construct, created_by, construct_info, plasmid_name, gene, transcript, promoter_length, left, forward, right, reverse, vector, expressing_strains = get_strain_info()
    _, uuids = get_links_to_all_details_pages()
    image_urls = download_images(uuids=uuids)
    data_dict = dict(zip(["uuids", "image_urls"], [uuids, image_urls]))
    data_dict = dict(zip(["uuids", "gene_function", "spatial_expression_patterns", "cellular_expression_patterns", "begining", "termination", "detailed_expression_patterns", "promoters", "strain_information", "strain_name", "date_created", "source", "reporter", "lineage", "construct", "created_by", "construct_info", "plasmid_name", "gene", "transcript", "promoter_length", "left", "forward", "right", "reverse", "vector", "expressing_strains", "image_urls"], [uuids, gene_function, spatial_expression_patterns, cellular_expression_patterns, begining, termination, detailed_expression_patterns, promoters, strain_information, strain_name, date_created, source, reporter, lineage, construct, created_by, construct_info, plasmid_name, gene, transcript, promoter_length, left, forward, right, reverse, vector, expressing_strains, image_urls]))
    
    
    with open("raw_data/data.json", "w") as f:
        json.dump(data_dict, f)    
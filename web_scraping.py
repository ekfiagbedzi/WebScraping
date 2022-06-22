import re
import json
import urllib.request as req
import json

import pandas as pd
import uuid
import boto3
from sqlalchemy import create_engine
import psycopg2


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

    @staticmethod
    def find_element_from_element(parent_element, by, value):
        """Find an element within another element
           Args:
                parent_element (selenium.WebElement): Element
                value: Element tag
           Return:
                selenium.WebElement
        """
        return parent_element.find_element(by, value)

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

    @staticmethod
    def store_data_as_json(data_dict, file_path):
        """Store dictionary data as JSON file
            Args:
                data_dict (dict): dictionary to be convereted to JSON
                file_path (str): Path to file to be dumped in
            Return:
                None
        """
        with open(file_path, "w") as f:
            json.dump(data_dict, f)

    @staticmethod
    def upload_to_s3(path_to_file, bucket_name=None, object_name=None):
        """Upload data to an AWS S3 bucket
           Args:
            path_to_file (str):
                directory of file to upload
            bucket_name (str):
                AWS S3 bucket
            object_name (str):
                Name to associated the file with on AWS S3
           Return:
                None"""
        s3_client = boto3.client("s3")
        response = s3_client.upload_file(path_to_file, bucket_name, object_name)
        return response

    @staticmethod
    def upload_data_to_RDS(DATABASE_TYPE, DBAPI, ENDPOINT, USER, PASSWORD, PORT, DATABASE, path_to_file, table_name):
        """Upload data to AWS RDS
            Args:
                DATABASE_TYPE (str): eg. postgresql, aurora
                DBAPI (str): eg. psycopg
                ENDPOINT (str): localhost or IP address of remote server
                USER (str): Username of server owner
                PASSWORD (str): PASSCODE
                PORT (str): Connection Port default 5432
                DATABASE (str): Database name
                path_to_file (str): Link or Buffer to the file
                table_name (str): Representative name for the table in the database
            Return:
                None
        """
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        engine.connect()
        DATA = pd.read_json(path_to_file)
        DATA.to_sql(table_name, engine, if_exists="replace")



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
    expression_details_links = worm_scrapper.get_element_attribute_from_list(expression_details_elements, "href") # list of links to all expression details pages

    # get promoter information
    gene_function = []
    spatial_expression_patterns = []
    cellular_expression_patterns = []
    for preview in promoter_previews:
        info = re.split("Gene function:|Temporal\sexpression\spattern:\s|Spatial\sexpression\spatterns:\nGeneral\slocations:|Cellular\sexpression\spattern:", preview.text)
        gene_function.append(info[1].strip("\n"))
        spatial_expression_patterns.append(info[3].strip("\n"))
        cellular_expression_patterns.append(info[4].strip("\n"))

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
        info_list = [info[i] for i in [2, 7, 9]] # All parsed required information
        promoters.append(info_list[0]) # promoter names
        begining.append(info_list[1]) # time of expression start
        termination.append(info_list[2]) # time of expression termination

    # get strain information
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
        info_list = re.split("Promoter:|Strain\sInformation:|Strain\sname:|Date\screated:|Source\sof\sgenotype:|Reporter\sallele:|Lineage\sallele:|Reporter\sconstruct:|Created\sby:|Construct\sInformation:|Plasmid\sname:|Gene:|Transcript:|Promoter\slength:|Left\sprimer:|Forward:|Right\sprimer:\s|Reverse:|Vector:|Integrated, Expressing Strains:|Expression Details", str(result_body.text))
        stripped = [i.strip() for i in info_list]
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

    # get image_urls
    image_tags = []
    for element in promoter_previews:
        try:
            image_tags.append(Scrapper.find_element_from_element(element, By.TAG_NAME, "img"))

        except:
            image_tags.append("NA")
            pass
    image_urls = []
    for tag in image_tags:
        try:
            image_urls.append(str(tag.get_attribute("src")))

        except:
            image_urls.append("NA")
            pass

    

    # generate uuids
    uuids = Scrapper.generate_uuids(len(image_urls))

    # download images
    index = -1
    for url in image_urls:
        index+=1
        try:
            Scrapper.download_image(url, "/home/biopythoncodepc/Documents/git_repositories/Data_Collection_Pipeline/raw_data/images", uuids[index])
        except:
            pass

    
    # store data as dictionaries
    promoter_previews_dict = dict(zip(["uuids", "gene_function", "spatial_expression_patterns", "cellular_expression_patterns", "image_urls"], [uuids, gene_function, spatial_expression_patterns, cellular_expression_patterns, image_urls]))
    expression_details = dict(zip(["uuids", "begining", "termination", "detailed_expression_patterns"], [uuids, begining, termination, detailed_expression_patterns]))
    strain_info = dict(zip(["uuids", "promoters", "strain_information", "strain_name", "date_created", "source", "reporter", "lineage", "construct", "created_by", "construct_info", "plasmid_name", "gene", "transcript", "promoter_length", "left", "forward", "right", "reverse", "vector", "expressing_strains"], [uuids, promoters, strain_information, strain_name, date_created, source, reporter, lineage, construct, created_by, construct_info, plasmid_name, gene, transcript, promoter_length, left, forward, right, reverse, vector, expressing_strains]))

    # dump data in json files
    Scrapper.store_data_as_json(promoter_previews_dict, "/home/biopythoncodepc/Documents/git_repositories/Data_Collection_Pipeline/raw_data/json/promoter_previews.json")
    Scrapper.store_data_as_json(expression_details, "/home/biopythoncodepc/Documents/git_repositories/Data_Collection_Pipeline/raw_data/json/expression_details.json")
    Scrapper.store_data_as_json(strain_info, "/home/biopythoncodepc/Documents/git_repositories/Data_Collection_Pipeline/raw_data/json/strain_info.json")
    
    # upload raw data to s3
    Scrapper.upload_to_s3("raw_data/json/expression_details.json", "neuronalpromoters", "expression_details.json")
    Scrapper.upload_to_s3("raw_data/json/expression_details.json", "neuronalpromoters", "promoter_previews.json")
    Scrapper.upload_to_s3("raw_data/json/expression_details.json", "neuronalpromoters", "expression_details.json")

    # upload data to postgresql
    Scrapper.upload_data_to_RDS(
        "postgresql", "psycopg2", "neuronalpromoters.cpjdqvkt7msy.us-east-1.rds.amazonaws.com", "postgres", "Ek2000ek", "5432", "neuronal_promoters", "raw_data/json/expression_details.json", "expression_details")
    Scrapper.upload_data_to_RDS(
        "postgresql", "psycopg2", "neuronalpromoters.cpjdqvkt7msy.us-east-1.rds.amazonaws.com", "postgres", "Ek2000ek", "5432", "neuronal_promoters", "raw_data/json/strain_info.json", "strain_info")
    Scrapper.upload_data_to_RDS(
        "postgresql", "psycopg2", "neuronalpromoters.cpjdqvkt7msy.us-east-1.rds.amazonaws.com", "postgres", "Ek2000ek", "5432", "neuronal_promoters", "raw_data/json/promoter_previews.json", "promoter_previews")

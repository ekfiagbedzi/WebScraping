import json
import urllib.request as req
import json

import pandas as pd
import uuid
import boto3
from sqlalchemy import create_engine

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

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
    """

    # web driver
    
    def __init__ (self, url: str, headless: bool) -> None:
        if headless:
            options = Options()
            options.add_argument("--headless") # run in headless mode
            # ensure default selenium window size is used in headless mode
            options.add_argument("window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)
        
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
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
    def generate_uuids(num_of_ids):
        """Generate unique IDs for each promoter
            Args:
             num_of_ids (int): Number of uuids to generate
            Return:
             uuids (list): List of UUIDS
        """
        return [str(uuid.uuid4()) for i in range(num_of_ids)]


    @staticmethod
    def download_image(image_url, file_path, unique_id):
        """Download associated images of each promoter
           Args:
            image_urls (list): Links to retrieve images
            file_path (str): Path to memory where images should be stored
            uuids (list): List of unique IDs to be assigned to each image
           Return:
            File paths of downloaded images (list)
        """
        
        req.urlretrieve(image_url, "{}{}.gif".format(file_path, unique_id))

        return "{}{}.gif".format(file_path, unique_id)


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
    def upload_data_to_RDS(
        DATABASE_TYPE,
        DBAPI,
        ENDPOINT,
        USER,
        PASSWORD,
        PORT,
        DATABASE,
        path_to_file,
        table_name):
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
        engine = create_engine(
            f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        engine.connect()
        DATA = pd.read_json(path_to_file)
        DATA.to_sql(table_name, engine, if_exists="replace")

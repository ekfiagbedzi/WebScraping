from utils.worm_scrapper import WormScrapper

import re
import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd

from sqlalchemy import create_engine

from selenium.webdriver.common.by import By


# variables for upload to postgresql
DATABASE_TYPE = os.environ["DATABASE_TYPE"]
DBAPI = os.environ["DBAPI"]
ENDPOINT = os.environ["ENDPOINT"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
PORT = os.environ["PORT"]
DATABASE = os.environ["DATABASE"]
BUCKET = os.environ["BUCKET"]


if __name__ == "__main__":
    
    print("Loading web driver")
    # navigate to results page
    worm_scrapper = WormScrapper(url="https://wormguides.org/", headless=True)
    print("Navigating to results page")
    worm_scrapper.load_webpage()
    worm_scrapper.click(
        By.XPATH, "https://wormguides.org/resources/", "href")
    worm_scrapper.click(
        By.XPATH, "Neuron-Specific Marker Genes", attribute="title")
    worm_scrapper.click(
        By.XPATH, "http://promoters.wormguides.org/", attribute="href")
    worm_scrapper.search("*", By.NAME, "q")
    print("Getting promoter preview info")


    # get needed elements on results page
    promoter_previews = worm_scrapper.find_elements(
        By.CLASS_NAME, "result_body")
    print("Getting image urls")


    # get image_urls
    image_tags = []
    for element in promoter_previews:
        try:
            image_tags.append(element.find_element(By.TAG_NAME, "img"))
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
    print("Generating UUIDS")


    # generate uuids
    uuids = WormScrapper.generate_uuids(len(image_urls))
    print("Downloading Images")


    # download images
    index = -1
    for url in image_urls:
        index+=1
        try:
            WormScrapper.download_image(url, "raw_data/images/", uuids[index])
        except ValueError:
            pass
    print("Geting links to all detail pages")


    # get links to details pages
    promoter_details_links = worm_scrapper.find_elements(By.TAG_NAME, "span")
    expression_details_elements = worm_scrapper.extract_elements_from_list(
        promoter_details_links, By.TAG_NAME, "a")
    expression_details_links = worm_scrapper.get_element_attribute_from_list(
        expression_details_elements, "href")
    print("Getting promoter information")


    # get promoter information
    gene_function = []
    spatial_expression_patterns = []
    cellular_expression_patterns = []
    for preview in promoter_previews:
        info = re.split(
            "Gene function:|Temporal\sexpression\spattern:\s|Spatial\sexpression\spatterns:\nGeneral\slocations:|Cellular\sexpression\spattern:",
            preview.text)
        gene_function.append(info[1].strip("\n"))
        spatial_expression_patterns.append(info[3].strip("\n"))
        cellular_expression_patterns.append(info[4].strip("\n"))

    print("Getting expression details")
    # get expression details
    promoters = []
    begining = []
    termination = []
    detailed_expression_patterns = []
    for url in expression_details_links:
        worm_scrapper = WormScrapper(url, True)
        worm_scrapper.load_webpage()
        result_body = worm_scrapper.find_element(By.CLASS_NAME, "result_body")
        info = re.split(
            "Promoter|Temporal\sexpression\spattern|Detailed\sexpression\spatterns|\n", str(result_body.text))
        detailed_expression_patterns.append(
            (re.split(
                "Detailed\sexpression\spatterns",
                str(result_body.text))[1]).strip(":\n"))
        info_list = [info[i] for i in [2, 7, 9]] # All parsed required info
        promoters.append(info_list[0]) # promoter names
        begining.append(info_list[1]) # time of expression start
        termination.append(info_list[2]) # time of expression termination

    print("Getting strain info")
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
        worm_scrapper = WormScrapper(url, True)
        worm_scrapper.load_webpage()
        result_body = worm_scrapper.find_element(By.CLASS_NAME, "result_body")
        info_list = re.split(
            "Promoter:|Strain\sInformation:|Strain\sname:|Date\screated:|Source\sof\sgenotype:|Reporter\sallele:|Lineage\sallele:|Reporter\sconstruct:|Created\sby:|Construct\sInformation:|Plasmid\sname:|Gene:|Transcript:|Promoter\slength:|Left\sprimer:|Forward:|Right\sprimer:\s|Reverse:|Vector:|Integrated, Expressing Strains:|Expression Details", str(result_body.text))
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
    print("Storing data as JSON")
    
    
    # store data as dictionaries
    promoter_previews_dict = dict(
        zip(
            ["uuids", "gene_function", "spatial_expression_patterns", "cellular_expression_patterns", "image_urls"],
            [uuids, gene_function, spatial_expression_patterns, cellular_expression_patterns, image_urls]))
    expression_details = dict(
        zip(
            ["uuids", "begining", "termination", "detailed_expression_patterns"],
            [uuids, begining, termination, detailed_expression_patterns]))
    strain_info = dict(
        zip(
            ["uuids", "promoters", "strain_information", "strain_name", "date_created", "source", "reporter", "lineage", "construct", "created_by", "construct_info", "plasmid_name", "gene", "transcript", "promoter_length", "left", "forward", "right", "reverse", "vector", "expressing_strains"],
            [uuids, promoters, strain_information, strain_name, date_created, source, reporter, lineage, construct, created_by, construct_info, plasmid_name, gene, transcript, promoter_length, left, forward, right, reverse, vector, expressing_strains]))


    # dump data in json files
    WormScrapper.store_data_as_json(
        promoter_previews_dict, "raw_data/json/promoter_previews.json")
    WormScrapper.store_data_as_json(
        expression_details, "raw_data/json/expression_details.json")
    WormScrapper.store_data_as_json(
        strain_info, "raw_data/json/strain_info.json")
    print("Uploading data to RDS database")
    
    
    # upload data to postgresql
    WormScrapper.upload_data_to_RDS(
        DATABASE_TYPE,
        DBAPI,
        ENDPOINT,
        USER,
        PASSWORD,
        PORT,
        DATABASE,
        "raw_data/json/expression_details.json", "expression_details")
    WormScrapper.upload_data_to_RDS(
        DATABASE_TYPE,
        DBAPI,
        ENDPOINT,
        USER,
        PASSWORD,
        PORT,
        DATABASE,
        "raw_data/json/strain_info.json", "strain_info")
    WormScrapper.upload_data_to_RDS(
        DATABASE_TYPE,
        DBAPI,
        ENDPOINT,
        USER,
        PASSWORD,
        PORT,
        DATABASE,
        "raw_data/json/promoter_previews.json", "promoter_previews")


    print("Uploading json data to AWS S3 bucket")
    # upload raw data to s3
    WormScrapper.upload_to_s3(
        "raw_data/json/expression_details.json", BUCKET, "expression_details.json")
    print("Uploading expression_details to S3")
    WormScrapper.upload_to_s3(
        "raw_data/json/promoter_previews.json", BUCKET, "promoter_previews.json")
    print("Uploading promoter_previews to S3")
    WormScrapper.upload_to_s3(
        "raw_data/json/strain_info.json", BUCKET, "strain_info.json")
    print("Uploading strain_info to S3")
    
    print("Uploading images to AWS S3 bucket")
    # upload images to AWS S3 bucket
    image_list = os.listdir("raw_data/images")
    for i in image_list:
        WormScrapper.upload_to_s3(
            "raw_data/images/{}".format(i), "neuronalpromoterimages", i)

    print("Website Scrapped Succesfully!!!")

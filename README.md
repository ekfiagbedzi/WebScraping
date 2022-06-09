# WebScraping
## Overview
This project involves creating a `Scrapper` class that can be used to extract information from websites. It includes methods such as `click`, `search`, `accept_all_cookies` etc. which are normally needed to scrape and navigate a website. 

To demonstrate how to use this class, I will use it scrape data from the website, https://www.wormguides.org. This website contains promoter information for *Caenorhabditis elegans* neurons such as sequence, time of expresson, tissues of expression and images for the expression.

## Enviroment setup
To run this script, use a python environment with the folowing libraries installed;
selenium         4.1.5
Python           3.9.12
uuid             1.30
pandas

## imports
The following libraries and packages were imported


## Code logic
Created a class called `Scrapper` used to scrape data from websites
This class is initialized with the url and path to the driver of your website of interest.
It gives access to methods such as `accept_all_cookies`, `click`, `search`, `forward`, `back`, which are usually needed to navigate webpages. 

Created the following functions to get data;
1. `get_strain_info` to get details such as promoter sequence and strain name
2. `get_expression details` to get temporal and spatial expression patterns of the promoter.
3. `get_image_urls` to get links to each image for each promoter
4. `download_images` to download and save each image associated to each promoter to disk. Each image is given a name corresponding to a uuid.
5. `navigate_to_results_page` to get to search results page


## Use Example for scrapping promoter information on wormguides.org
To scrape all promoter information on wormguides website, run `web_scrapping.py` file in the environment containing the libraries as shown in the **environment setup section**

The scrapper automatilcally acceses each details page of each promoter and gets information such as promoter
name, gene function, temporal and spatial expression details, strain and plasmid details, primers, image urls, and images. It then dumps the data as a json file `data.json` and saves images as `.gif` 


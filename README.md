# WebScraping
## Overview
This project involves creating a `Scrapper` class that can be used to extract information from websites. It includes methods such as `click`, `search`, `accept_all_cookies` etc. which are normally needed to scrape and navigate a website. 

To demonstrate how to use this class, I will use it scrape data from the website, https://www.wormguides.org. This website contains promoter information for *Caenorhabditis elegans* neurons such as sequence, time of expresson, tissues of expression and images for the expression.

## Enviroment setup
To run this script, use a python environment with the folowing libraries installed;
selenium         4.1.5
Python           3.9.12
uuid             1.30
pandas           1.4.2
urllib3          1.26.9

## imports
The following libraries and packages were imported


## Code logic
Created a class called `Scrapper` used to scrape data from websites
This class is initialized with the url and path to the driver of your website of interest.
It gives access to methods such as 

1. `click`: Click button on a website
2. `search`: Search for an item
3. `forward`, `back`, which are usually needed to navigate webpages. 



## Use Example for scrapping promoter information on wormguides.org
To scrape all the promoter information on wormguides website, run `web_scrapping.py` file in the environment containing the libraries as shown in the **environment setup section**

The scrapper automatilcally acceses each details page of each promoter and gets information such as promoter
name, gene function, temporal and spatial expression details, strain and plasmid details, primers, image urls, and images. It then dumps the data as a json file `data.json` and saves images as `.gif`

## Data Storage on AWS Cloud services
The JSON file was then dumped into a public AWS S3 bucket with the link
Image data was dumped into a public AWS S3 bucket
A SQL database was then created and stored in postgresql database using AWS RDS server

## Docekr in headless mode
The code has been made to run in headless mode by adding an argument `("--headless")` to the driver options
This eliminates issues such as website "slowness" and allows the code too run in the background

## Running the scrapper in a docker container
A docker image was created for the scrapper. To access it,
`docker pull emmacode/neuronal_promoters:v1`

To run the application
`docker run -v ~/.aws/:/root/.aws:ro -it emmacode/neuronal_promoters:v1`

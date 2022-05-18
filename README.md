# WebScraping
## Overview
This project involves creating a `Scrapper` class that can be used to extract information from websites. It includes methods such as `click`, `search`, `accept_all_cookies` etc. which are normally needed to scrape and navigate a website. 

To demonstrate how to use this class, I will use it scrape data from the website, https://www.wormguides.org. This website contains promoter information for *Caenorhabditis elegans* neurons such as sequence, time of expresson, tissues of expression and images for the expression.

## Enviroment setup
To run this script, use a python environment with the folowing libraries installed;
selenium         4.1.5
Python           3.9.12

## imports
The following libraries and packages were installed
![Getting_started](../../../Downloads/code-snapshot.png)

## Code logic
Created a class called `Scrapper` used to scrape data from websites
This class is initialized with the url and path to the driver of your website of interest.
It gives access to methods such as `accept_all_cookies`, `click`, `search`, `forward`, `back`, which are usually needed to navigate webpages. 

## Use Example for crapping promoter information on wormguides.org
To scrape all promoter information on wormguides website, run `web_scrapping.py` file in the environment containing the libraries as shown in the **environment setup section**



# CEN-4930C-Scrap

--- This program started on 10/19/21
I have little to no knowledge of python and how scraping works; however, I did went through youtube videos and a bit of lecture and reading on how to do so.
I am guided by such and will show my progress as a timeline of sorts in here.

--- 10/22/21 around 5:00am
A lot of the files shown here were examples done and practices through the usage of youtube video for my knowledge.

--- 10/22/21 11:48 pm
The main scrapper file is the amazonScraper.py, walmartScraper.py, and sqlTransfer.py

--- 10/23/21 4:28 AM
AmazonScraper.py and WalmartScraper.py are the main files. The database used is sql server so make sure to have import pyodbc
In addition for some reason the amazon scraper sometimes picks up elements that are not correct being sent to sql; however, I reviewed the section into a smaller code
and notice that at times the tag for the ounces and the count are not displayed. It is why sql retrieves NULLS and at times it retrieves incorrect tag of the given which I have no power in without higher knowledge in python as I am still a beginner.

--- 10/24/2021 5:09 AM
Amazonscraper.py has been updated. It nows retrieves reviews more reliably.


--- 10/31/2021

The Scrapper takes records from www.amazon.com searching up 'bottled water' similarly with www.walmart.com searching up 'bottled water'

The data takes information from the websites and place into a database in sql server.
Using python and beautiful soup I was successful and retrieving the data taking information every day for 7 days.

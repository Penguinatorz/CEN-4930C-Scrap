# CEN-4930C-Scrap

--- This program started on 10/19/21
I have little to no knowledge of python and how scraping works; however, I did went through youtube videos and a bit of lecture and reading on how to do so.
I am guided by such and will show my progress as a timeline of sorts in here.

--- 10/22/21 around 5:00am
A lot of the files were done to be used as examples for my project as I had no practice nor knowledge in python and in scrapping such examples done and practices through the usage of youtube video for my knowledge as well as other sites that can further improve my ability.

--- 10/22/21 11:48 pm
The main scrapper file is the amazonScraper.py, walmartScraper.py

--- 10/23/21 4:28 AM
AmazonScraper.py and WalmartScraper.py are the main files. The database used is sql server so make sure to have import pyodbc
In addition for some reason the amazon scraper sometimes picks up elements that are not correct being sent to sql; however, I reviewed the section into a smaller code
and notice that at times the tag for the ounces and the count are not displayed. It is why sql retrieves NULLS and at times it retrieves incorrect tag of the given which I have no power in without higher knowledge in python as I am still a beginner.

--- 10/24/2021 5:09 AM
Amazonscraper.py has been updated. It nows retrieves reviews more reliably.
Im not sure why though the walmart old prices always seems at 0 though on my practice database it had some values now it still shows 0.
Im not sure if it actually works or if water bottles in walmart don't have discount on such items for it to have an 'old price'


--- 10/31/2021

The Scrapper takes records from www.amazon.com searching up 'bottled water' similarly with www.walmart.com searching up 'bottled water'

The data takes information from the websites and place into a database in sql server. The database for the progrm has been exported into two alternatives
the .xls files and the .txt as flat files.
Using python and beautiful soup I was successful and retrieving the data taking information every day for 7 days.

The main scrapper file is the amazonScraper.py, walmartScraper.py

To set up database look into this function in the python script

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=JOANCORAL\SQLEXPRESS;'
                      'Database=ScrapData;'
                      'Trusted_Connection=yes;')
                      
Work around configuring into your database information.



1. Walmart table has about 400 rows. Amazon table has approximately 1000 rows.

2. Walmart able has 10 columns. Amazon table has 10 columns

3. www.walmart.com and www.amazon.com

3a. I collected the data using python coding and using beautiful soup library to scrap information from the respective websites under the searched term 'bottled water'

4. Column 1 is the id for the database. Column 2 is the title. Column 3 is the shorten title. Column 4 is the Price. Column 5 is the subscriber price for amazon and old price for walmart if the item is now on a newly discounted priced it will show the old price before the discount. Column 6 measurement fl oz, oz, gallon and pint. At times each item is listed under different names in ounces or in oz or in fl oz or in fl-oz and its difficult to capture all the variety of measurements they use. Column 7 is the amount or the package amount. Column 8 is the reviews. Column 9 is the date that the item has been retrieved and stored into the database. Column 10 is the product link so remember to type in the domain url at time the product link does not contain the full domain url.

5. This can be a bar graph or some sort of comparison chart between the prices or of any similar items between the two stores. A visualization of what products has cheaper bottled water can also work.

6. SQL SERVER EXPRESS was the program I used for the database. Its also important to import pyodbc for python for my code to work properly and connect to the sql server database.


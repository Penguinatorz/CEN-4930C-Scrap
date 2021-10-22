from bs4 import BeautifulSoup
import requests
from csv import writer

url= "https://www.pararius.com/apartments/amsterdam?ac=1" #requests
page = requests.get(url) #requests

soup = BeautifulSoup(page.content, 'html.parser') #beautiful soup parser
#beautifulsoul lists retrieval find_all to retrieve all information then find() individually
lists = soup.find_all('section', class_="listing-search-item") 

#Write statement
with open('housing.csv', 'w', encoding='utf8', newline='') as f: #file creation
    thewriter =  writer(f) #assigning writer to file
    header = ['Title', 'Location', 'Price', 'Area'] #assigning columns
    thewriter.writerow(header) #assigning columns to the first row

    for list in lists: #looping retrieving info from classes
        title = list.find('a', class_="listing-search-item__link--title").text.replace('\n', '')
        location = list.find('div', class_="listing-search-item__location").text.replace('\n', '')
        price = list.find('div', class_="listing-search-item__price").text.replace('\n', '')
        area = list.find('li', class_="illustrated-features__item--surface-area").text.replace('\n', '')

        info = [title, location, price, area] #info is passed to array
        thewriter.writerow(info) #sent to writer to write down info to csv

import re
import pyodbc
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.amazon.com/s?k=water+bottled&qid=1634885362&ref=sr_pg_1'
itemslist = []
tableName = 'amazonData'


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=JOANCORAL\SQLEXPRESS;'
                      'Database=ScrapData;'
                      'Trusted_Connection=yes;')

def create_table_amazon(tableName):

    c = conn.cursor()
    statement = f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{tableName}'"
    c.execute(statement)
    result = c.fetchone()
    if result:
        return
    else:
        c.execute(f'''CREATE TABLE {tableName}(
    {tableName}_product_id int not NULL identity(1,1) primary key, {tableName}_title varchar(300), {tableName}_split_title varchar(200), {tableName}_price float, {tableName}_subscriber_Price float, {tableName}_ounces varchar(40), {tableName}_count varchar(40), {tableName}_reviews float, {tableName}_date varchar(100), {tableName}_link nvarchar(2083), 
    )''')
        print("Table is now created")

def geturl(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(url, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    return soup2

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


def countCreation(splittxt):
    matches = ["count", "pack", "Count", "Pack"]

    for x in range(len(splittxt)):
        neg1 = x-1
        neg2 = x-2
        pos1 = x+1
        pos2 = x+2

        for b in range(len(matches)):
            tempmatch = matches[b]
            if tempmatch in splittxt[x]:
                if has_numbers(splittxt[x]) is True:
                    return splittxt[x]
                elif has_numbers(splittxt[neg1]):
                    ounces = splittxt[neg1] + " " + splittxt[x]
                    return ounces
                elif has_numbers(splittxt[neg2]):
                    ounces = splittxt[neg2] + " " + splittxt[neg1] + " " + splittxt[x]
                    return ounces
                elif has_numbers(splittxt[pos2]) and  splittxt[pos1] == "of":
                    ounces = splittxt[x] + " " + splittxt[pos1] + " " + splittxt[pos2]
                    return ounces
            elif splittxt[x].endswith("ct") and has_numbers(splittxt[x]):
                ounces = splittxt[x]
                return ounces
    return 1

def sizechecker(splittxt):
    matches = ["ounce", "oz", "-ounce", "gallon", "ml", "oz.", "mL", "Oz", "Gallon", "Ounce", "ounces", "Ounces", "OZ", "ML", "Liter", "Liters"]

    for x in range(len(splittxt)):
        tempval1 = x-1
        tempval2 = x+1
        for b in range(len(matches)):
            tempmatch = matches[b]
            if tempmatch in splittxt[x]:
                if has_numbers(splittxt[x]) is True:
                    return splittxt[x]
                else:
                    ounces = splittxt[tempval1] + " " + splittxt[x]
                    return ounces
            elif splittxt[x] == "Fl" or splittxt[x] == "Fl." or splittxt[x] == "fl" or splittxt[x] == "fl.":
                ounces = splittxt[tempval1] + " " + splittxt[x] + " " + splittxt[tempval2]
                return ounces                
            elif splittxt[x] == "l" or splittxt[x] == "L":            
                ounces = splittxt[tempval1] + " " + splittxt[x]
                return ounces
            elif splittxt[x].endswith("l") and has_numbers(splittxt[x]) is True:
                ounces = splittxt[x]
                return ounces

def getitems(soup2, tablename):
    products = soup2.find_all('div', {'data-component-type': 's-search-result'})

    for item in products:
        try:
            title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text a-text-normal'}).text.strip()
            split_title = title.rsplit(',')[0]
        except:
            title = item.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()
            split_title = title.rsplit(',')[0]
        try:
            link = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text a-text-normal'})['href']
        except:
            link = item.find('a', {'class': 'a-link-normal a-text-normal'})['href']
        try:
            price = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('$', '').strip())
        except:
            price = None
        try:
            subscribePrice = (item.find(text=lambda text: text and " with Subscribe & Save discount" in text).text.replace('$', '')).strip()[:5]
        except:
            subscribePrice = None
        try:
            ounces = item.find('span', {'class': 'a-color-information a-text-bold'}).text.strip()
            split_ounces = ounces.split()
            split_ounces = sizechecker(split_ounces)
        except:
            ounces = None
            split_ounces = ounces
        try:
            count = item.find('span', {'class': 'a-color-information a-text-bold'}).text.strip()
            split_count = count.split()
            split_count = countCreation(split_count)
        except:
            count = None
            split_count = count        
        try:
            reviews = float(item.find('span', {'class': 'a-size-base'}).text.strip())
        except:
            reviews = 0
        
        today = time.asctime(time.localtime(time.time()))

        c = conn.cursor()
        c.execute(f'''
            INSERT INTO {tablename}({tablename}_title, {tablename}_split_title, {tablename}_price, {tablename}_subscriber_Price, {tablename}_ounces, {tablename}_count, {tablename}_reviews, {tablename}_date, {tablename}_link)
            VALUES
            (?,?,?,?,?,?,?,?,?)''', title, 
            split_title, 
            price, 
            subscribePrice, 
            split_ounces,
            split_count, 
            reviews, 
            today, 
            link)

        itemdetails = {
            'title': title,
            'split_title': split_title,
            'price': price,
            'subscriberprice': subscribePrice,
            'ounces': split_ounces,
            'count': split_count,
            'reviews': reviews,
            'Date': today,
            'link': link
             }
        itemslist.append(itemdetails)
    return

def getnextpage(soup): 
    pages = soup.find('ul', {'class': 'a-pagination'})   
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.com' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return


create_table_amazon(tableName)

for x in range(3):
    soup = geturl(url)
    getitems(soup, tableName)
    url = getnextpage(soup)

conn.commit()
conn.close
#df = pd.DataFrame(itemslist)
#df.to_csv('aExample.csv', index=False)
print('Done.')

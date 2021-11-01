import re
import time
import pandas as pd
import pyodbc
import requests
from bs4 import BeautifulSoup
#This was is a failure though I wouldn't it isn't as it does retrieve the items
#The reason why its a failure is because it get stuck at 6 items and loops the retrieval.

url = ['https://www.walmart.com/search?q=bottled+water&affinityOverride=store_led']
categories = ["Water_Bottle"]
itemslist = []
tablename = 'walmartData'

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=JOANCORAL\SQLEXPRESS;'
                      'Database=ScrapData;'
                      'Trusted_Connection=yes;')

def create_table_walmart(tableName):
    c = conn.cursor()
    statement = f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{tableName}'"
    c.execute(statement)
    result = c.fetchone()
    if result:
        return
    else:
        c.execute(f'''CREATE TABLE {tableName}(
    {tableName}_product_id int not NULL identity(1,1) primary key, {tableName}_title varchar(200), {tableName}_split_title varchar(100), {tableName}_price float, {tableName}_old_price varchar(20), {tableName}_ounces varchar(20), {tableName}_count varchar(20), {tableName}_reviews float, {tableName}_date varchar(50), {tableName}_link nvarchar(2083), 
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

def getitems(soup2, tablename):
    products = soup2.find_all('div', {'class': 'mb1 ph1 pa0-xl bb b--near-white w-25'})

    for item in products:
        title = item.find('a', {'class': 'absolute w-100 h-100 z-1'}).text.strip()
        split_title = title.rsplit(',')[0]
        link = item.find('a', {'class': 'absolute w-100 h-100 z-1'})['href']
        try:
            price = float(item.find_all('div', {'class': 'b black f5 mr1 mr2-xl lh-copy f4-l'})[0].text.replace('$', '').strip())
        except:
            price = 0
        try:
            oldprice = item.find_all('div', {'class': 'flex flex-wrap justify-start items-center lh-title mb2 mb1-m'})[0].strip()
            split_oldprice = oldprice.rsplit('$')[3]
        except:
            oldprice = 0
            split_oldprice = oldprice
        try:
            ounces = item.find('span', {'class': 'f6 f5-l normal dark-gray mb0 mt1 lh-title'}).text.strip()
            split_ounces = ounces.split()
            split_ounces = sizechecker(split_ounces)
        except:
            ounces = None
            split_ounces = ounces
        try:
            count = item.find('span', {'class': 'f6 f5-l normal dark-gray mb0 mt1 lh-title'}).text.strip()
            split_count = count.split()
            split_count = countCreation(split_count)
        except:
            count = None
            split_count = count
        try:
            reviews = float(item.find('span', {'class': 'sans-serif gray f7'}).text.strip())
        except:
            reviews = 0
        
        
        today = time.asctime(time.localtime(time.time()))
        
        c = conn.cursor()
        c.execute(f'''
            INSERT INTO {tablename}({tablename}_title, {tablename}_split_title, {tablename}_price, {tablename}_old_price, {tablename}_ounces, {tablename}_count, {tablename}_reviews, {tablename}_date, {tablename}_link)
            VALUES
            (?,?,?,?,?,?,?,?,?)''', title, 
            split_title, 
            price, 
            split_oldprice, 
            split_ounces, 
            split_count,
            reviews, 
            today, 
            link)

        itemdetails = {
            'title': title,
            'split_title': split_title,
            'price': price,
            'oldprice': split_oldprice,
            'ounces': split_ounces,
            'count': split_count,
            'reviews': reviews,
            'Date': today,
            'link': link
             }

        itemslist.append(itemdetails)
    return


create_table_walmart(tablename)
for pg in range(len(url)):
    # number of pages per category
    top_n= ["1","2","3","4","5"]
    
    # extract page number within sub-category
    url_category=url[pg]
    for i_1 in range(len(top_n)):
        url_cat=url_category+"&page="+top_n[i_1]
        soup = geturl(url_cat)
        getitems(soup, tablename)

conn.commit()
#df = pd.DataFrame(itemslist)
#df.to_csv('wExample.csv', index=False)
print('Done.')

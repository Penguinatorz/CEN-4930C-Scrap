#import libraries
from bs4 import BeautifulSoup
import requests
import time
import datetime
import re
import smtplib
import csv
import pandas as pd

#-----I will be scrapping water bottles information, package, ounces, original prices, 
# its discounted price, and the brand. 
# This project will also be scrapping from two websites that is Amazon and Walmart. 
# The retrieval of the data will be run everyday for a week. 
# This is to see any changes in prices of the product.------



#connecting to website

URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
#print(soup2)

title = soup2.find(id='productTitle').get_text()

price = soup2.find(id='priceblock_ourprice').get_text()


size = soup2.find(text=lambda text: text and "Ounces" in text)

today = datetime.date.today()

#print(title)
#print(price)
#print(ounces)

price = price.strip()[1:]
title = title.strip()
size = size.strip()


print(title)
print(price)
print(size)
print(today)

header = ['Title', 'Price', 'Size', 'Date']
data = [title, price, size, today]

with open('amazonExample.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)

df = pd.read_csv(r'C:\Users\blast\Desktop\Stuff\Homework\CEN-4930C\scrapping\amazonExample.csv')

print(df)


#now we are appending data to the csv

with open('amazonExample.csv', 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)

def check_price():
    URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id='productTitle').get_text()
    price = soup2.find(id='priceblock_ourprice').get_text()
    size = soup2.find(text=lambda text: text and "Ounces" in text)
    today = datetime.date.today()

    header = ['Title', 'Price', 'Size', 'Date']
    data = [title, price, size, today]

    with open('amazonExample.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

while(True):
    check_price()
    time.sleep(86400)
    
    df = pd.read_csv(r'C:\Users\blast\Desktop\Stuff\Homework\CEN-4930C\scrapping\amazonExample.csv')
    print(df)




#import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.amazon.com/s?k=water+bottled&qid=1634885362&ref=sr_pg_1'
itemslist = []
check = 1

def geturl(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(url, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    return soup2

def getitems(soup2):
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
        except:
            ounces = None
        try:
            reviews = float(item.find('span', {'class': 'a-size-base'}).text.strip())
        except:
            reviews = 0
        
        itemdetails = {
            'title': title,
            'split_title': split_title,
            'link': link,
            'price': price,
            'subscriberprice': subscribePrice,
            'ounces': ounces,
            'reviews': reviews
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


for x in range(3):
    soup = geturl(url)
    getitems(soup)
    url = getnextpage(soup)

df = pd.DataFrame(itemslist)
df.to_csv('aExample.csv', index=False)
print('Done.')

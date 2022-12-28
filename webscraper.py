from bs4 import BeautifulSoup
import datetime
import requests
import schedule
import time


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
ASIN = "B00005BIEF"

url = f'https://www.amazon.com/dp/{ASIN}/'
file_name = f"{ASIN}-2.txt"


with open(file_name, "w") as file:
    file.write(f'Timestamp,ASIN,Price,Ship From,Sold By\n')

def job():

    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, 'lxml')
    timestamp = datetime.datetime.now()

    # price
    current_price = soup.find('span', attrs={'class': 'a-offscreen'})
    current_price_string = current_price.string

    # ship from
    current_ship_from = soup.find('span', attrs={'class': 'tabular-buybox-text-message'})
    current_ship_from_string = current_ship_from.string

    # sold by
    current_sold_by = soup.find('a', attrs={'id': 'sellerProfileTriggerId'})
    current_sold_by_string = current_sold_by.string

    with open(file_name, "a") as file:
        file.write(f'{timestamp},{ASIN},{current_price_string},{current_ship_from_string},{current_sold_by_string}\n')

schedule.every(2).minutes.until(datetime.timedelta(hours=24)).do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

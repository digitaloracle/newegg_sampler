import json
import os
import sys
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from random import randint
import re



def telegram_send_message(title, url):
    try:
        telegram_api_key = os.environ["telegram_api_key"]
    except KeyError:
        print(datetime.now(), "missing telegram api key")
    chat_id = '-363919721'
    content = f'{title}\n[inline URL]({url})'
    url = f'https://api.telegram.org/bot{telegram_api_key}/sendMessage'
    payload = {'chat_id': chat_id,
               'text': content,
               'parse_mode': 'MarkdownV2'}
    print(datetime.now(), "found something, sending message")
    response = requests.post(url, data=payload)
    return response.json()



if __name__ == "__main__":
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    products = ('https://www.newegg.com/global/il-en/evga-geforce-rtx-3080-10g-p5-3883-kr/p/N82E16814487521?Description=rtx3080&cm_re=rtx3080-_-14-487-521-_-Product',
                'https://www.newegg.com/global/il-en/evga-geforce-rtx-3080-10g-p5-3897-kr/p/N82E16814487518?Description=rtx3080&cm_re=rtx3080-_-14-487-518-_-Product',
                'https://www.newegg.com/global/il-en/evga-geforce-rtx-3080-10g-p5-3885-kr/p/N82E16814487520?Description=rtx3080&cm_re=rtx3080-_-14-487-520-_-Product')

    proxies = ('79.139.56.97:3128', '43.247.39.126:443', '51.83.134.249:3128', '168.169.96.2:8080')


    try:
        while True:
            
            res = ''
            

            for base_url in products:
                time.sleep(3)
                print(datetime.now(), "fetching page")
                res = requests.get(base_url, headers={'User-Agent': ua}, proxies={'https': proxies[randint(0, len(proxies))]})
                if res.status_code != 200:
                    print(datetime.now(), res.text)
                    # sys.exit()


                soup = BeautifulSoup(res.text, 'html.parser')
                sold_out_tag = False
                for i in soup.select(".fa-exclamation-triangle"):
                    try:
                        sold_out_tag = i.select_one("span").contents[0]
                    except AttributeError:
                        pass
                if sold_out_tag:
                    pass
                else:
                    print(datetime.now(), "found item in stock")
                    print(datetime.now(), base_url, soup.select_one('title').contents[0])
                    telegram_send_message( soup.select_one('title').contents[0], base_url)
 
            time.sleep(1800)
    except KeyboardInterrupt:
        sys.exit()
        print(datetime.now(), "exiting")

    except requests.exceptions.ConnectionError:
        sys.exit()
        print(datetime.now(), "connection error")
       
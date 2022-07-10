from datetime import datetime
import requests
from requests import *
from bs4 import BeautifulSoup
import csv
import urllib3
urllib3.disable_warnings()
URL = 'https://www.goszakup.gov.kz/ru/search/announce?filter%5Bname%5D=%D0%BA%D1%83%D1%80%D1%81&filter%5Bcustomer%5D=&filter%5Bnumber%5D=&filter%5Byear%5D=&filter%5Bstatus%5D%5B%5D=230&filter%5Bstatus%5D%5B%5D=280&filter%5Bstatus%5D%5B%5D=220&filter%5Bstatus%5D%5B%5D=240&filter%5Bamount_from%5D=&filter%5Bamount_to%5D=&filter%5Btrade_type%5D=&filter%5Bstart_date_from%5D=&filter%5Bstart_date_to%5D=&filter%5Bend_date_from%5D=&filter%5Bend_date_to%5D=&filter%5Bitog_date_from%5D=&filter%5Bitog_date_to%5D=&smb=/'
HEADERS = {'user agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'accept' : '*/*'
}
HOST= 'https://www.goszakup.gov.kz'
FILE = f'{datetime.now()}-goszakup.csv'

def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params, verify=False)
    return response
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr')
    template = []
    for item in items:
        index = item.find('strong')
        lots = item.find('small')
        ways = item.find_next('a').get_text(strip=True)
        start = item.find_next(ways),
        if index and index != 'None' and lots and start:
            index = index.get_text(strip=True)
            lots = lots.get_text(strip=True)
        else: continue
        template.append({
            'index': index,
            'lots': lots.replace('Лотов:',''),
            'link': HOST + item.find('a').attrs['href'],
            'name': item.find('a').get_text(strip=True),
            'organizer': item.find('a').find_next_sibling().find_next_sibling().get_text(strip=True).replace('Организатор:',''),
            'ways': ways,
            'start':  item.find('td').find_next_sibling().find_next_sibling().find_next_sibling().get_text(strip=True),
            'stop': item.find('td').find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text(strip=True),
            'price': item.find('td').find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().get_text(strip=True),
        })
    return template
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Индекс', 'Лоты', 'Ссылка', 'Имя', 'Организатор', 'Способ', 'Начало', 'Конец', 'Цена'])
        for item in items:
            writer.writerow([item['index'], item['lots'], item['link'], item['name'], item['organizer'], item['ways'], item['start'], item['stop'], item['price']])
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        template = get_content(html.text)
        save_file(template, FILE)
    else:
        print(html.status_code)
parse()
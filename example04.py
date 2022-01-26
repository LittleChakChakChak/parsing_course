import requests
from pymongo import MongoClient
from lxml import html
from pprint import pprint

# Подключение noSQL
client = MongoClient('localhost', 27017)
db = client['parsing']

# Получение новстей с Яндекс.Новости

# headers = {'accept': '*/*', 'user-agent': 'ua.firefox'}
news = []

response = requests.get("https://yandex.ru/news")
dom = html.fromstring(response.text)

items_news = dom.xpath('//div[@class="mg-grid__col mg-grid__col_xs_4"]')

for item_new in items_news:
    new = {}
    name_source = item_new.xpath('.//span[@class="mg-card-source__source"]/a/text()')
    name_new = item_new.xpath('.//h2[@class="mg-card__title"]/a/text()').replace('/xa0',' ')
    url_new = item_new.xpath('.//h2[@class="mg-card__title"]/a/@href')
    date_publication = item_new.xpath('.//span[@class="mg-card-source__time"]/text()')

    new = {'name_new': name_new,
           'name_source': name_source,
           'url_new': url_new,
           'date_publication': date_publication}
    news.append(new)

    # pprint(new)

pprint(news)
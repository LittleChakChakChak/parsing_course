import requests
from pymongo import MongoClient
from lxml import html
from pprint import pprint

# Подключение noSQL
client = MongoClient('localhost', 27017)
db = client['parsing']

# Получение новстей с Яндекс.Новости
news = []

response = requests.get("https://yandex.ru/news")
dom = html.fromstring(response.text)

items_news = dom.xpath('//div[@class="mg-grid__col mg-grid__col_xs_4"]')

for item_new in items_news:
    new = {}
    name_source = item_new.xpath('.//span[@class="mg-card-source__source"]/a/text()')[0]
    name_new = item_new.xpath('.//h2[@class="mg-card__title"]/a/text()')[0].replace('\xa0', ' ')
    url_new = item_new.xpath('.//h2[@class="mg-card__title"]/a/@href')[0]
    date_publication = item_new.xpath('.//span[@class="mg-card-source__time"]/text()')[0]

    new = {'name_new': name_new,
           'name_source': name_source,
           'url_new': url_new,
           'date_publication': date_publication}
    news.append(new)

    # Запись новостей (с проверкой) в бд

    if db.ya_news.find_one({'name_new': new['name_new']}) \
            and db.ya_news.find_one({'name_source': new['name_source']}) \
            and db.ya_news.find_one({'date_publication': new['date_publication']}):
        continue
    else:
        db.ya_news.insert_one(new)


pprint(news)
print('Новости добавлены в бд!')
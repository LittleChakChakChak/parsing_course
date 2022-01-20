import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from pprint import pprint

# создание не реляционную БД
client = MongoClient('localhost', 27017)
db = client['parsing']

print('Введите "1" - если хотите заполнить БД')
print('Введите "2" - если хотите получить данные из БД')
print('Какой вариант вам нужен 1 или 2?')
choice = input()

# Заполнение БД по поиску
if choice == '1':
    # Получение вакансий через парсинг html (метод BeautifulSoup) с сайта hh.ru
    job_search = input('Введите какую вакансию искать: ')
    job_openings = ""
    page = ""

    url = 'https://hh.ru'
    full_url = 'https://hh.ru/search/vacancy/'
    headers = {'accept': '*/*', 'user-agent': 'ua.firefox'}
    params = {'text': job_search, 'items_on_page': 20, 'page': 0}

    data_jobs = []


    # зарплата
    def split_salary(salary_job):
        salary = {}
        if salary_job:
            if salary_job.text.find('–') != -1:
                salary['prefix_salary'] = '-'
                salary_full = salary_job.contents[0].replace(' – ', ', ').replace('\u202f', '')
                salary['min_salary'], salary['max_salary'] = salary_full.split(', ')
                salary['min_salary'] = int(salary['min_salary'])
                salary['max_salary'] = int(salary['max_salary'])
                salary['currency_salary'] = salary_job.contents[2]
            elif salary_job.text.find('от') != -1:
                salary['prefix_salary'] = 'от'
                min_salary = salary_job.contents[2].replace('\u202f', '')
                salary['min_salary'] = int(min_salary)
                salary['currency_salary'] = salary_job.contents[6]
            elif salary_job.text.find('до') != -1:
                salary['prefix_salary'] = 'до'
                max_salary = salary_job.contents[2].replace('\u202f', '')
                salary['max_salary'] = int(max_salary)
                salary['currency_salary'] = salary_job.contents[6]
            else:
                salary = 'не указана'

        return salary


    while True:
        response = requests.get(full_url, params=params, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        list_job = soup.findAll('div', attrs={'class': 'vacancy-serp-item'})

        print(f"Парсим страницу: {params['page'] + 1}")

        for job in list_job:
            data_job = {'name': job.find('a', attrs={'class': "bloko-link"}).text,
                        'job_url': job.find('a', attrs={'class': "bloko-link"}).get('href'),
                        'salary_job': split_salary(
                            job.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})),
                        'city': job.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text}

            if job.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}):
                data_job['company'] = job.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text

            if job.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}):
                data_job['company_url'] = url + job.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).get(
                    'href')

            # data_jobs.append(data_job)

            # проверка на уже существующую запись в БД
            if db.jobs_hh.find_one({'job_url': data_job['job_url']}):
                continue
            else:
                db.jobs_hh.insert_one(data_job)

        if not soup.find('a', text='дальше') or not response.ok:
            break

        params['page'] += 1

    # первое заполнение бд
    # db.jobs_hh.insert_many(data_jobs)

# Чтения из БД с отбором по минимальной зп
elif choice == '2':
    min_salary = int(input('Введите минимальную сумму зп: '))
    for db_job in db.jobs_hh.find():
        salary_job = db_job['salary_job']
        if type(salary_job.get('min_salary')) == int and type(salary_job.get('max_salary')) == int:
            if (salary_job.get('min_salary') >= min_salary) or (salary_job.get('max_salary') >= min_salary
                                                                    and salary_job.get('prefix_salary') == 'до'):
                pprint(db_job)
        else:
            continue
else:
    print("Вы ввели не правиьный вариант")
import requests
from bs4 import BeautifulSoup
import csv
import time
""" Parsing data from the site https://uain.press/ """

# URL = 'https://uain.press/blogs'
# URL = 'https://uain.press/videos'
# URL = 'https://uain.press/news'
# URL = 'https://uain.press/interview'
URL = 'https://uain.press/articles'
# URL = 'https://uain.press/photos'

FILE_NAME = f'data_{URL.split("/")[-1]}.scv'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36"
}


def get_content(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', {"class": 'td_module_3 td_module_wrap td-animation-stack'})
    list_data = []
    for quote in quotes:
        list_data.append(
            {
                'title': quote.find('img', class_="entry-thumb").get('title'),
                'href': quote.find('div', class_='td-module-thumb').find('a').get('href'),
                'src_image': quote.find('img', class_="entry-thumb").get('src'),
                'author': quote.find('div', class_="td-module-meta-info").find('a').text,
                'date': quote.find('time', class_="entry-date updated td-module-date").text
            }
        )
    return list_data


def save_data_scv(items):
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Назва', 'Посилання на статтю', 'Посилання на зображення', 'Автор', 'Дата публікації'])
        for item in items:
            writer.writerow([item['title'], item['href'], item['src_image'], item['author'], item['date']])


def pagination():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    page = soup.find('div', class_='page-nav td-pb-padding-side').find('a', class_='last').text
    return page


def main():
    value_paginator = int(pagination().replace(',', ''))
    if requests.get(URL).status_code == 200:
        all_articles = []
        for p in range(1, value_paginator+1):
            all_articles.extend((get_content(URL + f'/page/{p}/')))
            print(f'Page:{p}')
            save_data_scv(all_articles)
    else:
        print("Error")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(time.monotonic() - start)

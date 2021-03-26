from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
from multiprocessing.dummy import Pool


def get_all_links(url):
    try:
        url, p = url.split('?p')
        p = '?p' + p
    except:
        url = url
        p = ''

    url = url + p  # URL с каталогом
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    r = requests.get(url, headers=headers)  # отправляем HTTP запрос и получаем результат
    soup = BeautifulSoup(r.text, features="lxml")  # Отправляем полученную страницу в библиотеку для парсинга

    all_links = []
    for item in soup.find_all('a', {'class': 'catalog-product__rating ui-link ui-link_black'}):
        g = item.get('href')
        all_links.append(g)
    return all_links


def make_all(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    #url1 = "https://www.dns-shop.ru"
    url2 = link+ "?id=%d&p=1" % (random.randint(1000000000, 9999999999))
    r1 = requests.get(url2, headers=headers) #отправляем HTTP запрос и получаем результат
    soup1 = BeautifulSoup(r1.text) #Отправляем полученную страницу в библиотеку для парсинга
    r = ''
    try:
        popular = soup1.find('div', {'class':'ow-opinions opinions-widget__opinions'}) #cамый популярный отзыв
        popular_text = popular.find('div', {'class':'ow-opinion__texts'})
        for item in popular_text.find_all('p'):
            r = r+' '+ item.text
        name = soup1.find('a', {'class':'product-card-tabs__product-title ui-link ui-link_black'}).text
        review = [name, r, link]
    except:
        review =["NULL", "NULL", link]
    return review


def parser(all_links):
#   all_links = get_all_links(url)
    pool = Pool(len(all_links))
    results = pool.map(make_all, all_links)
    results = pd.DataFrame(results)
    results.rename({0:'name', 1:'review', 2:'url'}, axis=1, inplace=True)
    pool.close()
    return results


from bs4 import BeautifulSoup
import pandas as pd
import requests
import random

def parser(url):
#url = url +"?id=%d&p=1"  % (random.randint(1000000000,9999999999))
#    url = name.replace('~', "/")
    url = url +"?id=%d&p=1"  % (random.randint(1000000000,9999999999)) #URL с товаром
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    r = requests.get(url, headers=headers) #отправляем HTTP запрос и получаем результат
    soup = BeautifulSoup(r.text, features="lxml") #Отправляем полученную страницу в библиотеку для парсинга

    res_get = pd.DataFrame()
    for item in soup.find_all('a',{'class':'catalog-product__rating ui-link ui-link_black'}):
        g = item.get('href')+"?id=%d&p=1" % (random.randint(1000000000,9999999999))
        res_get = res_get.append(pd.DataFrame([[g]],
            columns = ['GET']), ignore_index=True)

    review = pd.DataFrame()

    for index, row in res_get.iterrows():
        url1 = "https://www.dns-shop.ru"
        url2 = url1+row['GET']
        r1 = requests.get(url2, headers=headers) #отправляем HTTP запрос и получаем результат
        soup1 = BeautifulSoup(r1.text) #Отправляем полученную страницу в библиотеку для парсинга
        r = ''
        try:
            popular = soup1.find('div', {'class':'ow-opinion ow-opinion_popular ow-opinions__item'}) #cамый популярный отзыв
            popular_text = popular.find('div', {'class':'ow-opinion__texts'})
            for item in popular_text.find_all('p'):
                r = r+' '+ item.text
            name = soup1.find('a', {'class':'ui-link ui-link_black'}).text
            review = review.append(pd.DataFrame([[name, r]],
                columns = ['name','review']), ignore_index=True)
        except:
          try:
                popular = soup1.find('div', {'class': 'ow-opinion ow-opinions__item'})  # cамый популярный отзыв
                popular_text = popular.find('div', {'class': 'ow-opinion__texts'})
                for item in popular_text.find_all('p'):
                    r = r + ' ' + item.text
                name = soup1.find('a', {'class': 'ui-link ui-link_black'}).text
                review = review.append(pd.DataFrame([[name, r]],
                                                    columns=['name', 'review']), ignore_index=True)
          except:
             a = 0
    return review

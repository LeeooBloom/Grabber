import json
import requests
import time
from pyquery import PyQuery as pq


URL = 'http://www.piluli.ru/product{}/product_info.html'
JSON_FILE = 'export.json'


def requests_get(url):
    limit = 10
    print('Запрос: {}'.format(url))
    for i in range(limit):
        try:
            res = requests.get(url, allow_redirects=False)
            res.raise_for_status()
            if res.status_code > 300:
                print('{}: HTTP {}'.format(url, res.status_code))
                return None
            return res
        except Exception as e:
            print(e)
            print('Ошибка запроса. {}. {} из {}'.format(url, i, limit))
            time.sleep(1)

    return None


def parse_item(item):
    item_pq = pq(item)
    price = item_pq('.price-wrap')[0].text
    price = price and float(price)

    a = item_pq('a:first')[0]
    url = a.attrib['href']
    title = a.text

    obj = {'title': title, 'url': url, 'price': price}
    print('Parsed similar: {}'.format(obj))

    return obj


def parse_form(item):
    item_pq = pq(item)
    price = item_pq('.table-cell .price')[0].text
    price = price and float(price)

    a = item_pq('.table-cell .title')[0]
    url = a.attrib['href']
    title = a.text

    obj = {'title': title, 'url': url, 'price': price}
    return obj 


if __name__ == '__main__':
    start_id = 886299
    limit = 100
    result = []
    try:
        for i in range(start_id, start_id + limit):
            url = URL.format(i)
            response = requests_get(url)
            if not response:
                print('Нет ответа для {}'.format(url))
                continue
            page_pq = pq(response.text)

            title = page_pq('h1')[0].text
            price_text = page_pq('#products_price')[0].text
            price = float(price_text)

            related_items = page_pq('#relatedUnit .slide .slide-item .details')
            similar_items = []
            for item in related_items:
                similar_obj = parse_item(item)
                similar_items.append(similar_obj)

            related_form = page_pq('#allFormsUnit .reg-table .table-row')
            forms = []
            for form in related_form:
                similar_form = parse_form(related_form)
                forms.append(similar_form)


            obj = {'title': title, 'price': price, 'url': url, 'similar': similar_items, 
                   'forms': forms}
            print('Получено: {}'.format(obj))
            result.append(obj)

    finally:
        # try to save something
        with open(JSON_FILE, 'w') as fp:
            json.dump(result, fp, indent=2)





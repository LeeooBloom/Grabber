import requests
from pyquery import PyQuery as pq

URL = 'https://www.piluli.ru'
URL_BRAND = 'https://www.piluli.ru/brand/'
JSON_FILE = 'export.json'


def grab_data(url):
    res = requests.get(url, allow_redirects=False)
    nomenclature_links = []
    nomenclature_links_file = open('C:\\Grabber\\src\\main\\nomenclature_links.txt', 'w')
    try:
        if res.status_code == 200:
            brand_links = parse_brands_links(res)
            for brand_link in brand_links:
                nomenclature_links.extend(collect_nomenclatures_links(brand_link))
        else:
            print('{}: HTTP {}'.format(url, res.status_code))
    except:
        print('Ошибка запроса. {}'.format(url))
    for link in nomenclature_links:
        nomenclature_links_file.write('%s\n' % link)
    return nomenclature_links


# parse postfix of brand page
def parse_brands_links(res):
    brands = pq(res.text) \
        .find(".brands--grid-item") \
        .map(lambda i, item: pq(item).attr('href'))
    return brands


def collect_nomenclatures_links(brand_link):
    nomenclatures = []
    target_url = URL + '{}'.format(brand_link) + '{}'
    i = 2
    res = requests.get(target_url.format(''))
    while (True):
        nomenclatures.extend(set(pq(res.text)
                                 .find('.item-name')
                                 .map(lambda i, item: pq(item).find('a').attr('href'))))
        res = requests.get(target_url.format('/page{}'.format(i)))
        if (res.url == target_url.format('')):
            break
        i += 1
    return nomenclatures


def main():
    grab_data(URL_BRAND)
    return None


if __name__ == '__main__':
    main()


# collect data to {brand,{nomenclature,[add_sales]}}
# collect nomenclature and add_sales to {nomenclature,[add_sales]}

def collect_nomenclatures_with_add_sales(nomenclature):
    return None

# def requests_get(url):
#     limit = 10
#     print('Запрос: {}'.format(url))
#     for i in range(limit):
#         try:
#             res = requests.get(url, allow_redirects=False)
#             res.raise_for_status()
#             if res.status_code > 300:
#                 print('{}: HTTP {}'.format(url, res.status_code))
#                 return None
#             return res
#         except Exception as e:
#             print(e)
#             print('Ошибка запроса. {}. {} из {}'.format(url, i, limit))
#             time.sleep(1)
#
#     return None
#
#
# def parse_item(item):
#     item_pq = pq(item)
#     price = item_pq('.price-wrap')[0].text
#     price = price and float(price)
#
#     a = item_pq('a:first')[0]
#     url = a.attrib['href']
#     title = a.text
#
#     obj = {'title': title, 'url': url, 'price': price}
#     print('Parsed similar: {}'.format(obj))
#
#     return obj
#
#
# def parse_form(item):
#     item_pq = pq(item)
#     price = item_pq('.table-cell .price')[0].text
#     price = price and float(price)
#
#     a = item_pq('.table-cell .title')[0]
#     url = a.attrib['href']
#     title = a.text
#
#     obj = {'title': title, 'url': url, 'price': price}
#     return obj
# f
#
# if __name__ == '__main__':
#     start_id = 886299
#     limit = 100
#     result = []
#     try:
#         for i in range(start_id, start_id + limit):
#             url = URL.format(i)
#             response = requests_get(url)
#             if not response:
#                 print('Нет ответа для {}'.format(url))
#                 continue
#             page_pq = pq(response.text)
#
#             title = page_pq('h1')[0].text
#             price_text = page_pq('#products_price')[0].text
#             price = float(price_text)
#
#             related_items = page_pq('#relatedUnit .slide .slide-item .details')
#             similar_items = []
#             for item in related_items:
#                 similar_obj = parse_item(item)
#                 similar_items.append(similar_obj)
#
#             related_form = page_pq('#allFormsUnit .reg-table .table-row')
#             forms = []
#             for form in related_form:
#                 similar_form = parse_form(related_form)
#                 forms.append(similar_form)
#
#
#             obj = {'title': title, 'price': price, 'url': url, 'similar': similar_items,
#                    'forms': forms}
#             print('Получено: {}'.format(obj))
#             result.append(obj)
#
#     finally:
#         # try to save something
#         with open(JSON_FILE, 'w') as fp:
#             json.dump(result, fp, indent=2)

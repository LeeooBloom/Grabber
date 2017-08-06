import requests
from pyquery import PyQuery as pq

URL = 'https://www.piluli.ru{}'
URL_BRAND = 'https://www.piluli.ru/brand/'
CATEGORY_URL = 'https://www.piluli.ru/categories.html'
JSON_FILE = 'export.json'


def grab_data(url):
    res = requests.get(url, allow_redirects=False)
    nomenclature_links_file = open(
        'C:\\Grabber\\src\\main\\nomenclature_links_1.txt', 'w')
    nomenclature_links = []
    parse_category_rec(CATEGORY_URL, nomenclature_links)
    for link in set(nomenclature_links):
        nomenclature_links_file.write('%s\n' % link)
    return nomenclature_links


def write_unique_nomenclature_links():
    lines = [line.rstrip('\n') for line in open("C:\\Grabber\\src\\main\\nomenclature_links_1.txt")]
    unique_lines = set(lines)
    file = open('C:\\Grabber\\src\\main\\unique_links.txt', 'w')
    for line in unique_lines:
        file.write('%s\n' % line)


def parse_category_links(url):
    nomenclatures = []
    res = requests.get(url, allow_redirects=False)
    content = pq(res.text)
    category_links = content('a[href^="/category"]') \
        .map(lambda i, data: pq(data).attr('href')) \
        .filter(lambda i, text: "index.html" not in text)
    for link in category_links:
        content = pq(requests.get(URL.format(link) + "/index.html", allow_redirects=False).text)
        first_level_ids = content.find('li').map(lambda i, li: pq(li).attr('data-id'))
        for first_level_id in first_level_ids:
            first_level_url = URL.format(link) + '_{}'.format(first_level_id) + "/index.html"
            first_level_content = pq(requests.get(first_level_url, allow_redirects=False).text)
            second_level_ids = first_level_content.find('li').map(lambda i, li: pq(li).attr('data-id'))
            for second_level_id in second_level_ids:
                second_level_url = URL.format(link) + '_{}'.format(first_level_id) \
                                   + '_{}'.format(second_level_id) + "/index.html"
                second_level_content = pq(requests.get(second_level_url, allow_redirects=False).text)
                if (second_level_content('a[href^="/category"]') > 0):
                    nomenclatures.extend(parse_category_links(second_level_url))
    return nomenclatures


def parse_category_rec(url, nomenclatures):
    content = pq(requests.get(url).text)
    content_ids = content.find('li').map(lambda i, li: pq(li).attr('data-id'))
    if content_ids.length == 0:
        nomenclatures.extend(collect_nomenclatures_links(url))
    else:
        for content_id in content_ids:
            if url in CATEGORY_URL:
                parse_category_rec(URL.format("/category") + content_id, nomenclatures)
            else:
                parse_category_rec(url + '_{}'.format(content_id), nomenclatures)


# parse postfix of brand page
def parse_brands_links(res):
    brands = pq(res.text) \
        .find(".brands--grid-item") \
        .map(lambda i, item: pq(item).attr('href'))
    return brands


def collect_nomenclatures_links(link):
    nomenclatures = []
    target_url = link + '/index.html' + '{}'
    i = 2
    res = requests.get(target_url.format(''))
    while (True):
        nomenclatures.extend(set(pq(res.text)
                                 .find('.item-name')
                                 .map(lambda i, item: pq(item).find('a').attr('href'))))
        res = requests.get(target_url.format('?page={}'.format(i)), allow_redirects=False)
        if (res.status_code > 300):
            break
        i += 1
    return nomenclatures


def main():
    write_unique_nomenclature_links()
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

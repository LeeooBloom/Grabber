from time import sleep

import requests
import unicodecsv as csv
from pyquery import PyQuery as pq

URL = 'https://www.piluli.ru{}'
# name, id
MNN_CACHE = {}
BRAND_CACHE = {}
COUNTRY_CACHE = {}
PRODUCER_CACHE = {}
# nomenclature_name, [nomenclature_name]
ADD_SALES = {}
# id,name,mnn_id,symptom_id,brand_id,country_id,producer_id
NOMENCLATURE_CACHE = []
# id,nomenclature_id,nomenclture_id
LINKED_ADD_SALES = []
# id,name,nomenclature_id,
SYMPTOM_CACHE = []


def collect_and_save():
    nomenclature_id = 1
    links = [line.rstrip('\n') for line in open("C:\\Grabber\\src\\main\\unique_links.txt")]
    res = None
    for link in links:
        try:
            res = requests.get(URL.format(link), allow_redirects=False)
        except:
            print('Ошибка ввыполнения запроса {}'.format(URL.format(link)))
            print('Пауза перед повторным запросом, 5 сек.')
            sleep(5)
            try:
                print('Ошибка ввыполнения запроса {}'.format(URL.format(link)))
                print('Пауза перед повторным запросом, 15 сек.')
                sleep(15)
                res = requests.get(URL.format(link), allow_redirects=False)
            except:
                res = None
        if res is not None:
            content = pq(res.text)
            details = content.find(".details-list")
            related = content.find('#relatedUnit')
            nomenclature_name = content('h1[itemprop="name"]').text()
            producer = None
            country = None
            brand = None
            mnn = None
            symptom = None
            add_sales = pq(related('a[href^="/product"]')).filter('.title').map(lambda i, name: pq(name).text())
            if len(pq(details('a[href^="/manufacturer"]')).text().split(",")) > 1:
                producer = pq(details('a[href^="/manufacturer"]')).text().split(",").pop(0)
                country = pq(details('a[href^="/manufacturer"]')).text().split(",").pop(1)
            else:
                producer = pq(details('a[href^="/manufacturer"]')).text()
            brand = pq(details('a[href^="/brand"]')).text()
            mnn = pq(details('.activesubstance_name')).text()
            symptom = content('#desc1').text()
            add_in_cache(BRAND_CACHE, brand)
            add_in_cache(COUNTRY_CACHE, country)
            add_in_cache(PRODUCER_CACHE, producer)
            add_in_cache(MNN_CACHE, mnn)
            symptom = process_symptom_and_put_in_cache(nomenclature_id, SYMPTOM_CACHE, symptom)
            nomenclature = (nomenclature_id, nomenclature_name,
                            get_id_from_cache(MNN_CACHE, mnn),
                            get_id_from_cache(BRAND_CACHE, brand), get_id_from_cache(COUNTRY_CACHE, country),
                            get_id_from_cache(PRODUCER_CACHE, producer))
            NOMENCLATURE_CACHE.append(nomenclature)
            ADD_SALES.update({nomenclature_name: "\\".join(add_sales)})
            nomenclature_id += 1
    write()
    return None


def process_symptom_and_put_in_cache(nomenclature_id, cache, value):
    if value is not None and len(value) is not 0:
        value = value.replace('Показания', '')
        processed = ','.join(value.split())
        cache.append((nomenclature_id, value))
        return processed
    else:
        return None


def add_in_cache(cache, value):
    if value is not None and value not in cache and len(value) is not 0:
        cache.update({value: len(cache) + 1})


def get_id_from_cache(cache, value):
    if cache.get(value) is None:
        return 'null'
    else:
        return cache.get(value)


def write():
    brands = open("C:\\Grabber\\src\\main\\brand.csv", 'wb')
    writer = csv.writer(brands)
    writer.writerows(BRAND_CACHE.items())
    brands.flush()
    brands.close()

    mnns = open("C:\\Grabber\\src\\main\\mnn.csv", 'wb')
    writer = csv.writer(mnns)
    writer.writerows(MNN_CACHE.items())
    mnns.flush()
    mnns.close()

    countries = open("C:\\Grabber\\src\\main\\country.csv", 'wb')
    writer = csv.writer(countries)
    writer.writerows(COUNTRY_CACHE.items())
    countries.flush()
    countries.close()

    producers = open("C:\\Grabber\\src\\main\\producer.csv", 'wb')
    writer = csv.writer(producers)
    writer.writerows(PRODUCER_CACHE.items())
    producers.flush()
    producers.close()

    symptoms = open("C:\\Grabber\\src\\main\\symptom.csv", 'wb')
    writer = csv.writer(symptoms)
    writer.writerows(SYMPTOM_CACHE)
    symptoms.flush()
    symptoms.close()

    nomenclatures = open("C:\\Grabber\\src\\main\\nomenclature.csv", 'wb')
    writer = csv.writer(nomenclatures)
    writer.writerows(NOMENCLATURE_CACHE)
    nomenclatures.flush()
    nomenclatures.close()

    add_sales = open("C:\\Grabber\\src\\main\\add_sales.csv", 'wb')
    writer = csv.writer(add_sales)
    writer.writerows(ADD_SALES.items())
    add_sales.flush()
    add_sales.close()

    return None


def main():
    collect_and_save()
    return None


if __name__ == '__main__':
    main()

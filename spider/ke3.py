import requests
from pyquery import PyQuery as pq
import json
import pandas as pd
from multiprocessing.pool import Pool

columns = ['title', 'place', 'msg', 'price', 'per_meter']

# 爬取某网页
def get_a_page(url):
    result = requests.get(url)
    doc = pq(result.text)
    ul = doc('.sellListContent')
    divs = ul.children('.clear .info.clear').items()
    titles = []
    places = []
    msgs = []
    prices = []
    per_meters = []
    count = 0
    for div in divs:
        count += 1
        title = div.children('.title a').text()
        place = div.children('.address .flood .positionInfo a').text()
        msg = div.children('.address .houseInfo').text()
        price = div.children('.address .priceInfo .totalPrice span').text()
        # per_meter = div.children('.address .priceInfo .unitPrice').attr('data-price')
        per_meter = div.children('.address .priceInfo .unitPrice span').text()
        dict = {
            'title': title,
            'place': place,
            'msg': msg,
            'price': price,
            'per_meter': per_meter
        }
        titles.append(title)
        places.append(place)
        msgs.append(msg)
        prices.append(price)
        per_meters.append(per_meter)
        print(str(count) + ':' + json.dumps(dict, ensure_ascii=False))

    # 写excel
    datas={
        'title': titles,
        'place': places,
        'msg': msgs,
        'price': prices,
        'per_meter': per_meters
    }
    df = pd.DataFrame(data=datas, columns=columns)
    df.to_csv('nj.csv', mode='a', index=False, header=False)

if __name__ == '__main__':
    pool = Pool(20)
    group = ([f'https://nj.ke.com/ershoufang/jiangning/pg{x}/'for x in range(1, 2000)])
    pool.map(get_a_page,group)
    pool.close()
    pool.join()
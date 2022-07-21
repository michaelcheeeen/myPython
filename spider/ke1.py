import requests
from pyquery import PyQuery as pq
import json

def get_a_page(url):
    result = requests.get(url)
    doc = pq(result.text)
    ul = doc('.sellListContent')
    divs = ul.children('.clear .info.clear').items()
    count=0
    for div in divs:
        count += 1
        title = div.children('.title a').text()
        place = div.children('.address .flood .positionInfo a').text()
        msg = div.children('.address .houseInfo').text()
        price = div.children('.address .priceInfo .totalPrice span').text()
        per_meter = div.children('.address .priceInfo .unitPrice').attr('data-price')
        dict = {
            'title': title,
            'place': place,
            'msg': msg,
            'price': price,
            'per_meter': per_meter
        }
        print(str(count) + ':' + json.dumps(dict, ensure_ascii=False))
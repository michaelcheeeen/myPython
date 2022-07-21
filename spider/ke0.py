import requests

def get_a_page(url):
    result = requests.get(url)
    print(result.text)

if __name__ == '__main__':
    for i in range(1, 2):
        get_a_page(f'https://nj.ke.com/ershoufang/jiangning/pg{i}/')

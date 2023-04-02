import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urljoin

os.mkdir('data')

url1 = str(input('Введите url сайта: ')) # 'https://habr.com/ru/'
url_deep = int(input('Введите глубину обхода: ')) # 2
finish = set()


def get_links(url: str, deep: int):
    if deep == 0:
        return url
    list_all = []
    try:
        req = Request(url)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, "lxml")
        for part_link in soup.findAll('a'):
            p_link = part_link.get('href')
            if str(p_link)[0:4] != 'http':
                if p_link not in finish:
                    finish.add(urljoin(url, p_link))
                    list_all.append(urljoin(url, p_link))

            if deep > 0:
                for n in list_all:
                    get_links(n, deep = deep - 1)
            deep -= 1

        return finish
    except ValueError:
        print(f'{url1} - не ссылка, введите другую')


try:
    if url_deep == 0:
        urls = open('urls.txt', 'w')
        urls
        datas = open(f'data1/1.html', 'w')

    else:
        end = list(get_links(url1, url_deep))

        with open('urls.txt', 'w') as text:
            text.write(f"{1} {url1}\n")
            for index, item in enumerate(end):
                text.write(f"{index + 2} {item}\n")
            text.close()

        for index, item in enumerate(end):
            with open(f'data/{index + 1}.html', 'w') as site:
                site.write(f"{BeautifulSoup(urlopen(Request(item)), 'lxml')}\n")
            site.close()
except TypeError:
    print('там возможненько указан не сайт (TypeError)')

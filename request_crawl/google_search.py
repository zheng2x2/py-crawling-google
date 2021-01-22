import requests
from bs4 import BeautifulSoup


def search_result(html):
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    result_count = soup.select_one('#result-stats')
    print(result_count.get_text())


def search_keyword(keyword):
    base_url = 'https://www.google.co.kr/search'

    #: 검색조건 설정
    values = {
        'sxsrf': 'ALeKk019OlTWuIKsVgBJ8SetotOu9RVY5Q:1609994327560',
        'ei': 'V5D2X-raIYPT-Qah1rOAAg',
        'q': keyword,  # 검색할 내용
        'oq': keyword,
        'gs_lcp': 'CgZwc3ktYWIQAzIFCCEQoAFQAFgAYNLkEGgAcAB4AIABjQGIAY0BkgEDMC4xmAEAqgEHZ3dzLXdpesABAQ',
        'sclient': 'psy-ab',
        'ved': '0ahUKEwiq4u-fgInuAhWDad4KHSHrDCAQ4dUDCA0',
        'uact': '5'
    }

    # Google에서는 Header 설정 필요
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) \ Chrome/87.0.4280.88 Safari/537.36',
           'sec-ch-ua': '"Google Chrome";v="87"," Not;A Brand";v="99","Chromium";v="87"',
           'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
           'accept-encoding': 'gzip,deflate,br'
           }

    response = requests.get(base_url,params=values,headers=hdr)

    if response.status_code == 200:
        # print(response.url)
        # print(response.headers)
        # print(response.text)

        # soup = BeautifulSoup(response.text, 'html.parser')
        # result_count = soup.select_one('#result-stats')
        # print(result_count.get_text())

        search_result(response.text)
    else:
        print(response.status_code)


if __name__ == '__main__':
    keywords = ['칼칼한 김치볶음밥', '"칼칼한 김치볶음밥"', '칼칼한 AND 김치볶음밥']

    for keyword in keywords:
        print(keyword)
        search_keyword(keyword)
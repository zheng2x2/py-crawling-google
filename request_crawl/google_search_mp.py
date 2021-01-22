import time
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import db_conn
# import pandas as pd

pg_conn_cursor = None

# def search_result(html):
#     try:
#         # print(html)
#         soup = BeautifulSoup(html, 'html.parser')
#         result_count = soup.select_one('#result-stats')tea
#         if result_count is not None:
#             text = result_count.get_text()
#             start_idx = 0
#             if "약" in text:
#                 start_idx = 7
#                 text = text[7 : result_count.index("개")].replace(",", "")
#             elif "About" in text:
#                 text = text[6 : result_count.index(" result")].replace(",", "")
#             else:
#                 text = text[5 : result_count.index("개")].replace(",", "")
#
#             print("##### 검색결과 >> ", text)
#         else:
#             print("검색결과 : 0")
#
#         db_conn.update_result2(col, row[col], int(num), row[1], row[2] )
#
#     except Exception as e:
#         print(e)


def search_keyword(keyword):
    base_url = 'https://www.google.co.kr/search'
    columns = [2,3,4] #keyword1, keyword2, keyword3

    try:
        res_cd = 0
        for col in columns:
            #: 검색조건 설정
            values = {
                'sxsrf': 'ALeKk019OlTWuIKsVgBJ8SetotOu9RVY5Q:1609994327560',
                'ei': 'V5D2X-raIYPT-Qah1rOAAg',
                'q': keyword[col],  # 검색할 내용
                'oq': keyword[col],
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

            response = requests.get(base_url, params=values, headers=hdr)

            if response.status_code == 200:
                # print(response.url)
                # print(response.headers)
                # print("response.text :::", response.text)

                # result_count = soup.select_one('#result-stats')
                # search_result(response.text)

                try:
                    html = response.text # print(html)
                    soup = BeautifulSoup(html, 'html.parser')
                    # result_count = None
                    print("res ::", response.status_code,  keyword[col], "#result-stats >>> ", soup.select_one('#result-stats'))
                    result_count = soup.select_one('#result-stats')
                    if result_count is not None:
                        text = result_count.get_text()
                        start_idx = 0
                        if "약" in text:
                            print("약 >> ", text)
                            text = text[7 : text.index("개")].replace(",", "")
                        elif "About" in text:
                            print("About >> ", text)
                            text = text[6 : text.index(" result")].replace(",", "")
                        else:
                            print("ELSE >> ", text) #검색결과 1개 (0.57초)
                            text = text[5 : text.index("개")].replace(",", "")
                        
                        db_conn.update_result2(col, keyword[col], int(text), keyword[0], keyword[1])
                    else:
                        print(keyword[col], "검색결과 : 0")
                        db_conn.update_result2(col, keyword[col], 0, keyword[0], keyword[1])

                except Exception as e:
                    print("오류 1 >>", e)
                
            else:
                print("ERROR >> status_code >>", response.status_code) #429?
                if response.status_code == 429:
                    res_cd = 429
            time.sleep(1)
        print("res_cd 1 >> ", res_cd)
        if res_cd == 429:
            print("res_cd 2 >> ", res_cd)
            return

    except Exception as e:
        print("오류 2 >>", e)


def get_keywords():

    global pg_conn_cursor
    pg_conn_cursor = db_conn.connect() # DB 연결

    # pg_conn_cursor.execute("""
    #     select name_ko , taste_ko,
    #         case
    #             when ( synonyms is null or synonyms = '' ) then taste_ko || ' AND ' || name_ko
    #             else '('|| taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') ' ||  name_ko
    #         end as keyword,
    #         case
    #             when ( synonyms is null or synonyms = '' ) then taste_ko || ' AROUND(4) ' || name_ko
    #             else '('|| taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') AROUND(4) ' ||  name_ko
    #         end as keyword2,
    #         case
    #             when ( synonyms is null or synonyms = '' ) then '"'|| taste_ko || ' ' || name_ko || '"'
    #             else '"('|| taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') ' ||  name_ko || '"'
    #         end as keyword3
    #     from dish_names dn, taste_adj ta;
    # """)

    pg_conn_cursor.execute("""
        select r.name_ko , r.taste_ko, --674932
            case
                when ( synonyms is null or synonyms = '' ) then r.taste_ko || ' AND ' || r.name_ko
                else '('|| r.taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') ' ||  r.name_ko
            end as keyword,
            case
                when ( synonyms is null or synonyms = '' ) then r.taste_ko || ' AROUND(4) ' || r.name_ko
                else '('|| r.taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') AROUND(4) ' ||  r.name_ko
            end as keyword2,
            case
                when ( synonyms is null or synonyms = '' ) then '"'|| r.taste_ko || ' ' || r.name_ko || '"'
                else '"('|| r.taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') ' ||  r.name_ko || '"'
            end as keyword3
        from dish_names dn, taste_adj ta, retrieve_nums4 r
        where r.con_and is null
        and r.con_around4 is null
        and r.con_quote  is null
        and r.name_ko = dn.name_ko 
        and r.taste_ko = ta.taste_ko ;
    """)

    keyword = pg_conn_cursor.fetchall()
    # pg_conn_cursor.execute("""
    #     select 
    #         case 
    #             when ( synonyms is null or synonyms = '' ) then taste_ko || ' AND ' || name_ko
    #             else '('|| taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') ' ||  name_ko
    #         end as keyword
    #     from dish_names dn, taste_adj ta;
    # """)
    # keyword = pg_conn_cursor.fetchall()
    global pool
    pool = Pool(processes=1)  # CPU Core 개수
    pool.map(search_keyword, keyword) # 함수, 리스트
    
    # pg_conn_cursor.execute("""
    #     select 
    #         case 
    #             when ( synonyms is null or synonyms = '' ) then taste_ko || ' AROUND(4) ' || name_ko 
    #             else '('|| taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') AROUND(4) ' ||  name_ko
    #         end as keyword2
    #     from dish_names dn, taste_adj ta;
    # """)
    # keyword2 = pg_conn_cursor.fetchall()
    # pool = Pool(processes=8)  # CPU Core 개수
    # pool.map(search_keyword, keyword2) # 함수, 리스트

    # pg_conn_cursor.execute("""
    #     select 
    #         case 
    #             when ( synonyms is null or synonyms = '' ) then '"'|| taste_ko || ' ' || name_ko || '"'
    #             else '"('|| taste_ko || ' OR ' || replace(synonyms, ',', ' OR') ||') ' ||  name_ko || '"' 
    #         end as keyword3
    #     from dish_names dn, taste_adj ta;
    # """)
    # keyword3 = pg_conn_cursor.fetchall()
    # pool = Pool(processes=8)  # CPU Core 개수
    # pool.map(search_keyword, keyword3) # 함수, 리스트


if __name__ == '__main__':

    start_time = time.time()

    get_keywords()

    # for keyword in keywords:
    #     print(keyword)
    #     search_keyword(keyword)

    print("--- %s seconds ---" % (time.time() - start_time))
    db_conn.dbclose()


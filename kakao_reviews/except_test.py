import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup

import csv
import ssl
from urllib.request import urlopen
from urllib.parse import quote_plus

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')
chromedriver_path = "/chromedriver"
driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기


def main():
    global driver, load_wb, review_num

    driver.implicitly_wait(4)  # 렌더링 될때까지 기다린다 4초
    driver.get('https://map.kakao.com/')  # 주소 가져오기
   
    # place_infos = ['맛집']  # 검색할 목록

    # for i, place in enumerate(place_infos):
    #     # delayn
    #     if i % 4 == 0 and i != 0:
    #         sleep(5)
    #     print("#####", i)
    #     search(place)
    search('맛집')
    driver.quit()
    print("finish")


def search(place):
    global driver

    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]')  # 검색 창
    search_area.send_keys(place)  # 검색어 입력
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    sleep(2)

    # 검색된 정보가 있는 경우에만 탐색
    # 1번 페이지 place list 읽기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    place_lists = soup.select('.placelist > .PlaceItem')  # 검색된 장소 목록
    # place_lists = soup.select('.placelist') # 검색된 장소 목록



    # 검색된 첫 페이지 장소 목록 크롤링하기
    crawling(place, place_lists)
    search_area.clear()

    # 우선 더보기 클릭해서 2페이지
    # try:
    #     driver.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
    #     sleep(1)

    #     # 2~ 5페이지 읽기
    #     for i in range(2, 6):
    #         # 페이지 넘기기
    #         xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
    #         driver.find_element_by_xpath(xPath).send_keys(Keys.ENTER)
    #         sleep(1)

    #         html = driver.page_source
    #         soup = BeautifulSoup(html, 'html.parser')
    #         place_lists = soup.select('.placelist > .PlaceItem')  # 장소 목록 list
    #         # place_lists = soup.select('.placelist') # 장소 목록 list
    #         crawling(place, place_lists)

    # except ElementNotInteractableException:
    #     print('not found')
    # finally:
    #     search_area.clear()

async def crawling(p, place_lists):
    """ 페이지 목록을 받아서 크롤링 하는 함수 :param place: 리뷰 정보 찾을 장소이름 """
    ad_flg = 0
    while_flag = False
    
    for i, place in enumerate(place_lists):
        # 광고에 따라서 index 조정해야함
        # if i >= 6:
        place_name = place.select('.head_item > .tit_name > .link_name')[0].text
        print(i+1, place_name)
        try:
            detail_page_xpath = '//*[@id="info.search.place.list"]/li[' + str(i+1) + ']/div[5]/div[4]/a[1]'
            driver.find_element_by_xpath(detail_page_xpath).send_keys(Keys.ENTER)
            # driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환
            sleep(1)
            # place_name = place.select('.head_item > .tit_name > .link_name')[0].text  # place name
            # place_address = place.select('.info_item > .addr > p')[0].text  # place address
            # print('####', place_name, '####', place_address)
            
            # extract_review(place_name, place_address) # 첫 페이지
            print("one more tme", i+1, place_name)
           
        except (NoSuchElementException, ElementNotInteractableException):
            print("Ad Item")

def extract_review(place_name, place_address):
    global driver

    ret = True

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
   # more_button = driver.find_element_by_xpath('//*[@id="mArticle"]/div[5]/div[4]/ul/li[5]/div[2]/p/button').send_keys(Keys.ENTER)  #댓글에 더보기 버튼

    # 첫 페이지 리뷰 목록 찾기
    review_lists = soup.select('.list_evaluation > li')

    #리뷰가 있는 경우
    if len(review_lists) != 0:
        for i, review in enumerate(review_lists):
            comment = review.select('.txt_comment > span') # 리뷰
            rating = review.select('.grade_star > em') # 별점
            val = ''
            if len(comment) != 0:
                if len(rating) != 0:
                    # if len(more_button) != 0:
                    #     more_button
                    #     sleep(1)
                    val = place_name + ',' + place_address + ',' + comment[0].text + ',' + rating[0].text.replace('점', '')
                    # else:
                    #     val = place_name + ',' + place_address + ',' + comment[0].text + ',' + rating[0].text.replace('점', '')
                else:
                    val = comment[0].text + '/0'
                print(val)
                # with open('맛집.csv', 'a', encoding='utf-8', newline='')as writer_csv:
                #     writer = csv.writer(writer_csv, delimiter=',')
                #     writer.writerow([val])
    else:
        print('no review in extract')
        ret = False

    return ret


if __name__ == "__main__":
    main()
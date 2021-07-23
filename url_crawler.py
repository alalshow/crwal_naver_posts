from common.chrome import open_browser, get_chrome_driver, close_browser
from tqdm.notebook import tqdm
import tqdm
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import sys
import platform

# 네이버에서 검색어 입력받아 검색 한 후 블로그 메뉴를 선택하고
# 오른쪽에 있는 검색옵션 버튼을 눌러서
# 정렬 방식과 기간을 입력하기


def get_urls(query_txt, start_date, end_date, page_count):

    # Step 1. 크롬 웹브라우저 실행
    open_browser()
    driver = get_chrome_driver()

    # 사이트 주소는 네이버
    driver.get('http://www.naver.com')
    driver.maximize_window()
    time.sleep(2)

    # Step 2. 네이버 검색창에 "검색어" 검색
    element = driver.find_element_by_id("query")
    element.send_keys(query_txt)  # query_txt는 위에서 입력한 '이재용'
    element.submit()
    time.sleep(2)

    # Step 3. "블로그" 카테고리 선택
    driver.find_element_by_link_text("블로그").click()    # .click() 괄호 안을 눌러라는 뜻
    time.sleep(2)

    url_list = []
    title_list = []

    search_url = "https://search.naver.com/search.naver?date_from="

    for i in range(0, page_count):  # 페이지 수
        print(f"페이지번호====>{i}")
        i = i*10 + 1
        url = f"{search_url}{start_date}&date_option=8&date_to={end_date}&dup_remove=1&nso=p%3Afrom{start_date}to{end_date}post_blogurl=&post_blogurl_without=&query={query_txt}&sm=tab_pge&srchby=all&st=sim&where=post&start={i}"
        print(url)
        driver.get(url)
        time.sleep(0.5)

        # URL 크롤링 시작
        titles = "a.total_tit"
        article_raw = driver.find_elements_by_css_selector(titles)
    #     article_raw

        # url 크롤링 시작
        for article in article_raw:
            url = article.get_attribute('href')
            url_list.append(url)

        # 제목 크롤링 시작
        for article in article_raw:
            title = article.get_attribute('title')
            title_list.append(title)

            print(title)

    print('최종 url갯수: ', len(url_list))

    # 브라우저 닫기
    close_browser(driver)

    return url_list


if __name__ == "__main__":

    # Step 0. 필요한 모듈과 라이브러리를 로딩하고 검색어를 입력 받습니다.
    query_txt = "이재용"
    start_date = "20210608"
    end_date = "20210614"
    page_count = 1

    urls = get_urls(query_txt, start_date, end_date, page_count)
    print(urls)

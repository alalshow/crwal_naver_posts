import sys
import os
import pandas as pd
import time
import numpy as np
from common.chrome import open_browser, close_browser, get_chrome_driver
from common.utils import remove_file

# "blog_url.xlsx" 불러오기
input_file = "output/blog_url.xlsx"
output_file = f"output/blog_content_{input_file}"
remove_file(output_file)

url_load = pd.read_excel(input_file)        # 기본 모델
num_list = len(url_load)
print(f"글 갯수: {num_list}")

dict = {}  # 전체 크롤링 데이터를 담을 그릇

# ★수집할 글 갯수
number = 2
for i in range(0, num_list):
    # 글 띄우기
    url = url_load['url'][i]
    browser = open_browser()
    driver = get_chrome_driver()

    # 사이트 주소는 네이버
    driver.get('http://www.naver.com')
    driver.maximize_window()
    time.sleep(2)
    driver.get(url)   # 글 띄우기

    # 크롤링

    try:
        # iframe 접근
        driver.switch_to_frame('mainFrame')

        target_info = {}

        # 제목 크롤링 시작
        overlays = ".se-fs-.se-ff-"
        tit = driver.find_element_by_css_selector(overlays)         # title
        title = tit.text
        title

        # 글쓴이 크롤링 시작
        overlays = ".nick"
        nick = driver.find_element_by_css_selector(overlays)         # nick
        nickname = nick.text

        # 날짜 크롤링
        overlays = ".se_publishDate.pcol2"
        date = driver.find_element_by_css_selector(overlays)         # date
        datetime = date.text

        # 내용 크롤링
        overlays = ".se-component.se-text.se-l-default"
        contents = driver.find_elements_by_css_selector(
            overlays)         # date

        content_list = []
        for content in contents:
            content_list.append(content.text)

        content_str = ' '.join(content_list)

        # 글 하나는 target_info라는 딕셔너리에 담기게 되고,
        target_info['title'] = title
        target_info['nickname'] = nickname
        target_info['datetime'] = datetime
        target_info['content'] = content_str

        # 각각의 글은 dict라는 딕셔너리에 담기게 됩니다.
        dict[i] = target_info
        time.sleep(1)

        print(i, title)

        # 글 하나 크롤링 후 크롬 창 닫기
        driver.close()

    # 에러나면 현재 크롬창 닫고 다음 글(i+1)로 이동
    except:
        driver.close()
        time.sleep(1)
        continue

    finally:
        close_browser(browser)

    # 중간,중간에 파일로 저장하기
    if i == 30 or 50 or 80:
        # 판다스로 만들기

        result_df = pd.DataFrame.from_dict(dict, 'index')

        # 저장하기
        result_df.to_excel(output_file)
        time.sleep(3)

print('수집한 글 갯수: ', len(dict))
print(dict)

# 판다스로 만들기
result_df = pd.DataFrame.from_dict(dict, 'index')

# 저장하기
result_df.to_excel(output_file)

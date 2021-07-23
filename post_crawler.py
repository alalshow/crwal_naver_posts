import sys
import os
import pandas as pd
import time
import numpy as np
from common.chrome import open_browser, close_browser, get_chrome_driver
from common.utils import remove_file, create_folder_not_remove
from url_crawler import get_urls
import arrow
from formal_changer import Changer


def get_df_posts(urls, output_file_path):

    dict_posts = {}  # 전체 크롤링 데이터를 담을 그릇
    model = Changer()

    # ★수집할 글 갯수
    number = 2
    for i in range(0, len(urls)):
        # 글 띄우기
        url = urls[i]
        print(url)
        browser = open_browser()
        driver = get_chrome_driver()

        # 사이트 주소는 네이버
        driver.get('http://www.naver.com')
        time.sleep(2)
        driver.get(url)   # 글 띄우기
        time.sleep(2)
        driver.maximize_window()

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

            formal_content_str = model.dechanger(content_str)

            # 글 하나는 target_info라는 딕셔너리에 담기게 되고,
            target_info['title'] = title
            target_info['nickname'] = nickname
            target_info['datetime'] = datetime
            target_info['content'] = formal_content_str

            # 각각의 글은 dict_posts라는 딕셔너리에 담기게 됩니다.
            dict_posts[i] = target_info
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

            result_df = pd.DataFrame.from_dict(dict_posts, 'index')

            # 저장하기
            result_df.to_excel(output_file_path)
            time.sleep(3)

    print('수집한 글 갯수: ', len(dict_posts))
    print(dict_posts)

    # 판다스로 만들기
    result_df = pd.DataFrame.from_dict(dict_posts, 'index')

    # 저장하기
    result_df.to_excel(output_file_path)

    return result_df


if __name__ == "__main__":

    # Step 0. 필요한 모듈과 라이브러리를 로딩하고 검색어를 입력 받습니다.
    query_txt = "이재용"
    start_date = "20210608"
    end_date = "20210614"
    page_count = 1

    today_foramt = arrow.now().format('YYYYMMDD')
    folder_path = f"output/{today_foramt}"
    create_folder_not_remove(folder_path)
    output_file_path = f"{folder_path}/posts_{query_txt}.xlsx"
    urls = get_urls(query_txt, start_date, end_date, page_count)
    df_posts = get_df_posts(urls, output_file_path)
    print(df_posts)

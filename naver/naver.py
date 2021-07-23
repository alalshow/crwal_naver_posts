from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyperclip


def naver_login(browser, naver_id, naver_pw):
    browser.maximize_window()
    browser.get('https://nid.naver.com/nidlogin.login')
    time.sleep(1)

    # 로그인 버튼을 찾고 클릭합니다
    # login_btn = browser.find_element_by_class_name('link_login')
    # login_btn.click()
    # time.sleep(1)

    # id, pw 입력할 곳을 찾습니다.
    tag_id = browser.find_element_by_name('id')
    tag_pw = browser.find_element_by_name('pw')
    tag_id.clear()
    time.sleep(1)

    # id 입력
    tag_id.click()
    pyperclip.copy(naver_id)
    tag_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # pw 입력
    tag_pw.click()
    pyperclip.copy(naver_pw)
    tag_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 로그인 상태 유지 선택
    keep_login = browser.find_element_by_xpath('//*[@id="label_login_chk"]')
    keep_login.click()

    # 로그인 버튼을 클릭합니다
    login_btn = browser.find_element_by_id('log.login')
    login_btn.click()
    time.sleep(2)
    return browser


def template_copy(browser, naver_id):  # 일반 답변
    browser.get(
        f"https://blog.naver.com/{naver_id}?Redirect=Write&categoryNo=0&editor=4")
    browser.maximize_window()
    time.sleep(3)
    browser.find_element_by_css_selector('li[data-name="template"]').click()
    # browser.find_element_by_class_name("se-template-toolbar-button").click()

    # search_input = browser.find_element_by_xpath('//*[@id="nx_query"]')
    # search_input.send_keys(keyword)
    # search_input.send_keys(Keys.ENTER)
    # time.sleep(1)
    # lista_elem = browser.find_elements_by_class_name("_searchListTitleAnchor")
    # links = []
    # for a in lista_elem:
    #     links.append(a.get_attribute("href"))
    # time.sleep(2)


def search_keyword(browser, keyword):  # 일반 답변
    browser.get("https://kin.naver.com/")
    browser.maximize_window()

    search_input = browser.find_element_by_xpath('//*[@id="nx_query"]')
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)
    time.sleep(1)
    lista_elem = browser.find_elements_by_class_name("_searchListTitleAnchor")
    links = []
    for a in lista_elem:
        links.append(a.get_attribute("href"))
    time.sleep(2)
    return browser, links


def get_answer_links(browser, keyword):  # 답변을 기다리는 질문
    browser.get(
        f"https://kin.naver.com/search/noAnswerList.nhn?query={keyword}")
    browser.maximize_window()
    time.sleep(1)

    lista_elem = browser.find_elements_by_class_name("_title")
    links = []
    for a in lista_elem:
        links.append(a.get_attribute("href"))
    time.sleep(2)
    print(links)
    return browser, links


def anwser(browser, links, answer_text, answer_link):
    for a in links:
        browser.get(a)
        time.sleep(1)
        try:
            browser.find_element_by_id('answerWriteButton').click()
            time.sleep(3)
            pyperclip.copy(answer_text)
            actions = ActionChains(browser)
            actions.key_down(Keys.CONTROL).send_keys('v').perform()
            time.sleep(1)
            pyperclip.copy(answer_link)
            actions = ActionChains(browser)
            actions.key_down(Keys.CONTROL).send_keys('v').perform()
            time.sleep(5)
            elem = browser.find_element_by_id('answerRegisterButton').click()
            time.sleep(60)
            print(elem)
            # browser.find_element_by_css('answerRegisterButton').click()
        except:
            print('답변 실패')
        finally:
            continue

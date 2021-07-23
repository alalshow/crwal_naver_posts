import time
import subprocess
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium import webdriver


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script(
        'return arguments[0].shadowRoot', element)
    return shadow_root


def download_location(driver):
    driver.get('chrome://settings/downloads')
    time.sleep(1)
    root1 = driver.find_element_by_tag_name('settings-ui')
    shadow_root1 = expand_shadow_element(driver, root1)
    root2 = shadow_root1.find_element_by_css_selector('#main')
    shadow_root2 = expand_shadow_element(driver, root2)
    root3 = shadow_root2.find_element_by_css_selector('settings-basic-page')
    shadow_root3 = expand_shadow_element(driver, root3)
    root4 = shadow_root3.find_element_by_css_selector(
        '#advancedPage > settings-section:nth-child(3) > settings-downloads-page')
    shadow_root4 = expand_shadow_element(driver, root4)
    download_path = shadow_root4.find_element_by_css_selector(
        '#defaultDownloadPath').text
    return download_path.replace("\\", "/")


def open_browser():

    browser = None

    try:
        browser = subprocess.Popen(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동
    except:
        browser = subprocess.Popen(
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

    return browser


def get_chrome_driver():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # 알림창 끄기
    # options.add_argument('--disable-notifications')
    # options.add_argument("--disable-infobars")
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome(
            f'./{chrome_ver}/chromedriver.exe', options=options)
    except:
        chromedriver_autoinstaller.install('./')
        driver = webdriver.Chrome(
            f'./{chrome_ver}/chromedriver.exe', options=options)
    driver.implicitly_wait(15)  # 페이지가 로딩될 때 까지 10초동안 대기
    driver.set_page_load_timeout(30)
    return driver


def close_browser(browser):
    try:
        # driver.quit()
        browser.kill()
    except:
        pass


def remove_alert(browser):
    try:
        result = browser.switch_to_alert()
        print(result.text)

        # # alert 창 확인
        # result.accept()

        # alert 창 끄기
        result.dismiss()
    except:
        "There is no alert"


if __name__ == "__main__":
    browser = open_browser()
    time.sleep(3)
    # driver = get_chrome_driver()
    # driver.get("www.naver.com")
    browser.kill()

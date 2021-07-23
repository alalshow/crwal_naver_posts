from naver.naver import naver_login, template_copy
from common.chrome import open_browser, close_browser, get_chrome_driver, remove_alert
import time

if __name__ == "__main__":
    print("====start crawling====")
    browser = open_browser()
    driver = get_chrome_driver()
    naver_login(driver, "alalshow2", "rhxh123!")
    template_copy(driver, "alalshow2")
    time.sleep(1222)

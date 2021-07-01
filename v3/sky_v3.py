from tkinter import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui, expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import winsound
import simpleaudio as sa
import requests
import time
from datetime import datetime
import msvcrt as m
import ctypes  # An included library with Python install.
from curl_api_3 import make_form_call_to_api
import random
import threading
# sound alert
duration = 5000  # milliseconds
freq = 440  # Hz
paralell = 0
# gaußsche Summe + 1000

# 1286_

# 1286_1230_758065 - 27.11. - 12861230758065 - 56
# 1286_1288_831116 - 25.11. - 12861288831116 - 1288 - 2
# 1286_1287_829828 - 24.11. - - 35658 - 1
# 1286_1259_794170 - 23.11. 27
# 1285 - 1255 - 789140
old_href_id = "825970"  # 831116 = real number


class AnyEc:
    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver):
                    return True
            except Exception as err:
                print(err)
                pass


def check_exists_by_link_text(link_text):
    try:
        driver.find_element_by_partial_link_text(link_text)
    except NoSuchElementException:
        return False
    return True


def get_new_url(href):
    print(href)
    # new_id = href.rpartition('-')[2]
    new_link = 'https://extra.sky.de/sweepstakes/sky-be-surprised-' + href
    print('~~~~~~~~~~~~~~  ' + new_link + '  ~~~~~~~~~~~~~~')
    return new_link


def find(driver):
    presence = EC.presence_of_element_located(
        (By.XPATH, "//*[@id='modal-content']/div"))
    # text = EC.text_to_be_present_in_element(
    #    (By.XPATH, '//*[@id="modal-content"]/div'), "kein" or "nvalid" or "geschlossen")  # erfolgreich oder teilgenommen

    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="modal-content"]/div[@class="progress-bar"]')))
    print('>> progress bar not present anymore')

    WebDriverWait(driver, 10).until(AnyEc(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="modal-content"]/div'), "geschlossen"),
        EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="modal-content"]/div'), "kein"),
        EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="modal-content"]/div'), "nvalid"),
        EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="modal-content"]/div'), "erfolgreich")
    ))

    result_elem = driver.find_element_by_xpath(
        '//*[@id="modal-content"]/div').text
    print('>> TEXT >> ' + result_elem)

    if presence and True:  # text
        return True
    else:
        return False


def request_in_thread(cookies, lottery_id, gauß, first_num, form_num):
    start = time.time()
    res_1 = make_form_call_to_api(
        cookies, lottery_id, gauß, first_num, form_num)
    end = time.time()
    print(
        f"\n############################################################################################\n>> {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}: \n      - response: {res_1}\n      - duration: {round((end-start),2)} second(s)\n#############################################################################################\n")
    try:
        file = open("crawl_api_log", "a")
        file.write(
            f"\n############################################################################################\n>> {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}: \n      - response: {res_1}\n      - duration: {round((end-start),2)} second(s)\n#############################################################################################\n")
        file.close()
    except Exception:
        print("Exception thrown while writing into log-file.")
    return


def run_script():

    driver = webdriver.Chrome()
    driver.delete_all_cookies()
    driver.get("https://extra.sky.de/")
    driver.maximize_window()

    try:
        input("Press enter after login!")
    except SyntaxError:
        pass

    driver.minimize_window()
    # get cookies after login.

    last_refresh = time.time()
    while(1 == 1):
        if((time.time() - last_refresh) > 300):
            driver.refresh()
            cookies = driver.get_cookies()
        else:
            cookies = driver.get_cookies()
        try:

            # parallel
            if (paralell == 1):
                t1 = threading.Thread(target=request_in_thread, args=(
                    cookies, "827255", "1285", "1286", "form-Ne6KjrGjFKzpf8PdrO4_RYGwgIRlko0OpPFaOvWpnC"))
                t1.name = "1286er-thread"
                t1.start()
            else:
                request_in_thread(cookies, "827255", "1285", "1286",
                                  "form-Ne6KjrGjFKzpf8PdrO4_RYGwgIRlko0OpPFaOvWpnC")

        except Exception as excep:
            print(f"---- exception {excep}")
            exit()

        time.sleep(2)

    # ps5_btn_2_parent.click()

    # html.js body.navbar-is-fixed-top.html.front.not-logged-in.no-sidebars.page-node.page-node-.page-node-21.node-type-page.i18n-de div#content-wrapper.content-wrapper div.main-container.container div.row section.col-sm-12 div.region.region-content section#block-member-api-rewards.block.block-member-api.clearfix div.page-category div.content-category div.content-group-1 div.newRow.highlight div.pdimg.content-row-1.content-row-twocolom1.content-row.col-sm-12.content-row-first.history-show div.content-row-twocolom div.content-field.content-field-node span.field-content a.active

    driver.close()
    return


def main():
    print("####### Running main function #####")
    run_script()
    print("####### Script ended at this time #####")


if __name__ == "__main__":
    main()

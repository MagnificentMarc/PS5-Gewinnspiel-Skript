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
import ctypes 
from curl_api_2 import make_form_call_to_api
import threading
from bs4 import BeautifulSoup


# sound alert settings
duration = 5000  # milliseconds
freq = 440  # Hz


# ############### Old hrefs #################################
# Berechnet über Gaußsche Summenformel
# 1286_1284_825970 - 30.11.
# 1286_1230_758065 - 27.11. - 12861230758065 - 56
# 1286_1288_831116 - 25.11. - 12861288831116 - 1288 - 2
# 1286_1287_829828 - 24.11. - - 35658 - 1
# 1286_1259_794170 - 23.11. 27
# 1285 - 1255 - 789140
old_href_id = "825970"  # 831116 = real number


class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """

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

    """WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@id="modal-content"]/div'), "geschlossen"))"""

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


def request_in_thread_2(cookies, url, waitingTime, form_id):
    time.sleep(waitingTime)
    try:
        lottery_id = url.split("_")[-1]
        gauß = url.split("_")[1]
        first_num = url.split("-")[-1].split("_")[0]
    except Exception:
        print('Couldnt split! Split Error!')
        return
    start = time.time()
    res_2 = make_form_call_to_api(
        cookies, lottery_id, gauß, first_num, form_id)
    end = time.time()
    print(
        f"\n############################################################################################\n>> {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}: \n      - response: {res_2}\n      - duration: {round((end-start),2)} second(s)\n#############################################################################################\n")
    return


# #################### Chrome Settings ####################
chrome_options = Options()
chrome_options.add_argument("--headless")
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
cookies = driver.get_cookies()

# create session with cookies
s = requests.Session()
for cookie in cookies:
    # print(cookie)
    s.cookies.set(cookie['name'], cookie['value'])

found_new_href = 0
new_href = ''

while(1 == 1):
    print('First: sleep 1s')
    time.sleep(1)
    if(found_new_href == 0):
        # with curl
        print('##############################################################################################')
        start = time.time()
        try:
            response = s.get("https://extra.sky.de/")
        except Exception as exc:
            print('Error in Request!!!')
            print(exc)
            continue

        end = time.time()
        print(f"- Extra-Seite geladen in {round((end-start),2)} Sekunden.")

        if('Reserviere dir eine Sony PlayStation' in response.text):
            # parse it with beautiful soup:

            soup = BeautifulSoup(response.text, 'html.parser')
            # test = soup.find('Reserviere dir eine Sony PlayStation')
            test = "null"

            for item in soup.find_all("a", href=True):
                if ("Reserviere" in item.text):
                    test = item
                else:
                    continue

            new_id = test['href'].split("-")[-1]
            print('> Reservierungselement existiert')
            if(old_href_id in new_id):
                print('old link.')
            else:
                print('new link.')
                found_new_href = 1
                new_href = get_new_url(new_id)

                # start threads with direct api call:
                thread_1 = threading.Thread(
                    target=request_in_thread_2, args=(cookies, new_href, 0, "form-Ne6KjrGjFKzpf8PdrO4_RYGwgIRlko0OpPFaOvWpnC"))
                thread_1.start()

                thread_2 = threading.Thread(
                    target=request_in_thread_2, args=(cookies, new_href, 0, "form-bPMfg58z1FwiaBJRGG4azyxyiiUqVo0MHITty9SiyuU"))
                thread_2.start()
                # play sound
                wave_obj = sa.WaveObject.from_wave_file("alert.wav")
                play_obj = wave_obj.play()

        else:
            print('> Reservierungselement existiert nicht')

        print(f"- {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} >> Request-duration:" +
              str(round((end - start), 2)) + " Sec")

        print('##############################################################################################')
    else:
        print('>>>> (re)Locate Browser to new_href!')
        print(new_href)
        driver.get(new_href)

        if "Jetzt reservieren" in driver.page_source:
            print('>> Reservierungsseite')
            try:
                # Click Reservierungsbutton und AGB-Zustimmung
                jetzt_reservieren_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[4]/div/div/section/div/section[1]/div[3]/div/div/div[4]/div/div/p/button"))).click()
                zustimmen_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, 'ctools_ss_form'))).click()

                # waits until result-text appeared.
                WebDriverWait(driver, 30).until(find)
                res = driver.find_element_by_xpath(
                    '//*[@id="modal-content"]/div').text
                print('#### res => ' + res)

                # checks if attempt was successfull
                if(('kein' in res) or ('nvalid' in res) or ('geschlossen' in res)):
                    print(
                        f"- {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} >> negatives Resultat:  {res}")
                    driver.maximize_window()
                    continue
                else:
                    print(
                        f"- {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} >> positives Resultat:  {res}")
                    driver.maximize_window()
                    try:
                        # Falls erfolgreich => Fülle die Form aus
                        salutation = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            By.XPATH, "//*[@id='edit-salutation--2']"))).select_by_value("0")
                        vorname_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            By.XPATH, "//*[@id='edit-firstname--2']")).send_keys("VORNAME")
                        nachname_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            By.XPATH, "//*[@id='edit-lastname--2']")).send_keys("NACHNAME")
                        mail_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            By.XPATH, "//*[@id='edit-email--2']")).send_keys("E-MAIL")
                        # value "0" => 1 PS5
                        anzahl_feld = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            By.XPATH, "//*[@select='edit-sky-amount--2']"))).select_by_value("0")

                        # Submit
                        submit_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                            By.XPATH, "//*[@id='participate_ss']")).click()

                        # Explicit Wait/Sleep
                        time.sleep(300)
                    except Exception as error:
                        print("error when selecting further details.")
                        print(error)
                        time.sleep(500)
                    
            except Exception as err:
                exception_type = type(err).__name__
                print(err)
                # Fehler passiert => nächste Iteration mit Href-Abfrage
                continue
        else:
            # Fehler passiert => nächste Iteration mit Href-Abfrage
            continue  # new iteration

        print('##############################################################################################')


time.sleep(300)
driver.close()

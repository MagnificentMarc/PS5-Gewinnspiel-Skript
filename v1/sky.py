from tkinter import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui, expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import winsound


import time
import msvcrt as m
import ctypes  

# sound alert
duration = 5000  # milliseconds
freq = 440  # Hz

old_href_id = "829828"  # 829828 = real number


def check_exists_by_link_text(link_text):
    try:
        driver.find_element_by_partial_link_text(link_text)
    except NoSuchElementException:
        return False
    return True


def get_new_url(href):
    print(href)
    new_id = href.rpartition('-')[2]
    return 'https://extra.sky.de/sweepstakes/sky-be-surprised-' + new_id


def find(driver):
    presence = EC.presence_of_element_located(
        (By.XPATH, "//*[@id='modal-content']/div"))
    text = EC.text_to_be_present_in_element(
        (By.XPATH, '//*[@id="modal-content"]/div'), "kein" or "nvalid")  # erfolgreich oder teilgenommen

    if presence and text:
        return True
    else:
        return False

# check login
start_dialogue_answer = ctypes.windll.user32.MessageBoxW(
    0, "Python will now start ", "Sky/Medion script v1.0", 4)

if start_dialogue_answer == 6:
    print('said yes')
else:
    print('said no.')
    exit()


driver = webdriver.Firefox()
driver.get("https://extra.sky.de/")
driver.maximize_window()
driver.execute_script(
    'alert("Further instructions -- a.) Accept cookies, b.) Log into your sky account, c.) Hit enter in the console ")')


try:
    input("Press enter after login!")
except SyntaxError:
    pass

found_new_href = 0
new_href = ''

while(1 == 1): 
    if(found_new_href == 0):
        driver.get("https://extra.sky.de/")
        if(check_exists_by_link_text("Reserviere dir eine Sony PlayStation")):
            print('>> PS5-Reservierungselement existiert')
            ps5_btn_2 = driver.find_element_by_partial_link_text(
                "Reserviere dir eine Sony PlayStation")
            href = ps5_btn_2.get_attribute('href')
        else:
            href = old_href_id
            print('>> PS5-Banner existiert nicht. (Start new Iteration)')
            time.sleep(0.2)
            continue

        # handle href identifier (either old numbers => wait + skip, or new id + go to link an get that damn ps5)
        if(old_href_id in href):
            print('>> is old link')
            print(href)
        else:
            found_new_href = 1  # while loop will end after this iteration.
            new_href = get_new_url(href)
            print('>> new Link is: ' + new_href)
            winsound.Beep(freq, duration)

        # make browser wait 1 sec before checking again
        print('>> now sleeping for 1 sec')
    # time.sleep(1)
    else:
        # direct to new link
        driver.get(new_href)
        if "Jetzt reservieren" in driver.page_source:
            # Reservierungsseite existiert
            try:
                # Versuche Reservierungsbutton zu klicken 
                jetzt_reservieren_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[4]/div/div/section/div/section[1]/div[3]/div/div/div[4]/div/div/p/button"))).click()

                # Versuche AGB-Zustimmung zu klicken
                zustimmen_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'ctools_ss_form'))).click()

                # 
                result_text_ele = WebDriverWait(driver, 10).until(find)

            except Exception as err:
                # Catch all errors.
                exception_type = type(err).__name__
                print('EX >> Couldnt grab jetzt-reservieren-button')
                print(err)
                continue

            # jetzt_reservieren_btn = driver.find_element_by_xpath(
            #   "/html/body/div[4]/div/div/section/div/section[1]/div[3]/div/div/div[4]/div/div/p/button")

        else:
            continue  # new iteration
# ps5_btn_2_parent.click()


# html.js body.navbar-is-fixed-top.html.front.not-logged-in.no-sidebars.page-node.page-node-.page-node-21.node-type-page.i18n-de div#content-wrapper.content-wrapper div.main-container.container div.row section.col-sm-12 div.region.region-content section#block-member-api-rewards.block.block-member-api.clearfix div.page-category div.content-category div.content-group-1 div.newRow.highlight div.pdimg.content-row-1.content-row-twocolom1.content-row.col-sm-12.content-row-first.history-show div.content-row-twocolom div.content-field.content-field-node span.field-content a.active
time.sleep(30)
driver.close()

import requests
import json
from bs4 import BeautifulSoup
import traceback


def make_call_to_form(cookies, lottery_id, gauß_num, first_num, form_num):
    first_num = first_num
    lottery_id = lottery_id
    gauß_num = gauß_num

    # generate url to be posted to.
    # cookies will be applied from selenium browser.
    url_dynamic = f"https://extra.sky.de/sweepstakes/sky-be-surprised-{first_num}_{gauß_num}_{lottery_id}"
    # print(f">> POST TO URL: {url_dynamic}")
    result_json = "null"
    return


def make_form_call_to_api(cookies, lottery_id, gauß_num, first_num, form_num):
    # replace if it changes next week
    first_num = first_num
    lottery_id = lottery_id
    gauß_num = gauß_num

    # generate url to be posted to.
    # cookies will be applied from selenium browser.
    url_dynamic = f"https://extra.sky.de/sweepstakes/sky-be-surprised-{first_num}_{gauß_num}_{lottery_id}"
    # print(f">> POST TO URL: {url_dynamic}")
    result_json = "null"
    sess_cookie = ""

    s = requests.Session()
    try:
        for cookie in cookies:
            # print(
            #    f"\nCookie-name: {cookie['name']}, Cookie-Value: {cookie['value']}")
            s.cookies.set(cookie['name'], cookie['value'])
    except Exception:
        # print(f"> Error occured while entering cookies into session: {exc}")
        result_json = {"code": 999, "result": "cookie preparation error",
                       "bool": False, "url": url_dynamic}
        return {"code": 999, "result": "cookie preparation error", "bool": False, "url": url_dynamic}

    headers = {
        'authority': 'extra.sky.de',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://extra.sky.de',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': f'{url_dynamic}',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    headers2 = {
        'authority': 'extra.sky.de',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://extra.sky.de',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://extra.sky.de/sweepstakes/sky-be-surprised-1286_1284_825970',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'KNOWN_USER=NOWTV:NOWTV:DE; skyTrackingPermission=false; cHash=869024e494b937d889b728384676f2250814487a5d54a24f28e38648e1bc1c1e; waSky.online=timestampSecsLastPage^>^>1606144874^]^[loginStatus^>^>logout^]^[loginString^>^>logout^]^[wkzEntryPage^>^>direct type in^]^[wkzPath^>^>direct type in^>^>30^>^>191120^]^[crmString^>^>free::direct type in::direct type in::^]^[currentPage^>^>home_index.jsp^]^[currentChannel^>^>basisseite - soso - home; waSky.consent.purposes=^' + "{^%^22essential^%^22:true^%^2C^%^22optimierung^%^22:true^%^2C^%^22personal^%^22:false^%^2C^%^22marketing^%^22:false^};" + f'optimizelyEndUserId=oeu1606197126875r0.156374443852902; optimizelyEndUserId=oeu1606197126875r0.156374443852902; RT=^\\^z=1^&dm=sky.de^&si=cc6f25ac-7cb7-4364-932c-ca3970f8054f^&ss=khvtjvb6^&sl=3^&tt=23i^&bcn=^%^2F^%^2F6852bd07.akstat.io^%^2F^&ld=9rs^&ul=btn^&hd=btr^\\^; SSESSba44b5fa62f75eccf2c22d74dc60b366={sess_cookie}; SESSba44b5fa62f75eccf2c22d74dc60b366=I5hNE78cefrgDpTDUeRJ1tdZ5LBjCSNwx1dibaf1fUc; TRADEDOUBLER=^\\^7a47b3cb4cfce0c3ee3c6ef9ba2a9239^#tduid=7a47b3cb4cfce0c3ee3c6ef9ba2a9239^&url=https://www.sky.de/mein-sky/sky-extra-174018?f=0^&wkz=WATD01^&eml=1408940_myDealZ.de+-+Der+Schn^%^C3^%^A4ppchenblog+mit+z^#Fri',
    }


    data = {
        'salutation': '0',
        'firstname': 'MARC',
        'lastname': 'OREL',
        'email': 'marc1.orel@st.oth-regensburg.de',
        'sky_amount': '0',
        'ss_fields_api': '{"salutation": "0", "firstname":"MARC","lastname":"OREL", "email":"marc1.orel@st.oth-regensburg.de", "sky_amount":"0"}',
        'lotteryId': f'{lottery_id}',
        'ss_successtext': 'Thank you for your registration. You will receive all further information shortly by e-mail.',
        'op': 'Teilnehmen',
        'form_build_id': f'{form_num}',
        'form_id': 'participate_ss_form'
    }

    # create session with cookies

    try:

        response_2 = s.post(
            f'https://extra.sky.de/ssform/{lottery_id}', headers=headers, data=data)
        with open("ssform_response.txt", 'wb') as fd:
            for chunk in response_2.iter_content(100):
                fd.write(chunk)
        try:
            new_response = response_2.text.replace("\\u003E", ">")
            new_response = new_response.replace("\\u003C", "<")
            new_response = new_response.replace("\\u0022", '"')
            new_response = new_response.replace("\\n", '')
            new_response = new_response.replace("\\/", '\\')
            new_response = new_response.replace("\\u0026", '&')
            new_response = new_response.replace("&quot;", '"')
            new_response = new_response.replace("\\u00f6", 'ö')
            form_build_id = new_response.split(
                'name="form_build_id" value="')[-1].split('" /><input')[0]
        except Exception as splitError:
            print(f'error in split, {splitError}')

        if not ("form_build_id" in response_2.text):
            print("-- ssform: invalid")
            data = {
                'salutation': '0',
                'firstname': 'MARC',
                'lastname': 'OREL',
                'email': 'marc1.orel@st.oth-regensburg.de',
                'sky_amount': '0',
                'ss_fields_api': '{"salutation": "0", "firstname":"MARC","lastname":"OREL", "email":"marc1.orel@st.oth-regensburg.de", "sky_amount":"0"}',
                'lotteryId': f'{lottery_id}',
                'ss_successtext': 'Thank you for your registration. You will receive all further information shortly by e-mail.',
                'op': 'Teilnehmen',
                'form_build_id': f'{form_num}',
                'form_id': 'participate_ss_form'
            }
        else:
            print("-- ssform: successfull")
            data = {
                'salutation': '0',
                'firstname': 'MARC',
                'lastname': 'OREL',
                'email': 'marc1.orel@st.oth-regensburg.de',
                'sky_amount': '0',
                'ss_fields_api': '{"salutation": "0", "firstname":"MARC","lastname":"OREL", "email":"marc1.orel@st.oth-regensburg.de", "sky_amount":"0"}',
                'lotteryId': f'{lottery_id}',
                'ss_successtext': 'Thank you for your registration. You will receive all further information shortly by e-mail.',
                'op': 'Teilnehmen',
                'form_build_id': f'{form_build_id}',
                'form_id': 'participate_ss_form'
            }

        # print(form_build_id)
        # response_2.text.replace(u"\u0022", '"')
        # print(response_2.text)

        response = s.post(
            f'https://extra.sky.de/sweepstakes/sky-be-surprised-{first_num}_{gauß_num}_{lottery_id}', headers=headers, data=data2)

        # https://extra.sky.de/sweepstakes/sky-be-surprised-
        print(
            f">> Status_code of api call to url {url_dynamic}: {response.status_code}")
    except Exception as exce:
        print(exce)
        print(" => error while posting to api.")
        result_json = {"code": 400, "result": "error",
                       "bool": False, "url": url_dynamic}
        return {"code": 400, "result": "error", "bool": False, "url": url_dynamic}
    # https://extra.sky.de/sweepstakes/sky-be-surprised-1286_1244_775390
    # https://extra.sky.de/ssform/775390

    if("The shot probably went backwards" in response.text):
        result_json = {"code": response.status_code,
                       "result": "not existing", "bool": False, "url": url_dynamic}
        return {"code": response.status_code, "result": "not existing", "bool": False, "url": url_dynamic}
    else:
        result_json = {"code": response.status_code,
                       "result": "success", "bool": True, "url": url_dynamic}
        return {"code": response.status_code, "result": "success", "bool": True, "url": url_dynamic}

    file = open("crawl_api_log", "ab")
    file.write(result_json)
    file.close()
    # print(response.text)


# make_form_call_to_api("", "775390", "1244", "")

# response = requests.post('https://extra.sky.de/sweepstakes/sky-be-surprised-1286_1230_758065', headers=headers, cookies=cookies, data=data)
# gaußsche Summe + 1000
# 1286_
# 1286_1230_758065 - 27.11. - 12861230758065 - 56
# 1286_1288_831116 - 25.11. - 12861288831116 - 1288 - 2
# 1286_1287_829828 - 24.11. - - 35658 - 1
# 1286_1259_794170 - 23.11. 27
# 1285 - 1255 - 789140
"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()
    # headl_driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.delete_all_cookies()
    driver.get("https://extra.sky.de/")
    driver.maximize_window()
        driver.minimize_window()
    # get cookies after login.
    cookies = driver.get_cookies()
"""

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
    result_json = "null"
    sess_cookie = ""

    # get session information
    s = requests.Session()

    try:
        # set session cookies to session
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
    except Exception:
        # Error handling, if cookies could not be set.
        result_json = {"code": 999, "result": "cookie preparation error",
                       "bool": False, "url": url_dynamic}
        return {"code": 999, "result": "cookie preparation error", "bool": False, "url": url_dynamic}

    # header/data/body template for HTTP calls.
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
    data = {
        'salutation': '0',
        'firstname': 'VORNAME',
        'lastname': 'NACHNAME',
        'email': 'EMAIL',
        'sky_amount': '0',
        'ss_fields_api': '{"salutation": "0", "firstname":"VORNAME","lastname":"NACHNAME", "email":"EMAIL", "sky_amount":"0"}',
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
            # log response in .txt file.
            for chunk in response_2.iter_content(100):
                fd.write(chunk)
        try:
            # manual decoding
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
            # Gewinnspiel wurde nicht gewonnen
            print("-- ssform: invalid")
            reason = ""
            if("Invalid" in response_2.text):
                reason = "Invalid ID"
            if("Too many" in response_2.text):
                reason = "too many requests"
            if("kein" in response_2.text):
                reason = "kein gewinn mehr verfügbar"
            if("geschlossen" in response_2.text):
                reason = "gewinnspiel geschlossen"

            print(
                f">> Status_code of api call to url {url_dynamic}: no request made (invalid ticket)\n - status_code: {response_2.status_code}\n - reason: {reason}")
            return
        else:
            # Gewinnspiel wurde gewonnen
            print("-- ssform: successfull")
            data = {
                'salutation': '0',
                'firstname': 'Vorname',
                'lastname': 'Nachname',
                'email': 'E-Mail',
                'sky_amount': '0',
                'ss_fields_api': '{"salutation": "0", "firstname":"Vorname","lastname":"Nachname", "email":"E-Mail", "sky_amount":"0"}',
                'lotteryId': f'{lottery_id}',
                'ss_successtext': 'Thank you for your registration. You will receive all further information shortly by e-mail.',
                'op': 'Teilnehmen',
                'form_build_id': f'{form_build_id}',
                'form_id': 'participate_ss_form'
            }
            # Gewinnspielteilnahme => Persönliche Datenabsenden
            response = s.post(
                f'https://extra.sky.de/sweepstakes/sky-be-surprised-{first_num}_{gauß_num}_{lottery_id}', headers=headers, data=data)
            print(
                f">> Status_code of api call to url {url_dynamic}: {response.status_code}")
    except Exception as exce:
        print(exce)
        print(" => error while posting to api.")
        result_json = {"code": 400, "result": "error",
                       "bool": False, "url": url_dynamic}
        return {"code": 400, "result": "error", "bool": False, "url": url_dynamic}

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



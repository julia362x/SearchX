import base64
import re
import requests

from lxml import etree
from urllib.parse import urlparse, parse_qs

import time
import cloudscraper
from bs4 import BeautifulSoup

from bot import APPDRIVE_EMAIL, APPDRIVE_PASS, GDTOT_CRYPT, HUBDRIVE_CRYPT, DRIVEHUB_CRYPT
from bot.helper.ext_utils.exceptions import DDLException

account = {
    'email': APPDRIVE_EMAIL, 
    'passwd': APPDRIVE_PASS
}

def account_login(client, url, email, password):
    data = {
        'email': email,
        'password': password
    }
    client.post(f'https://{urlparse(url).netloc}/login', data=data)

def gen_payload(data, boundary=f'{"-"*6}_'):
    data_string = ''
    for item in data:
        data_string += f'{boundary}\r\n'
        data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
    data_string += f'{boundary}--\r\n'
    return data_string

def appdrive(url: str) -> str:
    if (APPDRIVE_EMAIL or APPDRIVE_PASS) is None:
        raise DDLException("APPDRIVE_EMAIL and APPDRIVE_PASS env vars not provided")
    client = requests.Session()
    client.headers.update({
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    })
    account_login(client, url, account['email'], account['passwd'])
    res = client.get(url)
    try:
        key = re.findall(r'"key",\s+"(.*?)"', res.text)[0]
    except IndexError:
        raise DDLException("Invalid link")
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
    info = {}
    info['error'] = False
    info['link_type'] = 'login'  # direct/login
    headers = {
        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
    }
    data = {
        'type': 1,
        'key': key,
        'action': 'original'
    }
    if len(ddl_btn):
        info['link_type'] = 'direct'
        data['action'] = 'direct'
    while data['type'] <= 3:
        try:
            response = client.post(url, data=gen_payload(data), headers=headers).json()
            break
        except:
            data['type'] += 1
    if 'url' in response:
        info['gdrive_link'] = response['url']
    elif 'error' in response and response['error']:
        info['error'] = True
        info['message'] = response['message']

    if urlparse(url).netloc == 'driveapp.in' and not info['error']:
        res = client.get(info['gdrive_link'])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
        info['gdrive_link'] = drive_link
    
    if urlparse(url).netloc == "gdflix.pro" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivesharer.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivebit.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivelinks.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "driveace.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if urlparse(url).netloc == "drivepro.in" and not info["error"]:
        res = client.get(info["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn')]/@href"
        )[0]
        info["gdrive_link"] = drive_link
    
    if not info['error']:
        return info['gdrive_link']
    else:
        raise DDLException(f"{info['message']}")

def gdtot(url: str) -> str:
    if GDTOT_CRYPT is None:
        raise DDLException("GDTOT_CRYPT env var not provided")
    client = requests.Session()
    client.cookies.update({'crypt': GDTOT_CRYPT})
    res = client.get(url)
    res = client.get(f"https://new.gdtot.nl/dld?id={url.split('/')[-1]}")
    url = re.findall(r'URL=(.*?)"', res.text)[0]
    info = {}
    info['error'] = False
    params = parse_qs(urlparse(url).query)
    if 'gd' not in params or not params['gd'] or params['gd'][0] == 'false':
        info['error'] = True
        if 'msgx' in params:
            info['message'] = params['msgx'][0]
        else:
            info['message'] = 'Invalid link'
    else:
        decoded_id = base64.b64decode(str(params['gd'][0])).decode('utf-8')
        drive_link = f'https://drive.google.com/open?id={decoded_id}'
        info['gdrive_link'] = drive_link
    if not info['error']:
        return info['gdrive_link']
    else:
        raise DDLException(f"{info['message']}")


def gplinks(url: str):
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        p = urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'

        res = client.head(url)
        header_loc = res.headers['location']
        param = header_loc.split('postid=')[-1]
        req_url = f'{p.scheme}://{p.netloc}/{param}'

        p = urlparse(header_loc)
        ref_url = f'{p.scheme}://{p.netloc}/'

        h = { 'referer': ref_url }
        res = client.get(req_url, headers=h, allow_redirects=False)

        bs4 = BeautifulSoup(res.content, 'html.parser')
        inputs = bs4.find_all('input')
        data = { input.get('name'): input.get('value') for input in inputs }

        h = {
            'referer': ref_url,
            'x-requested-with': 'XMLHttpRequest',
        }
        time.sleep(10)
        res = client.post(final_url, headers=h, data=data)
        return res.json()['url'].replace('\/','/')

    except Exception: 
        err_msg =  'Something went wrong :('
        raise DDLException(f"{err_msg}")

def linkvertise(url: str):
    _apiurl = f"https://bypass.bot.nu/bypass2?url={url}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    try:
        resp = requests.get(_apiurl, headers=headers)
        if resp.status_code == 200:
            jresp = resp.json()
            bypassed = jresp["destination"]
            return bypassed

        elif resp.status_code == 404:
            jresp = resp.json()
            msg = jresp["msg"]
            plugin = jresp["plugin"]
            err_msg = f"{msg}\n\nPlugin : {plugin}"
            raise DDLException(err_msg)

        else:
            err_msg = f"API Status Code {str(resp.status_code)}"
            raise DDLException(err_msg)
    except Exception as e:
        raise DDLException(f"Error : {e}")

def hubdrive(url: str) -> str:
    if 'hubdrive' in url:
        if HUBDRIVE_CRYPT is None:
            raise DDLException("ERROR: HubDrive CRYPT cookie not provided")
    elif 'drivehub' in url:
        if DRIVEHUB_CRYPT is None:
            raise DDLException("ERROR: DriveHub CRYPT cookie not provided")        
    try:
        with requests.Session() as client:
            if 'hubdrive' in url:
                client.cookies.update({"crypt": HUBDRIVE_CRYPT})
            elif 'drivehub' in url:
                client.cookies.update({"crypt": DRIVEHUB_CRYPT})
            res = client.get(url)
            up = urlparse(url)
            req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
            file_id = url.split("/")[-1]
            data = {"id": file_id}
            headers = {"x-requested-with": "XMLHttpRequest"}
        try:
            res = client.post(req_url, headers=headers, data=data).json()["file"]
            gd_id = re.findall("gd=(.*)", res, re.DOTALL)[0]
        except BaseException:
            raise DDLException(
                "ERROR: Try in your broswer, mostly file not found or user limit exceeded!"
            )
        return f"https://drive.google.com/open?id={gd_id}"

    except BaseException:
        raise DDLException(f"Unable to Extract GDrive Link")
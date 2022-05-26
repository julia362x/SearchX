import re
import threading

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def is_gdrive_link(url: str):
    return "drive.google.com" in url

def is_appdrive_link(url: str):
    #url = re.match(r'https?://(appdrive|driveapp)\.in/\S+', url) #|drivehub|gdflix|drivesharer|drivebit|drivelink|driveace|drivepro
    #return bool(url)
    return "appdrive" in url or "driveapp" in url or "gdflix" in url or "drivesharer" in url or "drivebit" in url or "drivelink" in url or "driveace" in url or "drivepro" in url

def is_gdtot_link(url: str):
    url = re.match(r'https?://.+\.gdtot\.\S+', url)
    return bool(url)

def is_hubdrive_link(url: str):
    '''url = re.match(r'https?://hubdrive\.\S+', url)
    return bool(url)'''
    return "hubdrive" in url or "drivehub" in url

def is_gplink_link(url: str):
    url = re.match(r'https?://gplinks\.\S+', url)
    return bool(url)

def is_bitly_link(url: str):
    url = re.match(r'https?://bit\.ly\S+', url)
    return bool(url)

def is_linkvertise_link(url: str):
    return "linkvertise" in url or "link-to.net" in url or "direct-link.net" in url or "up-to-down.net" in url or "filemedia.net" in url or "file-link.net" in url or "link-hub.net" in url or "link-center.net" in url or "link-target.net" in url

def new_thread(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

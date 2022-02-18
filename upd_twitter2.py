import urllib.request
import urllib.parse
import urllib.error
import ssl
import json
import twurl


# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def creating_file(nickname:str):
    '''
    The function that creates the JSON file using the nickname from twitter.
    '''
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': nickname, 'count': '100'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    data = json.loads(data)
    with open('info.json', 'w',encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

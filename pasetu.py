from requests.packages import urllib3
import re
import requests
import warnings
import json
import os

warnings.filterwarnings("ignore")

urllib3.disable_warnings()

urls = ['https://image.anosu.top/pixiv/direct?r18=1&num=30', 'https://moe.jitsu.top/r18', 'https://api.lolicon.app/setu/v2?r18=1&num=10'] # , 'https://sex.nyan.xyz/api/v2/img?num=10&r18=true']
num = 0

def download_image(url, num):
    a = requests.get(url)
    try:
        a.raise_for_status()
        filename = '%d.png' % num
        filepath = './setu/%s' % filename
        while os.path.exists(filepath):
            num += 1
            filename = '%d.png' % num
            filepath = './setu/%s' % filename
        with open(filepath, 'wb') as f:
            f.write(a.content)
        print('%s is ok' % filename)
    except Exception as e:
        print(f'Error downloading image: {str(e)}')

try:
    while True:
        for url in urls:
            try:
                response = requests.get(url)
                content_type = response.headers.get('Content-Type')
                if content_type.find('application/json') != -1:
                    data = response.json()
                    links = [item['urls']['original'] for item in data['data']]
                    for link in links:
                        download_image(link, num)
                        num += 1
                else:
                    download_image(url, num)
                    num += 1
            except Exception as e:
                print(f'Error accessing URL: {str(e)}')
                num = 0
except KeyboardInterrupt:
    pass

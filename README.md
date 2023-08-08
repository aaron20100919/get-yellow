# get-yellow
用python爬取涩图

### 首先上效果
```
...
293.png is ok
Error accessing URL: HTTPSConnectionPool(host='pixiv.yuki.sh', port=443): Max retries exceeded with url: /img-original/img/2022/05/07/13/40/23/98170194_p0.png (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x000002A2AF9472E0>, 'Connection to pixiv.yuki.sh timed out. (connect timeout=None)'))
296.png is ok
298.png is ok
301.png is ok
303.png is ok
Error downloading image: 429 Client Error: Too Many Requests for url: https://api.lolicon.app/setu/v2?r18=1&num=20
306.png is ok
307.png is ok
309.png is ok
```

### 代码

```python
# file: 爬色图

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
```

```python
# file: 处理.py
import os
import hashlib
 
def filecount():
    filecount = int(os.popen('dir /B |find /V /C ""').read())
    return (filecount)
 
 
def md5sum(filename):
    f = open(filename, 'rb')
    md5 = hashlib.md5()
    while True:
        fb = f.read(8096)
        if not fb:
            break
        md5.update(fb)
    f.close()
    return (md5.hexdigest())
 
 
def delfile():
    all_md5 = {}
    filedir = os.walk(os.getcwd())
    for i in filedir:
        for tlie in i[2]:
            if md5sum(tlie) in all_md5.values():
                os.remove(tlie)
            else:
                all_md5[tlie] = md5sum(tlie)
 
 
if __name__ == '__main__':
    cnt = 0
    p = os.getcwd()
    files = os.listdir(p)
    for f in files:
        try:
            if open(p + '/' + f, 'rb').read(1) == b'{':
                os.remove(p + '/' + f)
                cnt += 1
        except:
            pass
    print('删除%d个返回失败的文件\n' % cnt)

    
    oldf = filecount()
    print('去重前有', oldf, '个文件\n\n\n请稍等正在删除重复文件...')
    delfile()
    print('\n\n去重后剩', filecount(), '个文件')
    print('\n\n一共删除了', oldf - filecount(), '个文件\n\n')
    os.system('pause')
```

### 使用说明
1. 在 `爬色图.py` 处新建 `setu` 文件夹
2. 运行 `爬色图.py`
3. 在 `setu` 文件夹里运行 `处理.py`

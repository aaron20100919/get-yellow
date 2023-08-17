# get-yellow
[用python爬取涩图](https://github.com/aaron20100919/get-yellow)

### 首先上效果
```
...

Error accessing URL: 'data'
868.png is ok
869.png is ok
870.png is ok
871.png is ok
872.png is ok
873.png is ok
874.png is ok
875.png is ok
876.png is ok
877.png is ok
878.png is ok
879.png is ok
880.png is ok
881.png is ok
882.png is ok
883.png is ok
884.png is ok
885.png is ok
886.png is ok
887.png is ok
888.png is ok
889.png is ok
890.png is ok
891.png is ok
892.png is ok
893.png is ok
Error downloading image: 404 Client Error: Not Found for url: https://i.pixiv.re/img-original/img/2023/06/29/13/55/17/109442914_p0.png
894.png is ok
895.png is ok
896.png is ok
Error downloading image: 404 Client Error: Not Found for url: https://i.pixiv.re/img-original/img/2022/08/23/20/13/55/100709529_p0.jpg
删除0个返回失败的文件

去重前有 897 个文件


请稍等正在删除重复文件...


去重后剩 894 个文件


一共删除了 3 个文件


836.png is ok
841.png is ok
879.png is ok
897.png is ok
898.png is ok
899.png is ok
900.png is ok
Error downloading image: 404 Client Error: Not Found for url: https://i.pixiv.re/img-original/img/2022/12/13/18/02/13/103575192_p0.jpg
Error downloading image: 404 Client Error: Not Found for url: https://i.pixiv.re/img-original/img/2022/06/21/20/03/30/99207335_p1.png
901.png is ok
902.png is ok
903.png is ok
Error downloading image: 404 Client Error: Not Found for url: https://i.pixiv.re/img-original/img/2022/11/30/02/36/34/103210968_p0.jpg
904.png is ok
905.png is ok
906.png is ok
907.png is ok
908.png is ok
909.png is ok
910.png is ok
911.png is ok
912.png is ok
913.png is ok
914.png is ok
```

### 代码

```python
# file: 爬色图(pasetu.py)

import re
import warnings
import json
import os
import hashlib

try:
    import requests
    from requests.packages import urllib3
except ModuleNotFoundError:
    os.system('pip install requests')
    import requests
    from requests.packages import urllib3

warnings.filterwarnings("ignore")

urllib3.disable_warnings()

# http://www.chinawriter.com.cn/2015/2015-03-17/236975.html # 如果你很坏, 读完这一行链接后, 将下一行删掉#和空格, 下下行删了
# urls = ['https://moe.jitsu.top/r18', 'https://api.lolicon.app/setu/v2?r18=1&num=10'] # , 'https://image.anosu.top/pixiv/direct?r18=1&num=30', 'https://sex.nyan.xyz/api/v2/img?num=10&r18=true']
urls = ['https://api.lolicon.app/setu/v2?num=10']
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
        if num % 20 == 0:
            fix()
        num = 0


def filecount():
    return len(os.listdir('./setu'))


def md5sum(filename):
    f = open('./setu/' + filename, 'rb')
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
    filedir = os.walk(os.getcwd() + '/setu')
    for i in filedir:
        for tlie in i[2]:
            if tlie[-3:] == 'png':
                if md5sum(tlie) in all_md5.values():
                    os.remove('./setu/' + tlie)
                else:
                    all_md5[tlie] = md5sum(tlie)


def fix():
    cnt = 0
    p = os.getcwd() + '/setu'
    files = os.listdir(p)
    for f in files:
        try:
            if open(p + '/' + f, 'rb').read(1) == b'{' or open(p + '/' + f, 'rb').read(1) == b'<':
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


if __name__ == "__main__":
    if not os.path.exists(os.getcwd() + '/setu'):
        os.mkdir(os.getcwd() + '/setu')
    try:
        while True:
            for url in urls:
                try:
                    response = requests.get(url)
                    content_type = response.headers.get('Content-Type')
                    if content_type.find('application/json') != -1:
                        data = response.json()
                        links = [item['urls']['original']
                                 for item in data['data']]
                        for link in links:
                            download_image(link, num)
                            num += 1
                    else:
                        download_image(url, num)
                        num += 1
                except Exception as e:
                    print(f'Error accessing URL: {str(e)}')
                    if num % 20 == 0:
                        fix()
                    num = 0
    except KeyboardInterrupt:
        fix()
        pass
```

### 使用说明
1. 直接运行 `爬色图.py`

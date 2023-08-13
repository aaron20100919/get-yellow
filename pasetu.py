import re
import warnings
import json
import os
import hashlib

try:
    import requests
    from requests.packages import urllib3
except ModuleNotFoundError:
    os.system('pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U')
    import requests
    from requests.packages import urllib3

warnings.filterwarnings("ignore")

urllib3.disable_warnings()

# http://www.chinawriter.com.cn/2015/2015-03-17/236975.html
# urls = ['https://moe.j???itsu.top/r18', 'https://api.lol???icon.app/setu/v2?r18=1&num=10'] # , 'https://image.anosu.top/pixi???v/direct?r18=1&num=30', 'https://sex.n???yan.xyz/api/v2/img?num=10&r18=true']
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

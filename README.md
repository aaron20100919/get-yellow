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

### 使用说明
1. 在 `爬色图.py` 处新建 `setu` 文件夹
2. 运行 `爬色图.py`
3. 在 `setu` 文件夹里运行 `去重.py`

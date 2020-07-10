#gl.py 全局变量定义模块

filmlist = []
casts = []
actorlist = []

head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "Cookie": 'bid=kQ3S0gUvVtc; __gads=ID=9247b7cae7ee6dc3:\
        T=1590506979:S=ALNI_Mab-EyjfbbvDHnXfGvtjb5hkM3r5A; ll="118316"; \
        __yadk_uid=Cz2RXPIH44JXT5xD580rYnlS3E2FiN9D; \
        _vwo_uuid_v2=D7F52A53160EEEE1537AD989E1162EBA8|d5ea1a5cd19412fdae66d1b4c56a58a3; \
        ct=y; __utmc=30149280; \
        __utmz=30149280.1591118319.2.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; \
        __utmc=223695111; __utmz=223695111.1591199738.5.3.utmcsr=douban.com|utmccn=(referral)|\
        utmcmd=referral|utmcct=/doulist/1605639/; \
        _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1591287294%2C%22https%3A%2F%2F\
        www.douban.com%2Fdoulist%2F1605639%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0;\
         __utma=30149280.1226899291.1590506980.1591230766.1591287295.7; __utmb=30149280.0.10.1591287295; \
         __utma=223695111.1410696961.1590506980.1591230766.1591287295.7; __utmb=223695111.0.10.1591287295;\
          _pk_id.100001.4cf6=12ce95e1d7ed8f21.1590506980.7.1591287710.1591231040.',

        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome \
        / 80.0.3987.122  Safari / 537.36",

        "Referer": "https://movie.douban.com/explore"
    }
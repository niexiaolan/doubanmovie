# coding=UTF-8
#-------全部信息搜索-------
import re
import time
import urllib.request,urllib.error
from bs4 import BeautifulSoup
from random import random
from urllib import parse
import requests
import json
import pymssql


def main():
    # 电影基本信息链接 tag和star字段可变
    url1 = 'https://movie.douban.com/subject/1299999'
    #提取数据至列表

    html = AskHTML(url1)

    # movie = re.findall(data,html)
    # print(movie)
    # print(type(movie))




# 爬取网页
def AskHTML(url):
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

        "Referer": "https://movie.douban.com/tag/"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #-----数据提取-----
        soup = BeautifulSoup(html, "html.parser")  # 把html文档通过html.parser解析器解析为文件树
        movie_list = soup.find_all(type="application/ld+json")
        for item in movie_list:
            movie_dict = json.loads(item.get_text())
            movie_tuple = (movie_dict["name"], movie_dict[""])

        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html
#--------获取和保存要不要放在一起？--------


    # print(soup.title) #打印标签树中出现的第一个title标签
    # print(soup.title.string) #打印标签中的内容
    # print(soup.title.attrs) #字典形式打印标签中的值
    # print(soup.head.contents) #文档遍历
#过滤重复数据
# def filterdata(filmlist):
#
# # 建立一个新的列表filmonlylist[]，每次像列表中添加数据是时先判断是否重复，重复就从内层循环跳出，不重复就加入新的列表
#
#     filmonlylist = []
#     filmonlylist.append(filmlist[1])
#     for index1 in range(len(filmlist)):
#         flag = 0
#         for index2 in range(len(filmonlylist)):
#             if filmlist[index1] == filmonlylist[index2]:
#                 flag = 1
#                 break
#         if flag == 0 :
#             filmonlylist.append(filmlist[index1])
#     return filmonlylist



if __name__ == '__main__':
    main()
    print("爬取完毕!")

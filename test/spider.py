# coding=UTF-8

from urllib import parse
import requests
import json
import pymssql


def main():
    # 电影基本信息链接 tag和star字段可变
    url1 = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=recommend&page_limit=20&page_start='
    # url1 = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0'
    #        'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=20'

    # print(AskHTML(url))
    #提取数据至列表
    filmlist = AskHTML(url1)
    # filmonlylist=filterdata(filmlist)
    # 保存到数据库
    saveData2DB(filmlist)


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

        "Referer": "https://movie.douban.com/explore"
    }
    typelist = ['热门', '最新', '经典', '冷门佳片', '华语', '欧美', '韩国','日本',
                '喜剧','爱情', '科幻', '悬疑', '恐怖', '文艺','治愈','动画']

    # 将typelist转为url编码
    codetypelist = []
    for a in typelist:
        a = parse.quote(a)
        codetypelist.append(a)

    filmlist = []  # 存放最终要导入数据库的数据
    # 更改url里的tag
    for a in range(len(codetypelist)):
        myurl = url.format(codetypelist[a])
        #更改url里的star
        for i in range(0,800, 20):
            marl = myurl + str(i)
            response = requests.get(marl, headers=head)
            jd = json.loads(response.text)
            jdlist = jd['subjects']
            '''
            jd是一个字典，只存了一个键值对，其中value：jd['subjects']是一个列表，
            其中的每一个元素又是一个字典,所以首先要遍历列表的每一个元素，将value组
            成新的元组，再将元组加入新的列表
            '''
            for index in range(len(jdlist)):
                jdtuple = (jdlist[index]['id'], jdlist[index]['url'],
                           jdlist[index]['cover'], jdlist[index]['title'],
                           jdlist[index]['rate'])
                filmlist.append(jdtuple)
    filmlist = list(set(filmlist))
    return filmlist

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

def saveData2DB(filmlist):
    serverName = '127.0.0.1'  #本地id
    userName = 'sa'           #用户名
    passWord = '19800506abcD' #密码
    # 建立连接并获取cursor
    conn = pymssql.connect(serverName, userName, passWord, database='douban', charset='utf8')
    cursor = conn.cursor()
    # 建表操作
    cursor.execute(
        '''
    IF OBJECT_ID('doubanlist', 'U') IS NOT NULL
        DROP TABLE doubanlist
        CREATE TABLE doubanlist
        (
        id INT PRIMARY KEY,
        info_link VARCHAR(255),
        pic_link VARCHAR(255),
        cname VARCHAR(255),
        score CHAR(4)
        )
        ''')
    conn.commit() #保存
    cursor.executemany("insert into doubanlist(id,info_link,pic_link,cname,score)"
                            "VALUES(%d,%s,%s,%s,%s)", filmlist)
    conn.commit()


if __name__ == '__main__':
    main()
    print("爬取完毕!")

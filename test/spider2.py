# coding=UTF-8
import random
import re
import time
import urllib
import requests
import json
import pymssql
from bs4 import BeautifulSoup


def main():

    #提取数据至列表
    AskHTML()
    # filmonlylist=filterdata(filmlist)
    # 保存到数据库



# 爬取网页
def AskHTML():
    movie_type = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑',
                  '惊悚', '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记',
                  '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠']
    movie_zone = ['中国大陆', '美国', '香港', '台湾', '日本',
                  '韩国', '英国', '法国', '德国', '意大利',
                  '西班牙', '印度', '泰国', '俄罗斯', '伊朗',
                  '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']
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
    directorlist = [] # 存放最终要导入数据库的导演数据
    filmlist = []  # 存放最终要导入数据库的电影数据
    casts = [] #存放最终要导入数据库的演员数据
    actor_list = []#存放最终要导入数据库的影人数据
    for type in movie_type:
        for zone in movie_zone:
            for i in range(0,10000 , 20):
                print("i is:", i)
                url = str(
                    "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={页面}&genres=" + type + "&countries=" + zone + "").format(
                    页面=i)
                print(url)
                response = requests.get(url, headers=head)
                time.sleep(random.random()*3)
                jd = json.loads(response.text)
                try:
                    jdlist = jd['data']
                    print(jdlist)
                    '''
                              jd是一个字典，只存了一个键值对，其中value：jd['subjects']是一个列表，
                              其中的每一个元素又是一个字典,所以首先要遍历列表的每一个元素，将value组
                              成新的元组，再将元组加入新的列表
                              '''
                    for index in range(len(jdlist)):
                        # 找到url 进入电影详情页
                        movieurl = jdlist[index]['url']
                        print(movieurl)
                        request = urllib.request.Request(movieurl, headers=head)
                        time.sleep(random.random() * 3)
                        html = ""
                        try:
                            response = urllib.request.urlopen(request)
                            html = response.read().decode("utf-8")
                            # -----数据提取-----
                            soup = BeautifulSoup(html, "html.parser")  # 把html文档通过html.parser解析器解析为文件树
                            movie_list = soup.find_all(type="application/ld+json")
                            for item in movie_list:  # 一条电影的全部信息
                                movie_dict = json.loads(item.get_text())
                                print(movie_dict)
                                movie_age = movie_dict["datePublished"]
                                movie_ratingCount = movie_dict["aggregateRating"]["ratingCount"]
                                movie_decription = movie_dict["description"]
                                # 电影数据整合
                                moivetuple = (jdlist[index]['id'], jdlist[index]['url'],
                                              jdlist[index]['cover'], jdlist[index]['title'],
                                              jdlist[index]['rate'], zone, movie_age, movie_ratingCount,
                                              movie_decription)
                                print(moivetuple)
                                filmlist.append(moivetuple)
                                casts_list = movie_dict['actor']
                                # director = movie_dict['director']
                                # print(director)

                                for castsindex in range(len(casts_list)):
                                    reid = re.match('/celebrity/(\d*)/', str(casts_list[castsindex]["url"]))
                                    actor_id = reid.group(1)
                                    actor_name = casts_list[castsindex]["name"]
                                    casts_tuple = (actor_id, actor_name, jdlist[index]['id'], '演员')
                                    print(casts_tuple)
                                    casts.append(casts_tuple)

                                director = movie_dict['director']
                                for directorindex in range(len(director)):  # 考虑到可能会有多个导演
                                    reDirectorId = re.match('/celebrity/(\d*)/', str(director[directorindex]['url']))
                                    director_id = reDirectorId.group(1)
                                    director_name = director[directorindex]['name']
                                    director_tuple = (director_id, director_name, jdlist[index]['id'], '导演')
                                    print(director_tuple)
                                    casts.append(director_tuple)

                                # director = movie_dict['director'][0]
                                # reDirectorId = re.match('/celebrity/(\d*)/',str(director['url']))
                                # director_id = reDirectorId.group(1)
                                # director_name = director['name']
                                # director_tuple = (director_id, director_name, jdlist[index]['id'], '导演')
                                # print(director_tuple)
                                # casts.append(director_tuple)

                        except urllib.error.URLError as e:
                            if hasattr(e, "code"):
                                print(e.code)
                            if hasattr(e, "reason"):
                                print(e.reason)

                except:
                    break
    filmlist = list(set(filmlist))
    print(filmlist)
    casts = list(set(casts))
    print(casts)
    # 从参演人员表中id得到url，爬取演员信息
    for indexcasts in range(len(casts)):
        actor_url = "https://movie.douban.com/celebrity/" + casts[indexcasts][0]
        print(actor_url)
        time.sleep(random.random() * 3)
        request = urllib.request.Request(actor_url, headers=head)
        response = urllib.request.urlopen(request)
        actorhtml = response.read().decode("utf-8")
        soup = BeautifulSoup(actorhtml, "html.parser")  # 把html文档通过html.parser解析器解析为文件树
        movie_list = soup.find_all(id="headline")
        findpiclink = re.compile(r'src="(.*?)"')
        findsex = re.compile(r'<span>性别</span>:(.*?)</li>', re.S)
        findstar = re.compile(r'<span>星座</span>:(.*?) </li>', re.S)
        finddate = re.compile(r'<span>出生日期</span>: (.*?)</li>', re.S)
        findcountry = re.compile(r'<span>出生地</span>: (.*?)</li>', re.S)
        for item in movie_list:
            item = str(item)
            piclinklist = re.findall(findpiclink,item)
            piclink = "".join(piclinklist)
            sex = re.findall(findsex, item)
            actorSex = "".join(sex).strip()
            star = re.findall(findstar, item)
            actorStar = "".join(star).strip()
            date = re.findall(finddate, item)
            actorDate = "".join(date).strip()
            country = re.findall(findcountry, item)
            actorCountry = "".join(country).strip()
            actor_tuple = (casts[indexcasts][0], casts[indexcasts][1], piclink,actorSex, actorStar, actorDate, actorCountry)
            print(actor_tuple)
            actor_list.append(actor_tuple)


    actor_list = list(set(actor_list))
    print(actor_list)

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

#保存到数据库
    serverName = '127.0.0.1'  #本地id
    userName = 'sa'           #用户名
    passWord = '19800506abcD' #密码
    # 建立连接并获取cursor
    conn = pymssql.connect(serverName, userName, passWord, database='douban', charset='utf8')
    cursor = conn.cursor()
    # 电影信息表
    cursor.execute(
        '''
    IF OBJECT_ID('filmtable', 'U') IS NOT NULL
        DROP TABLE filmtable
        CREATE TABLE filmtable
        (
        movieid INT PRIMARY KEY,
        infolink VARCHAR(255),
        piclink VARCHAR(255),
        filmname VARCHAR(255),
        score CHAR(4),
        country CHAR(10),
        filmdate CHAR(10),
        scorecount CHAR(10),
        descripetion VARCHAR(255)
        
        )
        ''')
    conn.commit() #保存
    cursor.executemany("insert into filmtable(movieid,infolink,piclink,filmname,score,country,filmdate,scorecount,descripetion)"
                            "VALUES(%d,%s,%s,%s,%s,%s,%s,%s,%s)", filmlist)
    conn.commit()

    #影人信息表

    cursor.execute(
        '''
    IF OBJECT_ID('actortable', 'U') IS NOT NULL
        DROP TABLE actortable
        CREATE TABLE actortable
        (
        actorid INT PRIMARY KEY,
        actorname VARCHAR(80),
        actorpic VARCHAR(255),
        actorsex CHAR(4),
        actorstar CHAR(10),
        actordate CHAR(10),
        actorcountry CHAR(40)

        )
        ''')
    conn.commit()  # 保存
    cursor.executemany(
        "insert into actortable(actorid,actorname,actorpic,actorsex,actorstar,actordate,actorcountry)"
        "VALUES(%d,%s,%s,%s,%s,%s,%s)", actor_list)
    conn.commit()

    #参演信息表
    cursor.execute(
        '''
    IF OBJECT_ID('caststable', 'U') IS NOT NULL
        DROP TABLE caststable
        CREATE TABLE caststable
        (
        actorid INT NOT NULL,
        actorname VARCHAR(80),
        movieid INT NOT NULL,
        caststype CHAR(10),
        CONSTRAINT PK_caststable PRIMARY KEY (actorid,movieid,caststype),
        CONSTRAINT FK_caststable_actortable FOREIGN KEY (actorid) 
        REFERENCES douban.actortable (actorid),
        CONSTRAINT FK_caststable_filmtable FOREIGN KEY (movieid) 
        REFERENCES douban.filmtable (movieid)
        
        )
        ''')
    conn.commit()  # 保存
    cursor.executemany(
        "insert into filmtable(actorid,actorname,movieid,caststype)"
        "VALUES(%d,%s,%d,%s)", casts)
    conn.commit()

    conn.close






if __name__ == '__main__':
    main()
    print("爬取完毕!")

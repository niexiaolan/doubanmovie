# coding=UTF-8
import random
import re
import time
import urllib
import requests
import json
from bs4 import BeautifulSoup
from spider import gl

# ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑',
#                   '惊悚', '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记',
#                   '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠']
# ['中国大陆', '美国', '香港', '台湾', '日本',
#                   '韩国', '英国', '法国', '德国', '意大利',
#                   '西班牙', '印度', '泰国', '俄罗斯', '伊朗',
#                   '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']

def AskHTML():

    movie_type = ['剧情'] #电影类型
    movie_zone = ['韩国'] #国家
    for typeindex in movie_type:
        for zone in movie_zone :
            for i in range(500,1000, 20):
                print("i is : ",i)
                url = str(
                    "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={页面}&genres=" + typeindex + "&countries=" + zone + "").format(
                    页面=i)
                print('URL')
                print(url)
                print("--------------")
                response = requests.get(url, headers=gl.head)
                time.sleep(random.random() * 3)
                jd = json.loads(response.text,strict=False)
                try:
                    jdlist = jd['data']
                    print("jdlist")
                    print(jdlist)
                    '''
                          jd是一个字典，只存了一个键值对，其中value：jd['subjects']是一个列表，
                          其中的每一个元素又是一个字典,所以首先要遍历列表的每一个元素，将value组
                          成新的元组，再将元组加入新的列表
                    '''
                    for index in range(len(jdlist)):
                        # 找到url 进入电影详情页
                        movieurl = jdlist[index]['url']
                        print("--------------")
                        print(movieurl)
                        print("--------------")
                        request = urllib.request.Request(movieurl, headers=gl.head)
                        time.sleep(random.random() * 5)
                        html = ""
                        response = urllib.request.urlopen(request)
                        html = response.read().decode("utf-8")
                        # -----数据提取-----
                        soup = BeautifulSoup(html, "html.parser")  # 把html文档通过html.parser解析器解析为文件树
                        movie_list = soup.find_all(type="application/ld+json")
                        for item in movie_list:  # 一条电影的全部信息
                            movie_dict = json.loads(item.get_text(), strict=False)
                            movie_age = movie_dict["datePublished"]
                            movie_ratingCount = movie_dict["aggregateRating"]["ratingCount"]
                            movie_decription = movie_dict["description"]
                            # 电影数据整合
                            moivetuple = (jdlist[index]['id'], jdlist[index]['url'],
                                          jdlist[index]['cover'], jdlist[index]['title'],
                                          jdlist[index]['rate'], zone, movie_age, movie_ratingCount,
                                          movie_decription)
                            print(moivetuple)
                            print("--------------")
                            gl.filmlist.append(moivetuple)
                            data = open("C:/spider/data.txt",'w+',encoding='utf-8')
                            print(gl.filmlist,file=data)
                            data.close()

                except KeyError:
                    print("keyerror ")





    filmlist = list(set(gl.filmlist))
    print('电影数据爬取结束！')
    print("--------------")
    return filmlist

def Askcasts(filmlist):

    for film in filmlist:
        movieurl = film[1]
        print("movieurl:" + movieurl)
        print("--------------")
        request = urllib.request.Request(movieurl, headers=gl.head)
        time.sleep(random.random() * 3)
        try:
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
            # -----数据提取-----
            soup = BeautifulSoup(html, "html.parser")  # 把html文档通过html.parser解析器解析为文件树
            movie_list = soup.find_all(type="application/ld+json")
            for item in movie_list:  # 一条电影的全部信息
                print("失败1")
                movie_dict = json.loads(item.get_text(),strict=False)
                print("失败2")
                print(movie_dict)
                casts_list = movie_dict['actor']
                print("失败3")

                for castsindex in range(len(casts_list)):
                    reid = re.match('/celebrity/(\d*)/', str(casts_list[castsindex]["url"]))
                    actor_id = reid.group(1)
                    actor_name = casts_list[castsindex]["name"]
                    casts_tuple = (actor_id, actor_name, film[0], '演员')
                    gl.casts.append(casts_tuple)
                    print(gl.casts)

                director = movie_dict['director']
                for directorindex in range(len(director)):  # 考虑到可能会有多个导演
                    reDirectorId = re.match('/celebrity/(\d*)/', str(director[directorindex]['url']))
                    director_id = reDirectorId.group(1)
                    director_name = director[directorindex]['name']
                    director_tuple = (director_id, director_name, film[0], '导演')
                    print(director_tuple)
                    gl.casts.append(director_tuple)


        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
    casts = list(set(gl.casts))
    data1 = open("C:/spider/data1.txt", 'w+', encoding='utf-8')
    print(casts, file=data1)
    data1.close()
    print('参演数据爬取完毕！')
    return casts

def Askactor(casts):

    for indexcasts in range(len(casts)):
        actor_url = "https://movie.douban.com/celebrity/" + casts[indexcasts][0]
        print(actor_url)
        time.sleep(random.random() * 3)
        request = urllib.request.Request(actor_url, headers=gl.head)
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
            piclinklist = re.findall(findpiclink, item)
            piclink = "".join(piclinklist)
            sex = re.findall(findsex, item)
            actorSex = "".join(sex).strip()
            star = re.findall(findstar, item)
            actorStar = "".join(star).strip()
            date = re.findall(finddate, item)
            actorDate = "".join(date).strip()
            country = re.findall(findcountry, item)
            actorCountry = "".join(country).strip()
            actor_tuple = (
            casts[indexcasts][0], casts[indexcasts][1], piclink, actorSex, actorStar, actorDate, actorCountry)
            print(actor_tuple)
            gl.actorlist.append(actor_tuple)
            data2 = open("C:/spider/data2.txt", 'w+', encoding='utf-8')
            print(gl.actorlist, file=data2)
            data2.close()

    actorlist = list(set(gl.actorlist))
    print(actorlist)
    return actorlist




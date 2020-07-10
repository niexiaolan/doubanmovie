# coding=UTF-8
import pymssql

#连接数据库并获取游标
def connectDB():
    serverName = '127.0.0.1'  # 本地id
    userName = 'sa'  # 用户名
    passWord = '19800506abcD'  # 密码
    # 建立连接并获取cursor
    conn = pymssql.connect(serverName, userName, passWord, database='douban', charset='utf8')

    return conn

#搜索电影结果并返回一个字典
def searchfilm(filmname):
    conn = connectDB()
    cursor =conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM filmtable WHERE filmname ='%s'" % filmname)
    filmList = cursor.fetchall()
    cursor.close
    conn.close
    #搜索到则返回搜索结果，无结果则返回 1
    if filmList:
        return filmList
    return 1



def searchfilm(filmname):
    conn = connectDB()
    cursor =conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM filmtable WHERE filmname ='%s'" % filmname)
    #结果不存在怎么办？
    filmList = cursor.fetchall()
    cursor.close
    conn.close
    return filmList


def searchfilmname(movieid):
    conn = connectDB()
    cursor =conn.cursor(as_dict=True)
    cursor.execute("SELECT infolink,piclink,filmname,score,scorecount,country,filmdate FROM filmtable WHERE movieid = %d" % movieid)
    #结果不存在怎么办？
    filmonlyList = cursor.fetchall()
    cursor.close
    conn.close
    return filmonlyList

def searchactor(actorname):
    conn = connectDB()
    cursor =conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM actortable WHERE actorname LIKE '%s'" % actorname)
    #结果不存在怎么办？
    actorList = cursor.fetchall()
    cursor.close
    conn.close
    return actorList

#top250
def searchtop():

    conn = connectDB()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM douban250")
    actorList = cursor.fetchall()
    #结果不存在怎么办？
    cursor.close
    conn.close
    return actorList

#参演表查询
def searchcasts(actorid):

    conn = connectDB()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM caststable WHERE actorid = '%s'" % actorid )
    caststList = cursor.fetchall()
    #结果不存在怎么办？
    cursor.close
    conn.close
    return caststList

#搜索获奖名单
# def searchaward():
#     conn = connectDB()
#     cursor =conn.cursor()
#     cursor.execute("SELECT * FROM Oscar")
#     awardlist = cursor.fetchall()
#     cursor.close
#     conn.close
#     return awardlist




# def main():
#     # dict = {'filmname':'出租车','film':'bala'}
#     # filmname = dict['filmname']
#     #
#     # searchfilm(filmname)
#     movielist = searchtop()
#     print(movielist)
#
# if __name__ == '__main__':
#     main()
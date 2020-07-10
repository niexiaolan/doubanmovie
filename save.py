# coding=UTF-8
import pymssql

# filmlist = casts = actorlist =
casts = []
def main():
    print("开始保存数据...")
    # savefilm2DB(filmlist)
    # saveActor2DB(actorlist)
    saveCasts2DB(casts)
    print("数据保存完毕！")

def savefilm2DB(filmlist):
    serverName = '127.0.0.1'  # 本地id
    userName = 'sa'  # 用户名
    passWord = '19800506abcD'  # 密码
    # 建立连接并获取cursor
    conn = pymssql.connect(serverName, userName, passWord, database='douban', charset='utf8')
    cursor = conn.cursor()
    # 建表操作
    # cursor.execute(
    #     '''
    #
    #     CREATE TABLE filmtable
    #     (
    #     movieid INT ,
    #     infolink VARCHAR(255),
    #     piclink VARCHAR(255),
    #     filmname VARCHAR(255),
    #     score CHAR(4),
    #     country CHAR(10),
    #     filmdate CHAR(10),
    #     scorecount CHAR(10),
    #     descripetion VARCHAR(255)
    #
    #     )
    #     ''')
    # conn.commit()  # 保存

    cursor.executemany(
        "insert into filmtable(movieid,infolink,piclink,filmname,score,country,filmdate,scorecount,descripetion)"
        "VALUES(%d,%s,%s,%s,%s,%s,%s,%s,%s)", filmlist)
    conn.commit()
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接

def saveActor2DB(actorlist):
    serverName = '127.0.0.1'  # 本地id
    userName = 'sa'  # 用户名
    passWord = '19800506abcD'  # 密码
    # 建立连接并获取cursor
    conn = pymssql.connect(serverName, userName, passWord, database='douban', charset='utf8')
    cursor = conn.cursor()
    # cursor.execute(
    #     '''
    # IF OBJECT_ID('actortable', 'U') IS NOT NULL
    #     DROP TABLE actortable
    #     CREATE TABLE actortable
    #     (
    #     actorid INT PRIMARY KEY,
    #     actorname VARCHAR(255),
    #     actorpic VARCHAR(255),
    #     actorsex CHAR(4),
    #     actorstar CHAR(10),
    #     actordate CHAR(10),
    #     actorcountry VARCHAR(40)
    #
    #     )
    #     ''')
    # conn.commit()  # 保存
    cursor.executemany(
        "insert into actortable(actorid,actorname,actorpic,actorsex,actorstar,actordate,actorcountry)"
        "VALUES(%d,%s,%s,%s,%s,%s,%s)", actorlist)
    conn.commit()
    conn.close


def saveCasts2DB(casts):
    serverName = '127.0.0.1'  # 本地id
    userName = 'sa'  # 用户名
    passWord = '19800506abcD'  # 密码
    # 建立连接并获取cursor
    conn = pymssql.connect(serverName, userName, passWord, database='douban', charset='utf8')
    cursor = conn.cursor()
    # cursor.execute(
    # #     '''
    # # IF OBJECT_ID('caststable', 'U') IS NOT NULL
    # #     DROP TABLE caststable
    # #     CREATE TABLE caststable
    # #     (
    # #     actorid INT NOT NULL,
    # #     actorname VARCHAR(255),
    # #     movieid INT NOT NULL,
    # #     caststype CHAR(10),
    # #     CONSTRAINT PK_caststable PRIMARY KEY (actorid,movieid,caststype),
    # #     CONSTRAINT FK_caststable_actortable FOREIGN KEY (actorid)
    # #     REFERENCES actortable (actorid),
    # #     CONSTRAINT FK_caststable_filmtable FOREIGN KEY (movieid)
    # #     REFERENCES filmtable (movieid)
    # #
    # #
    # #     )
    # #     ''')
    # conn.commit()  # 保存
    cursor.executemany(
        "insert into caststable(actorid,actorname,movieid,caststype)"
        "VALUES(%d,%s,%d,%s)", casts)
    conn.commit()

    conn.close

if __name__ == '__main__':
    main()
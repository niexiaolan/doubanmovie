import json
import re

from flask import Flask,render_template,request
import pymssql

import movieDB

app = Flask(__name__)


# 主页
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/index')
def home():
    return render_template('index.html')

# 搜索电影
@app.route('/searchfilm')
def searchfilm():
    return render_template('searchfilm.html')

#电影结果
@app.route('/resultfilm',methods = ['POST','GET'])
def resultfilm():
    if request.method == 'POST':
        result = request.form.get("moviename")
        #数据库查询
        moviedict = movieDB.searchfilm(result)
        return render_template('resultfilm.html',result = moviedict)

#搜索影人
@app.route('/searchactor')
def searchactor():

    return render_template('searchactor.html')

#影人介绍
@app.route('/resultactor',methods = ['POST','GET'])
def resultactor():
    if request.method == 'POST':
        result = request.form.get("actorname") + '%'
        actor = movieDB.searchactor(result)
        actorid = actor[0][0]
        casts = movieDB.searchcasts(actorid)
        movielist = []
        # movieidlist = []
        for item in casts:
            movieid = item[2]
            # movieidlist.append(movieid)
            movie = movieDB.searchfilmname(movieid = movieid)#存在大量重复数据
            movielist.append(movie[0])
        for i in range(len(movielist)):
            for j in range(0,len(movielist)-i-1):
                if movielist[j]['filmdate']<movielist[j+1]['filmdate']:
                    temp = movielist[j]
                    movielist[j] = movielist[j+1]
                    movielist[j+1] = temp

        # movieidtuple = tuple(movieidlist)
        # movielist = movieDB.searchfilmname(movieidtuple)

        return render_template('resultactor.html',actor = actor,movielist = movielist)



# Oscar获奖影片
@app.route('/Oscar')
def oscar():
    # awardfilm = movieDB.searchaward()
    # movielist = []
    # for item in awardfilm:
    #     movieid = item[0]
    #     movie = movieDB.searchfilmname(movieid=movieid)  # 存在大量重复数据
    #     movielist.append(movie)
    return render_template('Oscar.html')

#榜单
@app.route('/top')
def top():
    datalist = movieDB.searchtop()
    return render_template('top.html',movies = datalist)

if __name__ == '__main__':
    app.run(debug=True)
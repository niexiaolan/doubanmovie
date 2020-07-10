# coding=UTF-8

from spider import spiderfilm,save2DB

def main():

    print("开始爬取数据...")
    filmlist = spiderfilm.AskHTML()
    save2DB.savefilm2DB(filmlist)
    casts = spiderfilm.Askcasts(filmlist)
    save2DB.saveCasts2DB(casts)
    actor = spiderfilm.Askactor(casts)
    save2DB.saveActor2DB(actor)
    print("数据爬取完毕！")






if __name__ == '__main__':
    main()

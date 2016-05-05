# coding=utf-8
'''
Created on 2016年4月27日
 @author: moverzp
 description: mongoDB相关的操作，替代原先的url管理器和html输出器
'''
import pymongo
from pyExcelerator import *

class MongoDB(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017) #连接服务器
        db = client.GoodBooks #选择数据库
        self.newUrlsCol = db.newUrls #选择集合newUrls
        self.oldUrlsCol = db.oldUrls #选择集合oldUrls
        self.bookCol = db.book #选择集合book
        self.notFoundUrls = db.notFoundUrls #选择集合notFoundUrls
        
    #url管理器功能
    #保存一个新的url
    def add_new_url(self, url):
        if url is None:
            return
        #只有既不在未爬取集合，也不在已爬取集合，才加入该url
        if self.newUrlsCol.find({'url':url}).count() == self.oldUrlsCol.find({'url':url}).count() == 0:
            self.newUrlsCol.insert({'url': url})
    #在一堆url中取新的url进行保存    
    def add_new_urls(self, urls, data):
        if urls is None or len(urls) == 0:
            return
        if data is None: #舍弃书籍的推荐url也舍弃
            return
        for url in urls:
            self.add_new_url(url)
    #强制加入一个新的url
    def add_new_url_forcibly(self, url):
        self.oldUrlsCol.remove({'url': url})
        self.newUrlsCol.insert({'url': url})    
            
    def has_new_url(self):
        return self.newUrlsCol.find().count() != 0
    
    def get_new_url(self):
        urlDoc = self.newUrlsCol.find_one()
        self.newUrlsCol.remove(urlDoc)
        self.oldUrlsCol.insert(urlDoc)
        return urlDoc['url']
    
    def add_404_url(self, url):
        self.notFoundUrls.insert({'url':url})
         
    #html输出器功能
    def collect_data(self, data, urls):
        if data is None: #存在书籍由于评分过低或者信息不全被舍弃但是还有推荐书籍的情况
            return
        data['recommendUrls'] = urls
        self.bookCol.insert(data)
        
    def output_xls(self):
        allDatas = self.bookCol.find()
        w = Workbook() #创建一个工作簿
        ws = w.add_sheet('sheet1') #创建一个工作表
        ws.write(0,0,u'书名')
        ws.write(0,1,u'评分')
        ws.write(0,2,u'价格')
        ws.write(0,3,u'出版社')
        ws.write(0,4,u'url')
        row = 1
        for data in allDatas:
            ws.write( row, 0, data['bookName'] )
            ws.write( row, 1, data['score'] )
            ws.write( row, 2, data['price'] )
            ws.write( row, 3, data['publisher'] )
            ws.write( row, 4, data['url'] )
            row += 1
        w.save('GoodBooks.xls') #保存
            

            
    
    
    
    
    
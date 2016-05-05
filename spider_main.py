# -*- coding: utf-8 -*-


import url_manager, html_downloader, html_parser, html_outputer, mongoDB
import time

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager() #url管理器
        self.downloader = html_downloader.HtmlDownloader() #html网页下载器
        self.parser = html_parser.HtmlParser() #html分析器
        self.outputer = html_outputer.HtmlOutputer() #html输出器
        self.mongodb = mongoDB.MongoDB() #数据库操作器
        
    def craw(self, root_url, threshold):
        count = 1
        self.mongodb.add_new_url(root_url)
        #try:
        while self.mongodb.has_new_url():
            new_url = self.mongodb.get_new_url() #从url管理器中获取一个未爬取的url
            print 'craw %d : %s' % (count, new_url)
            html_cont = self.downloader.download(new_url) #下载该url的html
            if html_cont == 404: #某些页面一直是404，一般涉及政治问题
                self.mongodb.add_404_url(new_url)
            else:
                new_urls, new_data = self.parser.parse(new_url, html_cont, threshold) #分析html，返回urls和data
                self.mongodb.add_new_urls(new_urls, new_data) #将获取的urls添加进未爬取的url集合中，排除已爬取过的url
                self.mongodb.collect_data(new_data, new_urls) #连同其推荐书籍一起保存
            
            #time.sleep(0.2)
            if count == 10000:
                break
            count += 1
            
        #except:
            #print 'craw failed'
            #错误的url重新加入未爬取url集合
            #self.mongodb.add_new_url_forcibly(new_url)
        #finally:
            #self.mongodb.output_xls()

if __name__ == "__main__":
    root_url = "https://book.douban.com/subject/1477390/" #起始地址为《代码大全》
    obj_spider = SpiderMain()
    obj_spider.craw(root_url, 7.9) #默认最低评分书籍
    #obj_spider.mongodb.output_xls()
    print 'All down!'


















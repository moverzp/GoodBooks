# -*- coding: utf-8 -*-


import url_manager, html_downloader, html_parser, mongoDB
import time
import random

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager() #url管理器
        self.downloader = html_downloader.HtmlDownloader() #html网页下载器
        self.parser = html_parser.HtmlParser() #html分析器
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
            
            time.sleep(random.uniform(0.1, 0.3))
            if count == 100000:
                break
            count += 1
            
        #except:
            #print 'craw failed'
            #错误的url重新加入未爬取url集合
            #self.mongodb.add_new_url_forcibly(new_url)
        #finally:
            #self.mongodb.output_xls()

if __name__ == "__main__":
    rootUrl = "https://book.douban.com/subject/1477390/" #起始地址为《代码大全》
    obj_spider = SpiderMain()
    #爬取之前先保存两个cookie文件，防止403forbidden
    #obj_spider.downloader.save_cookie("cookie1.txt", rootUrl) #未登录运行
    #obj_spider.downloader.save_cookie("cookie2.txt", rootUrl) #登录运行
    
    #obj_spider.craw(rootUrl, 7.9) #开始爬取，默认最低评分为7.9
    #obj_spider.mongodb.output_xls() #以xls格式输出爬取结果
    print 'All down!'


















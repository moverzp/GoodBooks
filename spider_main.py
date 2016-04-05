# -*- coding: utf-8 -*-
import url_manager, html_downloader, html_parser, html_outputer
import time

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager() #url管理器
        self.downloader = html_downloader.HtmlDownloader() #html网页下载器
        self.parser = html_parser.HtmlParser() #html分析器
        self.outputer = html_outputer.HtmlOutputer() #html输出器
    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        try:
            while self.urls.has_new_url():
                new_url = self.urls.get_new_url() #从url管理器中获取一个未爬取的url
                print 'craw %d : %s' % (count, new_url)
                html_cont = self.downloader.download(new_url) #下载该url的html
                new_urls, new_data = self.parser.parse(new_url, html_cont) #分析html，返回urls和data
                self.urls.add_new_urls(new_urls) #将获取的urls添加进未爬取的url集合中，排除已爬取过的url
                self.outputer.collect_data(new_data) #数据都在内存中
                time.sleep(0.1)
                if count == 50:
                    break
                count += 1
            
        except:
            print 'craw failed'

        self.outputer.output_html()

if __name__ == "__main__":
    root_url = "https://book.douban.com/subject/1477390/" #起始地址为《代码大全》
    #root_url = "https://book.douban.com/subject/2243615/"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)


















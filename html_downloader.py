# coding=utf-8
'''
Created on 2016/4/3
 @author: moverzp
 description: 
'''
import urllib2
import time
from time import sleep

class HtmlDownloader(object):
    def __init__(self):
        # 伪装成浏览器，防止403错误
        self.headers = [
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'
        ]
        
    def _download(self, url, index):
        curHeader = self.headers[index] #获取一个浏览器头描述
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', curHeader)
            response = urllib2.urlopen(request)    
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
            if e.code == 403:
                return 403
            if e.code == 404:
                return 404
        if response.getcode() == 200: #200表示读取成功
                return response.read()
        
    def download(self, url):
        times = 1
        if url is None:
            return None
        index = 1
        while True:
            html_cont = self._download(url, index)
            if html_cont == 404: #404错误，将url放入404Urls
                return 404
            elif html_cont == 403: #如果出现403等错误，等待后继续爬取
                index = ( index + 1 ) % len(self.headers)
                import random
                sleeptime = random.randint(20, 30)
                print 'sleeping %d times...' % times
                times += 1
                sleep(sleeptime)
            else:
                return html_cont
                
                
            


            
            
    

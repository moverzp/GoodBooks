# coding=utf-8
'''
Created on 2016/4/3
 @author: moverzp
 description: 
'''
import urllib2
from time import sleep
import cookielib

class HtmlDownloader(object):
    useCookie = False #是否使用cookie
    changeCookie = False #是否需要更改cookie状态
    
    def __init__(self):
        pass

        
    def _download(self, url):
        Header = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #浏览器头描述
        
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', Header)
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
            html_cont = self._download(url)
            if html_cont == 404: #404错误，将url放入404Urls
                return 404
            elif html_cont == 403: #如果出现403等错误，等待后继续爬取
                index += 1
                import random
                sleeptime = random.randint(20, 30) * times #递增等待时间
                print 'sleeping %d times...' % times
                times += 1
                sleep(sleeptime)
            else:
                return html_cont
                
                
            


            
            
    

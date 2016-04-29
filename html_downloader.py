# coding=utf-8
'''
Created on 2016/4/3
 @author: moverzp
 description: 
'''
import urllib2
import random
import time

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
        
    def download(self, url):
        if url is None:
            return None
        while True: #如果出现403错误，等待后继续爬取
            #curHeader = self.headers[random.randint(0, len(self.headers)-1)] #随机获取一个浏览器头描述
            curHeader = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'
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
                    time.sleep(10)
                    return self.download(url)
            if response.getcode() == 200: #200表示读取成功
                return response.read()


            
            
    

# coding=utf-8
'''
Created on 2016/4/3
 
@author: Administrator
'''
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    #添加新的单个url，只添加不在新旧集合中的url
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    
    #添加新的一堆url，调用add_new_url添加
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
        
    def has_new_url(self):
        return len(self.new_urls) != 0
        
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
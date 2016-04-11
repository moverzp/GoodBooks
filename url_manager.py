# coding=utf-8
'''
Created on 2016/4/3
 
@author: Administrator
'''

class UrlManager(object):
    def __init__(self):
        self.new_urls = [] #用列表模拟队列，保证更可能喜欢的书的url在前面
        self.old_urls = set() #已经访问过的url使用set存储就可以了
    
    #添加新的单个url，只添加不在新旧集合中的url
    def add_new_url(self, url):
        if url is None:
            return
        tempSet = set(self.new_urls) #使用set查找效率高
        if url not in tempSet and url not in self.old_urls:
            self.new_urls.append(url)
    
    #添加新的一堆url，调用add_new_url添加
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
        
    def has_new_url(self):
        return len(self.new_urls) != 0
        
    def get_new_url(self):
        new_url = self.new_urls[0] #获取队头的元素
        del self.new_urls[0] #删除队头元素
        self.old_urls.add(new_url)
        return new_url
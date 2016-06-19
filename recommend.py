# coding=utf-8
'''
Created on 2016年6月20日
 @author: moverzp
 description: 推荐算法实现
'''
import mongoDB, math, pickle
from collections import defaultdict #可以直接使用下标访问二维字典不存在的元素
import sys


class Recommend(object):
    def __init__(self):
        self.mongodb = mongoDB.MongoDB() #数据库操作器
        self.itemUsers = dict() #物品到用户的倒排表
        self.C = defaultdict(defaultdict)
        self.N = defaultdict(defaultdict)
        self.W = defaultdict(defaultdict)
    
    def build_inver_table(self):
        doc = self.mongodb.bookCol.find()
        count = 0
        for book in doc:
            print count
            count += 1
            for i in book['recommendUrls']:
                item = self.mongodb.search_book_by_url(i)
                #如果物品为“无效书籍”，舍弃
                if item is None:
                    continue
                if i not in self.itemUsers:
                    self.itemUsers[i] = set()
                self.itemUsers[i].add(book['url'])
                
                
    def cal_corated_items(self):
        for i, users in self.itemUsers.items():
            for u in users:
                if u not in self.N.keys(): #如果一维字典中没有该键，初始化值为0
                    self.N[u] = 0
                self.N[u] += 1
                for v in users:
                    if u == v:
                        continue
                    if v not in self.C[u].keys(): #如果二维字典中没有该键，初始化值为0
                        self.C[u][v] = 0
                    self.C[u][v] += 1
                    
    def cal_matrix_W(self):
        for u, related_users in self.C.items():
            for v, cuv in related_users.items():
                self.W[u][v] = cuv / math.sqrt(self.N[u] * self.N[v])
    
    def save_matrix_w(self):
        f = open('matrixW.txt')
        pickle.dump(self.W, f)
        f.close()
    
    def load_matrix_w(self):
        f = open('matrixW.txt')
        self.W = pickle.load(f)
        f.close()
         
if __name__ == "__main__":
    recommend = Recommend()
    recommend.build_inver_table()
    recommend.cal_corated_items()
    recommend.cal_matrix_W()
    recommend.save_matrix_w()




            
# coding=utf-8
'''
Created on 2016年6月20日
 @author: moverzp
 description: 推荐算法实现
'''
import mongoDB, math, pickle, time
from collections import defaultdict #可以直接使用下标访问二维字典不存在的元素
import sys, operator
from operator import itemgetter
from numpy import rank
from time import sleep


class Recommend(object):
    def __init__(self):
        self.mongodb = mongoDB.MongoDB() #数据库操作器
        self.userItems = dict() #用户到物品的倒排表
        self.C = defaultdict(defaultdict) #用户与用户共同喜欢物品的个数
        self.N = defaultdict(defaultdict) #用户个数
        self.W = defaultdict(defaultdict) #相似度矩阵
        self.k = 20 #选取前k个最相似的物品计算预测相似度
        #初始化的时候需要载入物品相似度矩阵
        self.load_matrix_w()
    
    def _build_inver_table(self):
        doc = self.mongodb.bookCol.find()
        count = 0
        for book in doc:
            print count
            count += 1
            url = book['url']
            if url not in self.userItems:
                self.userItems[url] = set()
            if book['recommendUrls'] is None: #有些书籍没有推荐的url
                continue
            for i in book['recommendUrls']:
                item = self.mongodb.search_book_by_url(i)
                #如果物品为“无效书籍”，舍弃
                if item is None:
                    continue
                self.userItems[url].add(i)
                
                
    def _cal_corated_users(self):
        for u, items in self.userItems.items():
            for i in items:
                if i not in self.N.keys(): #如果一维字典中没有该键，初始化值为0
                    self.N[i] = 0
                self.N[i] += 1
                for j in items:
                    if i == j:
                        continue
                    if j not in self.C[i].keys(): #如果二维字典中没有该键，初始化值为0
                        self.C[i][j] = 0
                    self.C[i][j] += 1
                    
    def _cal_matrix_W(self):
        for i, related_items in self.C.items():
            for j, cij in related_items.items():
                self.W[i][j] = cij / math.sqrt(self.N[i] * self.N[j]) #余弦相似度
    
    def _save_matrix_w(self):
        f = open('matrixW.txt', 'w')
        pickle.dump(self.W, f)
        f.close()
    
    def load_matrix_w(self): #载入大概需要7.96s
        f = open('matrixW.txt')
        self.W = pickle.load(f)
        f.close()
    
    def cal_matrix_W(self):
        self.W.clear()
        print len(self.W)
        sleep(3)
        print 'build inver table...'
        self._build_inver_table()
        print 'cal corated users...'
        self._cal_corated_users()
        print 'cal matrix W...'
        self._cal_matrix_W()
        print 'save matrix...'
        self._save_matrix_w()
        
    
        
    #基于物品的协同过滤算法，输入为书本的urls，返回推荐的urls
    def itemCF(self, urls):
        rank = dict() #保存推荐的url及其对应的兴趣度
        for i in urls:
            book = self.mongodb.search_book_by_url(i)
            interest = float(book['score'])
            #j表示某物品，wj表示物品i和物品j的相似度
            for j, wj in sorted(self.W[i].items(), key=itemgetter(1), reverse=True)[0:self.k]:
                #如果已经包含了物品j，跳过
                if j in urls:
                    continue
                #如果物品j是无效书籍，跳过
                if self.mongodb.search_book_by_url(j) is None:
                    continue
                #根据评分和相似度计算物品j的预测兴趣度
                if j not in rank.keys():
                    rank[j] = 0
                rank[j] += interest * wj
        #按照兴趣度排序，返回推荐书籍的urls
        sorted_rank = sorted(rank.iteritems(), key=operator.itemgetter(1), reverse=True)[0:10]          
        print 'sorted:\n', sorted_rank
        res = []
        for i in sorted_rank:
            res.append(i[0])
        return res #只返回预测兴趣度前10的urls

if __name__ == '__main__':
    recommend = Recommend()
    recommend.cal_matrix_W()
    print 'all down!'



            
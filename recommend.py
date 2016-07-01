# coding=utf-8
'''
Created on 2016年6月20日
 @author: moverzp
 description: 推荐算法实现
'''
import mongoDB, math, pickle, time
from collections import defaultdict #可以直接使用下标访问二维字典不存在的元素
import sys, operator


class Recommend(object):
    def __init__(self):
        self.mongodb = mongoDB.MongoDB() #数据库操作器
        self.itemUsers = dict() #物品到用户的倒排表
        self.C = defaultdict(defaultdict) #用户与用户共同喜欢物品的个数
        self.N = defaultdict(defaultdict) #用户个数
        self.W = defaultdict(defaultdict) #相似度矩阵
        #初始化的时候需要载入物品相似度矩阵
        #self.load_matrix_w()
    
    def _build_inver_table(self):
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
                
                
    def _cal_corated_items(self):
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
                    
    def _cal_matrix_W(self):
        for u, related_users in self.C.items():
            for v, cuv in related_users.items():
                self.W[u][v] = cuv / math.sqrt(self.N[u] * self.N[v]) #余弦相似度
    
    def _save_matrix_w(self):
        f = open('matrixW.txt', 'w')
        pickle.dump(self.W, f)
        f.close()
    
    def load_matrix_w(self): #载入大概需要7.96s
        f = open('matrixW.txt')
        self.W = pickle.load(f)
        f.close()
    
    def cal_matrix_W(self):
        print 'build inver table...'
        self._build_inver_table()
        print 'cal corated items...'
        self._cal_corated_items()
        print 'cal matrix W...'
        self._cal_matrix_W()
        print 'save matrix...'
        self._save_matrix_w()
        
    
        
    #基于物品的协同过滤算法，输入为书本的urls，返回推荐的urls
    def itemCF(self, urls):
        recommendUrls = {} #保存推荐的url及其对应的兴趣度，最多10个
        for url in urls:
            book = self.mongodb.search_book_by_url(url)
            for i, j in self.W[url].items(): #i表示关联物品，j表示相似度
                #如果已经包含了关联物品，跳过
                if i in urls:
                    continue
                #如果关联物品是无效书籍，跳过
                if self.mongodb.search_book_by_url(i) is None:
                    continue
                #根据评分和相似度计算兴趣度，利用优先队列的思想更新推荐url
                interest = float(book['score']) * j
                if len(recommendUrls) < 10: #直接加入
                    recommendUrls[i] = interest
                else: #如果推荐书目>10，替换兴趣度最低的书籍
                    if interest > min(recommendUrls.values()):
                        index = min(recommendUrls, key=recommendUrls.get)
                        del(recommendUrls[index])
                        recommendUrls[i] = interest
        #按照兴趣度排序，返回推荐书籍的urls
        sorted_recommendUrls = sorted(recommendUrls.iteritems(), key=operator.itemgetter(1), reverse=True)                
        print 'sorted:\n', sorted_recommendUrls
        res = []
        for i in sorted_recommendUrls:
            res.append(i[0])
        return res
         
if __name__ == "__main__":
    recommend = Recommend()
    t1 = time.clock()
    recommend.load_matrix_w()
    t2 = time.clock()
    print t2 - t1





            
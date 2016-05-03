# coding=utf-8
'''
Created on 2016/4/3
 @author: moverzp
 description: 
'''
from bs4 import BeautifulSoup
import re, html_downloader

class HtmlParser(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader() #html网页下载器
        
    def _get_new_urls(self, soup):
        new_urls = []
        #同样喜欢区域：<div id="db-rec-section" class="block5 subject_show knnlike">
        recommend = soup.find('div', class_='block5 subject_show knnlike')
        #<a href="https://book.douban.com/subject/11614538/" class="">程序员的职业素养</a>
        links = recommend.find_all('a', href=re.compile(r"https://book\.douban\.com/subject/\d+/$"))
        for link in links:
            new_url = link['href']
            new_urls.append(new_url)
        return new_urls
    
    def _get_hot_review(self, soup):
        try: #没有热评，返回空
            firstReview = soup.find('div', class_='review-short').find('a', class_='pl')
            url = firstReview['href']
        except:
            return None 
        try: #页面错误，返回空
            html_cont = self.downloader.download(url)
            soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
            hotReview = soup.find('span', property='v:description') #包含了一定html的格式，只需修改一小部分即可直接显示
            hotReviewFormatted = str(hotReview).replace('</br>', '') #删除最后的换行
            hotReviewFormatted = hotReviewFormatted.replace('<br> <br>', '<br><br>') #删除乱码
            return hotReviewFormatted
        except:
            return None
        
    def _get_new_data(self, page_url, soup, threshold):
        res_data = {}
        try: #舍弃页面信息不完全的url
            #url
            res_data['url'] = page_url
            #<span property="v:itemreviewed">代码大全</span>
            res_data['bookName'] = soup.find('span', property='v:itemreviewed').string
            #<strong class="ll rating_num " property="v:average"> 9.3 </strong>
            res_data['score'] = soup.find('strong', class_='ll rating_num ').string
            if float(res_data['score']) < threshold: #评分低于阈值，舍弃
                return None
            '''
            <div id="info" class="">
            <span>
              <span class="pl"> 作者</span>:
              <a class="" href="/search/Steve%20McConnell">Steve McConnell</a>
            </span><br>
            <span class="pl">出版社:</span> 电子工业出版社<br>
            <span class="pl">出版年:</span> 2007-8<br>
            <span class="pl">页数:</span> 138<br>
            <span class="pl">定价:</span> 15.00元<br>
            <span class="pl">ISBN:</span> 9787115281586 #前面有一个空格
            </div>
            '''
            info = soup.find('div', id='info')        
            res_data['author'] = info.find(text=' 作者').next_element.next_element.string
            res_data['publisher'] = info.find(text='出版社:').next_element
            res_data['time'] = info.find(text='出版年:').next_element
            res_data['price'] = info.find(text='定价:').next_element
            res_data['ISBN'] = info.find(text='ISBN:').next_element.strip()
            res_data['intro'] = soup.find('div', class_='intro').find('p').string
        except:
            print 'invalid data'
            return None
        res_data['hotReview'] = self._get_hot_review(soup)
        if res_data['intro'] == None: #舍弃简介为空的页面，一般是旧版的书籍
            return None
        
        return res_data
        
    def parse(self, page_url, html_cont, threshold):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_data(page_url, soup, threshold)
        if new_data is None:
            new_urls = None
        else:
            new_urls = self._get_new_urls(soup)

        return new_urls, new_data





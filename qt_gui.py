# coding=utf-8
'''
Created on 2016年5月24日
 @author: moverzp
 description: 使用pyqt4编写GUI界面
'''
import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import *
import mongoDB

# reload(sys)
# sys.setdefaultencoding('utf-8')


#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class MyGui(QDialog):  
    
    def __init__(self, parent = None):
        QWidget.__init__(self)
        self.mongodb = mongoDB.MongoDB() #数据库操作器
        
        self._init_gui()
        self._init_signal_slot()
        self._show_bookshelf()
          
    def _init_gui(self):
        self.setWindowTitle("GoodBooks")
        #搜索栏布局
        self.searchLabel = QLabel(u'书名')
        self.searchEdit = QLineEdit()
        self.searchButton = QPushButton(u'搜索')
        self.searchTabel = QTableWidget(0, 2)
        self.searchTabel.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        self.searchTabel.setHorizontalHeaderLabels([u'书名', u'评分'])
        self.searchTabel.setSelectionBehavior(QAbstractItemView.SelectRows)  #整行选中的方式
        self.searchTabel.setColumnWidth(0, 220)
        self.searchTabel.setColumnWidth(1, 30) 
        
        searchLayout = QGridLayout()
        searchLayout.addWidget(self.searchLabel, 0, 0)
        searchLayout.addWidget(self.searchEdit, 0, 1)
        searchLayout.addWidget(self.searchButton, 0, 2)
        searchLayout.addWidget(self.searchTabel, 1, 0, 1, 3)
        
        #书籍栏布局
        self.bookNameLabel = QLabel(u'书名：')
        self.bookNameEdit = QLineEdit()
        #bookNameLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.scoreLabel = QLabel(u'评分：')
        self.scoreEdit = QLineEdit()
        self.authorLabel = QLabel(u'作者：')
        self.authorEdit = QLineEdit()
        self.timeLabel = QLabel(u'出版时间：')
        self.timeEdit = QLineEdit()
        self.publisherLabel = QLabel(u'出版社：')
        self.publisherEdit = QLineEdit()
        self.urlLabel = QLabel(u'url')
        self.urlEdit = QLineEdit()
        self.introLabel = QLabel(u'简介：')
        self.introTextEdit = QTextEdit()
        self.hotReviewLabel = QLabel(u'评论：')
        self.hotReviewTextEdit = QTextEdit()
        self.joinBookShelf = QPushButton(u'加入书架')
        self.deleteFromBookShelf = QPushButton(u'从书架删除')
        
        bookLayout = QGridLayout()
        bookLayout.addWidget(self.bookNameLabel, 0, 0)
        bookLayout.addWidget(self.bookNameEdit, 0, 1)
        bookLayout.addWidget(self.scoreLabel, 1, 0)
        bookLayout.addWidget(self.scoreEdit, 1, 1)
        bookLayout.addWidget(self.authorLabel, 2, 0)
        bookLayout.addWidget(self.authorEdit, 2, 1)
        bookLayout.addWidget(self.timeLabel, 3, 0)
        bookLayout.addWidget(self.timeEdit, 3, 1)
        bookLayout.addWidget(self.publisherLabel, 4, 0)
        bookLayout.addWidget(self.publisherEdit, 4, 1)
        bookLayout.addWidget(self.urlLabel, 5, 0)
        bookLayout.addWidget(self.urlEdit, 5, 1)
        bookLayout.addWidget(self.introLabel, 6, 0, Qt.AlignTop)
        bookLayout.addWidget(self.introTextEdit, 6, 1)
        bookLayout.addWidget(self.joinBookShelf, 7, 1)
        bookLayout.addWidget(self.deleteFromBookShelf, 7, 2)
        bookLayout.addWidget(self.hotReviewLabel, 0, 2, Qt.AlignTop)
        bookLayout.addWidget(self.hotReviewTextEdit, 1, 2, 6, 1)
        
        #书架栏布局
        self.bookShelfLabel = QLabel(u'我的书架：')
        self.bookShelfTabel = QTableWidget(0, 1)
        self.bookShelfTabel.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        self.bookShelfTabel.setHorizontalHeaderLabels([u'书名'])
        self.bookShelfTabel.setColumnWidth(0, 180) 
        
        bookShelfLayout = QVBoxLayout()
        bookShelfLayout.addWidget(self.bookShelfLabel)
        bookShelfLayout.addWidget(self.bookShelfTabel)
 
        #推荐栏布局
        self.recommendTabel = QTableWidget(3, 0)
        self.recommendTabel.setVerticalHeaderLabels([u'书名', u'评分', u'操作'])
        self.recommendTabel.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        self.recommendTabel.setSelectionBehavior(QAbstractItemView.SelectColumns) #整列选中的方式
        self.recommendTabel.resizeRowsToContents()
        
        recommendLayout = QGridLayout()
        recommendLayout.addWidget(self.recommendTabel, 0, 0)
        
        #主布局
        mainLayout = QGridLayout(self)
        mainLayout.setSpacing(10)
        mainLayout.addLayout(searchLayout, 0, 0)
        mainLayout.addLayout(bookLayout, 0, 1, 1, 2)
        mainLayout.addLayout(bookShelfLayout, 0, 3)
        mainLayout.addLayout(recommendLayout, 1, 0, 1, 4)
        mainLayout.setRowStretch(0, 3)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 4)
        #mainLayout.setColumnStretch(1, 2)
        mainLayout.setColumnStretch(3, 3)

        mainLayout.setSizeConstraint(QLayout.SetFixedSize) #固定对话框
        
    def _init_signal_slot(self):
        self.connect(self.searchButton, SIGNAL('clicked()'), self.slot_search_keyword)
        self.connect(self.searchTabel, SIGNAL('itemClicked (QTableWidgetItem *)'), self.slot_display_book_information)
        
        self.connect(self.joinBookShelf, SIGNAL('clicked()'), self.slot_join_bookshelf)
        self.connect(self.deleteFromBookShelf, SIGNAL('clicked()'), self.slot_delete_from_bookshelf)
        
        self.connect(self.bookShelfTabel, SIGNAL('itemClicked (QTableWidgetItem *)'), self.slot_display_book_information_on_the_shelf)
        
    def _show_bookshelf(self):
        doc = self.mongodb.get_user_docs()
        self.bookshelfDoc = doc.clone()
        #显示书架上的书
        self.bookShelfTabel.clearContents()
        self.bookShelfTabel.setRowCount(0)
        row = 0
        for i in doc:
            self.bookShelfTabel.insertRow(row)
            self.bookShelfTabel.setItem(row, 0, QTableWidgetItem( i['bookName'] ))
            row += 1
        
        
    #槽函数    
    def slot_search_keyword(self):
        keyword = self.searchEdit.text()
        if keyword is None:
            return
        doc = self.mongodb.search_book(keyword)
        self.bookDoc = doc.clone() #保留光标
        #显示查询结果
        self.searchTabel.clearContents()
        self.searchTabel.setRowCount(0)
        row = 0
        for i in doc:
            self.searchTabel.insertRow(row)
            self.searchTabel.setItem(row, 0, QTableWidgetItem( i['bookName'] ))
            self.searchTabel.setItem(row, 1, QTableWidgetItem( i['score'] ))
            row += 1
            
    def slot_display_book_information(self):
        curRow = self.searchTabel.currentRow()
        book = self.bookDoc[curRow]
        
        self.bookNameEdit.setText(book['bookName'].strip())
        self.scoreEdit.setText(book['score'].strip())
        self.authorEdit.setText(book['author'].strip())
        self.publisherEdit.setText(book['publisher'].strip())
        self.timeEdit.setText(book['time'].strip())
        self.urlEdit.setText(book['url'].strip())
        self.introTextEdit.setText(book['intro'])
        self.hotReviewTextEdit.setHtml(book['hotReview'])
        
    def slot_join_bookshelf(self):
        book = {}
        book['bookName'] = str(self.bookNameEdit.text())
        book['url'] = str(self.urlEdit.text())
        self.mongodb.add_data_to_user(book)
        self._show_bookshelf()
        
    def slot_delete_from_bookshelf(self):
        url = str(self.urlEdit.text())
        self.mongodb.remove_data_from_user(url)
        self._show_bookshelf()    
    
    def slot_display_book_information_on_the_shelf(self):
        curRow = self.bookShelfTabel.currentRow()
        url = self.bookshelfDoc[curRow]['url']
        book = self.mongodb.search_book_by_url(url)
        
        self.bookNameEdit.setText(book['bookName'].strip())
        self.scoreEdit.setText(book['score'].strip())
        self.authorEdit.setText(book['author'].strip())
        self.publisherEdit.setText(book['publisher'].strip())
        self.timeEdit.setText(book['time'].strip())
        self.urlEdit.setText(book['url'].strip())
        self.introTextEdit.setText(book['intro'])
        self.hotReviewTextEdit.setHtml(book['hotReview'])
       
##############################################################################################
    def recommend_good_books(self):
        #获取书架上所有书籍的url，并统计其频数
        urlFrequency = {} #保存推荐书籍url的频数
        for i in self.bookshelfDoc:
            book = self.mongodb.search_book_by_url(i['url'])
            for recommendUrl in book['recommendUrls']:
                if recommendUrl not in urlFrequency.keys():
                    urlFrequency[recommendUrl] = 0
                urlFrequency[recommendUrl] += 1
        
        #按照频数排序取前10
    
    
    
app=QApplication(sys.argv)  
gui = MyGui()
gui.show()
app.exec_()  
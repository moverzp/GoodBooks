# coding=utf-8
'''
Created on 2016年5月24日
 @author: moverzp
 description: 使用pyqt4编写GUI界面
'''
import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import *
from shelve import Shelf

#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class MyGui(QDialog):  
    
    def __init__(self, parent = None):
        QWidget.__init__(self)
        self.setWindowTitle("GoodBooks")
        
        #搜索栏布局
        searchLabel = QLabel(u'书名')
        searchEdit = QLineEdit()
        searchButton = QPushButton(u'搜索')
        searchTabel = QTableWidget(2, 3)
        searchTabel.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        searchTabel.setHorizontalHeaderLabels([u'书名', u'评分', u'操作'])
        searchTabel.setColumnWidth(0, 150) 
        searchTabel.setColumnWidth(1, 30) 
        searchTabel.setColumnWidth(2, 45) 
        searchTabel.setItem(0, 0, QTableWidgetItem(u'统计学习方法'))
        searchTabel.setItem(0, 1, QTableWidgetItem(u'9.0'))
        
        searchLayout = QGridLayout()
        searchLayout.addWidget(searchLabel, 0, 0)
        searchLayout.addWidget(searchEdit, 0, 1)
        searchLayout.addWidget(searchButton, 0, 2)
        searchLayout.addWidget(searchTabel, 1, 0, 1, 3)

        #书籍栏布局
        bookNameLabel = QLabel(u'书名：')
        bookNameEdit = QLineEdit()
        scoreLabel = QLabel(u'评分：')
        scoreEdit = QLineEdit()
        authorLabel = QLabel(u'作者：')
        authorEdit = QLineEdit()
        timeLabel = QLabel(u'出版时间：')
        timeEdit = QLineEdit()
        publisherLabel = QLabel(u'出版社：')
        publisherEdit = QLineEdit()
        introLabel = QLabel(u'简介：')
        introTextEdit = QTextEdit()
        hotReviewLabel = QLabel(u'评论：')
        hotReviewTextEdit = QTextEdit()
        
  
        bookLayout = QGridLayout()
        bookLayout.addWidget(bookNameLabel, 0, 0)
        bookLayout.addWidget(bookNameEdit, 0, 1)
        bookLayout.addWidget(scoreLabel, 1, 0)
        bookLayout.addWidget(scoreEdit, 1, 1)
        bookLayout.addWidget(authorLabel, 2, 0)
        bookLayout.addWidget(authorEdit, 2, 1)
        bookLayout.addWidget(timeLabel, 3, 0)
        bookLayout.addWidget(timeEdit, 3, 1)
        bookLayout.addWidget(publisherLabel, 4, 0)
        bookLayout.addWidget(publisherEdit, 4, 1)
        bookLayout.addWidget(introLabel, 5, 0, Qt.AlignTop)
        bookLayout.addWidget(introTextEdit, 5, 1)
        bookLayout.addWidget(hotReviewLabel, 0, 2, Qt.AlignTop)
        bookLayout.addWidget(hotReviewTextEdit, 1, 2, 5, 1)
        
        #书架栏布局
        bookShelfLabel = QLabel(u'我的书架：')
        bookShelfTabel = QTableWidget(8, 2)
        bookShelfTabel.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        bookShelfTabel.setHorizontalHeaderLabels([u'书名', u'操作'])
        bookShelfTabel.setColumnWidth(0, 150) 
        bookShelfTabel.setColumnWidth(1, 32) 
        bookShelfTabel.setItem(0, 0, QTableWidgetItem(u'集体智慧编程'))
        bookShelfTabel.setItem(0, 1, QTableWidgetItem(u'展开'))
        
        bookShelfLayout = QVBoxLayout()
        bookShelfLayout.addWidget(bookShelfLabel)
        bookShelfLayout.addWidget(bookShelfTabel)
 
        #推荐栏布局
        recommendTabel = QTableWidget(3, 8)
        recommendTabel.setVerticalHeaderLabels([u'书名', u'评分', u'操作'])
        recommendTabel.setEditTriggers(QAbstractItemView.NoEditTriggers) #禁止编辑
        recommendTabel.resizeRowsToContents()
        recommendTabel.setItem(0, 0, QTableWidgetItem(u'代码大全（第2版）'))
        recommendTabel.setItem(1, 0, QTableWidgetItem(u'9.2分'))
        
        recommendLayout = QGridLayout()
        recommendLayout.addWidget(recommendTabel, 0, 0)
        
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
        
        
app=QApplication(sys.argv)  
gui = MyGui()
gui.show()
app.exec_()  
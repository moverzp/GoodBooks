# coding=utf-8
'''
Created on 2016/05/22
 @author: moverzp
 description: 
'''
from Tkinter import *
#from ttk import *

root = Tk()
root.wm_title('我的书籍推荐')

#左侧搜索栏
searchLabel = Label(root, text='书名')
searchLabel.grid(row=0, column=0, sticky = W)

searchEntry = Entry(root, text='请输入搜索关键词')
searchEntry.grid(row=0, column=1, sticky=W)
#searchEntry.insert(0, '请输入搜索关键词')

searchButton = Button(root, text='搜索')
searchButton.grid(row=0, column=2, sticky=W)

searchLb = Listbox(root, selectmode=EXTENDED)
searchLb.grid(row=1, column=1)
searchLb.insert(END, "代码大全")
searchLb.insert(END, '推荐系统实践')
searchLb.insert(END, '统计学习方法')



root.mainloop()
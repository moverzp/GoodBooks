![](http://7xn9xp.com1.z0.glb.clouddn.com/16-7-2/29523713.jpg)
# GoodBooks

##目标
从豆瓣爬取书籍，使用推荐算法推荐可能喜欢的书籍。

给定初始豆瓣页面(默认为《代码大全》)url，然后提取该网页书籍的名称，评分，作者，出版社，出版时间，价格，ISBN，简介，热评和豆瓣推荐书籍的url。只要url管理器中的未爬取url集合不为空或者未到达指定爬取的次数，就一直爬取网页的信息以及新的url。

[点击查看原图](http://7xn9xp.com1.z0.glb.clouddn.com/16-7-4/43366047.jpg)
![](http://7xn9xp.com1.z0.glb.clouddn.com/16-7-4/43366047.jpg)

##使用Python2.7编写，需要的Python模块：
* `urllib2`, 高级Web交流模块，根据支持的协议下载数据
* `beautifulsoup`, 处理HTML/XML
* `re`, 提供正则表达式相关操作
* `pymongo`, 连接MongoDB数据库，并对其进行操作
* `pyExcelerator`, 提供Excel相关的操作
* `PyQt4`, GUI编写

##使用说明
* 安装上面提到的Python模块
* 安装mongoDB数据库，**每次运行程序之前一定要开启服务器mongod.exe**
* 在mongoDB数据中创建GoodBooks数据库（[点击查看方法](http://www.yiibai.com/mongodb/mongodb_create_collection.html)），建立以下集合：
    * `newUrls`, 保存未爬取的url
    * `oldUrls`, 保存已爬取的url
    * `book`, 保存爬取的书籍信息
    * `notFoundUrls`, 保存404错误的url
    * `user`, 保存用户添加的书籍
* 先生成文件`cookie1.txt`和`cookie2.txt`，依次点击“保存cookie1”，“保存cookie2”按钮
![](http://7xn9xp.com1.z0.glb.clouddn.com/16-7-2/57800400.jpg)

##文件
* `spider_main.py`, 爬虫引擎，进行各项任务的调度
* `url_manager.py`, url管理器，管理已爬取和未爬取的url，提供添加url，获取url，查询是否还有未爬取的url等功能
* `html_downloader.py`, html下载器
* `html_parser.py`, html分析器，提取html中的数据和url
* `mongoDB.py`, 数据库操作器，替代url管理器，html输出器
* `qt_gui.py`, 用户界面
* `recommend`, 推荐器，实现各种推荐算法

##2016.07.02
* 编写了爬虫界面，通过点击“爬虫窗口”按钮进入
* 创建了推荐器，已经实现了“基于物品的协同过滤算法”
* 修复了一些bug


##2016.06.10
* 加入`qt_gui.py`，创建用户界面
* 按照频数推荐书籍，其实不算推荐算法，后面更新
* 修复一些bug

##2016.05.15
* 经过实验，还是选择了单线程爬取，双线程就会禁止访问
* 双线程其实已经写好了（由于效果不好，已退回原来版本，但可以使用git恢复到多线程版本），只是未开启，可以设置代理然后开启双线程
* 经过测试，一个小时大概能访问2000+书籍页面，如果加上爬取热评需要进入页面的次数，则为3000+页面/h
* `GoodBooks.xls`中包含了所有“有效书籍”的基本信息，不包含推荐书籍的url以及热评

##2016.05.04
* 加入`mongoDB.py`, 数据库操作器
* 创建4个MongoDB集合，newUrls, oldUrls, notFoundUrls, book
* 在数据库操作器中实现url管理器的功能，这样就可以断点爬取了
* 在数据库操作器中实现html输出器的功能，将book集合中所有文档的关键信息打印成Excel文件
* 修正了部分bug
* 截止合并时已爬取6000本有效书籍，详见GoodBooks.xls


##2016.04.22
* 增加ISBN爬取
* 增加热评爬取
* 修改html输出器，显示ISBN以及热评

##2016.04.11
* 使用队列记录未爬取的url，避免随机获取url而导致越爬越偏的现象

##2016.04.04
* 新建工程，能够爬取书籍的简单信息。

##备注
* [我的博客](http://blog.csdn.net/xuelabizp)中有代码的详细解释，欢迎访问
* 会不断的更新与完善，例如增加代理，多线程爬取，断点爬取等功能
* 最终目标是使用自己的推荐算法推荐书籍以及编写GUI





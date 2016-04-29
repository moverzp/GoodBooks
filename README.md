# GoodBooks

##目标
获得自己可能喜欢的优秀书籍的信息。

给定初始豆瓣页面(默认为《代码大全》)url，然后提取该网页书籍的名称，评分，作者，出版社，出版时间，价格，ISBN，简介，热评和豆瓣推荐书籍的url。只要url管理器中的未爬取url集合不为空或者未到达指定爬取的次数，就一直爬取网页的信息以及新的url。

##使用Python编写，需要的Python模块：
* urllib2
* beautifulsoup
* re


##文件
* spider_main.py, 爬虫引擎，进行各项任务的调度
* url_manager.py, url管理器，管理已爬取和未爬取的url，提供添加url，获取url，查询是否还有未爬取的url等功能
* html_downloader.py, html下载器
* html_parser.py, html分析器，提取html中的数据和url
* html_outputer.py, html输出器，将提取的信息以一种较为友好的html形式保存


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





# elasticsearch_web_server
a www server for accept search request, and then get data from es, show it to user
一个演示版本for搜索结果展示，相当于搜索的web服务部分。目前仅作为个人测试用，不建议下载试用
1.使用python flask 框架开发，使用前需要安装如下依赖(以mac为例)：
1) 安装python: brew install python
2) 安装flask: pip install flask
2.使用时需要先修改搜索服务的ip和端口，然后调用python main.py
3.浏览器访问: http:127.0.0.1:5000 (简单的对搜索词进行飘红展示)。

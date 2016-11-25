# elasticsearch_web_server
a www server for accept search request, and then get data from search engine, show it to user
一个演示版本for搜索结果展示，相当于搜索的web服务部分。目前仅作为个人测试用，不建议下载试用
说明:此服务只是一个搜索和推荐结果的web展示，需要先部署搜索服务和推荐服务。
1.使用python flask 框架开发，使用前需要安装如下依赖(以mac为例)：
1) 安装python: brew install python
2) 安装flask: pip install flask
2.使用时需要先修改modules/mod_search.py 搜索服务和推荐服务的ip和端口，然后调用脚本./start.sh启动服务
3.浏览器访问: http:127.0.0.1:5100 (输入关键词回车可查看搜索结果)。
4.调用脚本./stop.sh停止服务

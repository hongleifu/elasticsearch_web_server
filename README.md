线上部署:
1.把整个工程拷贝到39\40的/unknown/svr/finance_one/ 目录下的search_new 目录中
2.修改modules/mod_public_config.py文件中的:
  get_search_service_base_url() 函数为:
      return 'http://10.120.66.39:9200/finance/_search?pretty'
  get_search_service_classify_url()函数为:
    return 'http://10.120.66.39:9200/finance/_search?pretty'
3.测试:/usr/local/python/bin/python main.py
4.mv search_new search
5.启动服务:nohup /usr/local/python/bin/python  main.py --search_web_server > search_web_server.log 2>&1 &

本地部署：
1.grep jinrongdao.unknown.cn ./ -r,把所有搜索相关的域名加上5100端口，社区相关的加上6100端口
2.修改 /etc/hosts 文件，加上映射：
  127.0.0.1       jinrongdao.unknown.cn  
  127.0.0.1       social.jinrongdao.unknown.cn  
3.pyhton main.py 启动
4. 在浏览器输入jinrongdao.unknown.cn:5100测试效果

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

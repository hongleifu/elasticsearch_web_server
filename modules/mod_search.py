#coding=utf-8
import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import datetime
import logging
log_file="myapp.log"
logging.basicConfig(filename = log_file, level = logging.DEBUG)
sys.path.append(sys.path[0])

def get_search_service_base_url():
    return 'localhost:9200/finance/toutiao/_search?pretty'
def get_recommend_service_base_url():
    return "http://jinrongdao.com:5200/recommend?"

def get_search_service_classify_url():
    #return 'localhost:9200/finance/laws_article/_search?pretty'
    return 'localhost:9200/finance/_search?pretty'

def service(query):
    print "enter mod search"
    logging.info("enter mod search")
    recommend_query=query
    query=query.encode('utf8')
    # get search result from search engine
    return_value=[]
    try:
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,get_search_service_base_url())
        query_condition = '{"query": { "match": { "title": '+ '"'+query+'"'+' } },"size":100}'
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_value=result_dict['hits']['hits'] 
        query_unicode = query.decode('utf8')
        for item in return_value:
            item["_source"]["content"] = item["_source"]["content"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
            item["_source"]["title"] = item["_source"]["title"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
        
    except Exception,e:
        print "get search result error:",e

    
    print "begin recommend"
    logging.info("begin recommend")
    #get recommend result of key word  from recommend engine
    param_dict={}
    param_dict['query']=recommend_query.encode('utf8')
    param_dict['type']='key_word'
    logging.info("param_dict")
    url=get_recommend_service_base_url()+urllib.urlencode(param_dict)
    logging.info("url:"+url)
    print 'get recommend :',url
    recommend=[]
    try:
        req=urllib2.Request(url)
        res_data=urllib2.urlopen(req)
        res=res_data.read()
        res=res.decode('utf8')
        result_dict_recommend = json.loads(res)
        recommend=result_dict_recommend['data']
        logging.info("get result :"+url)
    except Exception,e:
        logging.info("exception"+str(e))
        print "get recommend of keyword result error:",e

    #return all result
    return return_value, query.decode('utf8'), recommend

#search for classified article
def service_classify(tag):
    tag=tag.encode('utf8')
    if tag=='1':
      tag='法规速递'
    if tag=='2':
      tag='行业动态'
    
    # get search result from search engine
    return_value=[]
    try:
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tag": '+ '"'+tag+'"'+' } },\
          "size":1000,\
          "sort":{"insert_time":{"order":"desc"}},\
          "filter":{"range":{"level":{"gte":300,"lte":2000}}}\
        }'

       # date=get_day_befor_today_n_days(2)
       # date_time=(str)(date)
       # query_condition = '{\
       #   "query": { "match": { "tag": '+ '"'+tag+'"'+' } },\
       #   "size":100,\
       #   "sort":{"level":{"order":"desc"}},\
       #   "filter":{"range":{"insert_time":{"gte":'+'"' + date_time +'"' +'}}}\
       # }'
        print "search classify:",query_condition
       # query_condition = '{\
       #   "query":{
       #     "filtered":{
       #       "query": { "match": { "tag": '+ '"'+tag+'"'+' } },\
       #       "filter":{"range":{"publish_time":{"gte":'+'"' + date_time +'"' +'}}},\
       #       "sort":{"level":{"order":"desc"}}\
       #       "size":10\
       #     }\
       #   }\
       # }'
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_value=result_dict['hits']['hits'] 
        tag_unicode = tag.decode('utf8')
        print "search result:",len(return_value)
        for item in return_value:
            item["_source"]["content"] = item["_source"]["content"].replace(tag_unicode,'<font color="red">'+tag_unicode+'</font>')
            item["_source"]["title"] = item["_source"]["title"].replace(tag_unicode,'<font color="red">'+tag_unicode+'</font>')
    except Exception,e:
        print "get search result error:",e

    #return all result
    recommend=[]
    return return_value, tag.decode('utf8')

def get_day_befor_today_n_days(n):
  today=datetime.date.today()
  delta_day=datetime.timedelta(days=n)
  result = today-delta_day
  return result

#coding=utf-8
import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import datetime
import random,re
from Logger import *
sys.path.append(sys.path[0])
from modules import mod_public_config

def service(query,start,end):
    recommend_query=query
    adverse_query=query
    query=query.encode('utf8')

    # get search result from search engine
    return_value=[]
    try:
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_base_url())
        query_condition = '{"query": { "match": { "title": '+ '"'+query+'"'+' } },"size":60}'
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_value=result_dict['hits']['hits'] 
        query_unicode = query.decode('utf8')
        return_value=deal_result(return_value,query_unicode,start,end)
        Logger.infoLogger.info("search_keyword_"+query.decode('utf8'))
    except Exception,e:
        Logger.infoLogger.info(e)

    #get recommend result of key word  from recommend engine
    Logger.infoLogger.info("get recommend.....")
    param_dict={}
    param_dict['query']=recommend_query.encode('utf8')
    param_dict['type']='key_word'
    url=mod_public_config.get_recommend_service_base_url()+urllib.urlencode(param_dict)
    Logger.infoLogger.info("get recommend url:"+url)
    recommend=[]
    try:
        req=urllib2.Request(url)
        res_data=urllib2.urlopen(req)
        res=res_data.read()
        res=res.decode('utf8')
        result_dict_recommend = json.loads(res)
        recommend=result_dict_recommend['data']
        Logger.infoLogger.info("get recommend succ! result :"+url)
    except Exception,e:
        Logger.infoLogger.info("get recommend of keyword result exception:"+str(e))

    #get adverses, and this will open in future 
    adverses=[]

    #return all result
    return return_value, query.decode('utf8'), recommend, adverses

#search for classified article
def service_classify(tag,start,end):
    return_value=[]
    tag=tag.encode('utf8')
    if tag=='0':
        tag='首页'
        tag_unicode = tag.decode('utf8')
        resort_result=resort_classify_first_result(search_index_realtime(start,end))
        return_value=deal_result(resort_result,tag_unicode,start,end)
        return_value_2=search_index_recent(start,end)
        random.seed()
        random.shuffle(return_value_2)
        return_value.extend(deal_result(return_value_2,tag_unicode,start,end))
    elif tag=='1':
        tag='法规速递'
       # tag_unicode = tag.decode('utf8')
       # resort_result=resort_classify_first_result(get_fagui_realtime(start,end))
       # return_value=deal_result(resort_result,tag_unicode,start,end)
       # return_value_2=get_index_recent(start,end)
       # random.seed()
       # random.shuffle(return_value_2)
       # return_value.extend(deal_result(return_value_2,tag_unicode,start,end))
    elif tag=='2':
        tag='行业动态'
        tag_unicode = tag.decode('utf8')
        resort_result=resort_classify_first_result(search_hangye_realtime(start,end))
        return_value=deal_result(resort_result,tag_unicode,start,end)
        return_value_2=search_hangye_recent(start,end)
        random.seed()
        random.shuffle(return_value_2)
        return_value.extend(deal_result(return_value_2,tag_unicode,start,end))
    elif tag=='3':
        tag='股票'
        tag_unicode = tag.decode('utf8')
        resort_result=resort_classify_first_result(search_stock_realtime(start,end))
        return_value=deal_result(resort_result,tag_unicode,start,end)
        return_value_2=search_stock_recent(start,end)
        random.seed()
        random.shuffle(return_value_2)
        return_value.extend(deal_result(return_value_2,tag_unicode,start,end))
    elif tag=='4':
        tag='房产'
        tag_unicode = tag.decode('utf8')
        resort_result=resort_classify_first_result(search_house_realtime(start,end))
        return_value=deal_result(resort_result,tag_unicode,start,end)
        return_value_2=search_house_recent(start,end)
        random.seed()
        random.shuffle(return_value_2)
        return_value.extend(deal_result(return_value_2,tag_unicode,start,end))
    Logger.infoLogger.info("search_tag_"+tag.decode('utf8'))
    #return all result
    return_value_dedup=dedup_search_result(return_value)
    return return_value_dedup, tag.decode('utf8')

def get_day_befor_today_n_days(n):
  today=datetime.date.today()
  delta_day=datetime.timedelta(days=n)
  result = today-delta_day
  return result


def get_imgs_from_content_html(content_html):
    imgs = []
    if content_html:
        p = re.compile(r"""<img\s.*?\s?src\s*=\s*['|"]?([^\s'"]+).*?>""", re.I)
        img_array = p.findall(content_html)
        if img_array and len(img_array) > 0:
            count = 0
            for i in range(len(img_array)):
                if img_array[i].find('http')!=-1 or img_array[i].find('www')!=-1:
                    imgs.append(img_array[i])
                    if count > 9:
                        break
                    count += 1
    return imgs

#resort search result. the top1,2,3 and others
def resort_classify_first_result(search_result):
    return_value=[]
    if len(search_result) > 10:
        result_top10=search_result[0:10]
        result_after_top10=search_result[10:]
        random.seed()
        random.shuffle(result_top10)
        return_value=result_top10[0:2]
        result_after_two=result_top10[2:]
        result_after_two.extend(result_after_top10)
        random.seed()
        random.shuffle(result_after_two)
        return_value.extend(result_after_two)
    else:
        return_value=search_result
    return return_value

# deal result, extract imgs and mark keyword red 
def deal_result(resort_result,query_unicode,start,end):
    for index in range(len(resort_result)):
        if index < start or index >= end:
            continue
        item = resort_result[index]
        item["_source"]["content"] = item["_source"]["content"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
        item["_source"]["title"] = item["_source"]["title"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
        item["_source"]["imgs"] = get_imgs_from_content_html(item["_source"]["content_html"])
    return resort_result

#get adverses of search keyword
def get_adverses(adverse_query):
    Logger.infoLogger.info("get adverse.....")
    adverse_param_dict={}
    adverse_param_dict['query']=adverse_query.encode('utf8')
    adverse_param_dict['type']='search_news'
    adverse_param_dict['result_num']=4
    adverse_url=mod_public_config.get_adverse_service_base_url()+urllib.urlencode(adverse_param_dict)
    Logger.infoLogger.info("get adverse url:"+adverse_url)
    try:
        req=urllib2.Request(adverse_url)
        res_data=urllib2.urlopen(req)
        res=res_data.read()
        Logger.infoLogger.info("result is:"+str(res))
        res=res.decode('utf8')
        result_dict_adverse = json.loads(res)
        adverses=result_dict_adverse['data']
        Logger.infoLogger.info("result data is:"+str(adverses))
    except Exception,e:
        Logger.infoLogger.info("get adverse of keyword result exception:"+str(e))
    return adverses

#get days from n days ago to today,return a list of datetime
def get_days_to_today(n):
    days=[]
    for i in range(n):
        the_day=datetime.datetime.today()-datetime.timedelta(days=i)
        days.append(the_day)
    return days

#get days from n days ago to today,return a list of str 
def get_days_to_today_str(n):
    days=[]
    for i in range(n):
        the_day=datetime.datetime.today()-datetime.timedelta(days=i)
        days.append(datetime.datetime.strftime(the_day,'%Y-%m-%d'))
    return days

#get days between from m days ago to ndays ago, m<n, return a list of str 
def get_days_between_str(m,n):
    days=[]
    for i in range(n-m+1):
        the_day=datetime.datetime.today()-datetime.timedelta(days=m+i)
        days.append(datetime.datetime.strftime(the_day,'%Y-%m-%d'))
    return days

#format list of str of date to '20170810,20170813....'
def format_date_str(date_str):
    f_date=[]
    for item in date_str:
        f_date.append(item.replace('-',''))
    return ",".join(f_date)

def search_house_realtime(start,end):
    return_result=[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "房产" } },\
          "size":15,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(0,1))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result

def search_house_recent(start,end):
    return_result =[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "房产" } },\
          "size":100,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(2,30))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result


def search_stock_realtime(start,end):
    return_result =[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "股票" } },\
          "size":20,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(0,1))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result

def search_stock_recent(start,end):
    return_result=[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "股票" } },\
          "size":100,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(2,30))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result

def search_hangye_realtime(start,end):
    return_result=[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "行业动态" } },\
          "size":30,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(0,1))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result

def search_hangye_recent(start,end):
    return_result=[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "行业动态" } },\
          "size":200,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(2,30))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result

def search_index_realtime(start,end):
    return_result=[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "行业动态" } },\
          "size":15,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(0,1))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])

        c1=pycurl.Curl()
        buf1=cStringIO.StringIO()
        c1.setopt(c1.URL,mod_public_config.get_search_service_classify_url())
        query_condition1 = '{\
          "query": { "match": { "tags": "股票" } },\
          "size":15,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(0,1))+ ']}}\
        }'
        print query_condition1
        Logger.infoLogger.info("search classify:"+query_condition1)
        c1.setopt(c1.POSTFIELDS,query_condition1)
        c1.setopt(c1.WRITEFUNCTION, buf1.write)
        c1.perform()
        result1 = buf1.getvalue()
        result_dict1 = json.loads(result1)
        buf1.close()
        return_result.extend(result_dict1['hits']['hits'])
        
        c2=pycurl.Curl()
        buf2=cStringIO.StringIO()
        c2.setopt(c2.URL,mod_public_config.get_search_service_classify_url())
        query_condition2 = '{\
          "query": { "match": { "tags": "房产" } },\
          "size":15,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(0,1))+ ']}}\
        }'
        print query_condition2
        Logger.infoLogger.info("search classify:"+query_condition2)
        c2.setopt(c2.POSTFIELDS,query_condition2)
        c2.setopt(c2.WRITEFUNCTION, buf2.write)
        c2.perform()
        result2 = buf2.getvalue()
        result_dict2 = json.loads(result2)
        buf2.close()
        return_result.extend(result_dict2['hits']['hits'])
        
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result

def search_index_recent(start,end):
    return_result=[]
    try:
        #first search,search data in past two days
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,mod_public_config.get_search_service_classify_url())
        query_condition = '{\
          "query": { "match": { "tags": "行业动态" } },\
          "size":100,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(2,30))+ ']}}\
        }'
        print query_condition
        Logger.infoLogger.info("search classify:"+query_condition)
        c.setopt(c.POSTFIELDS,query_condition)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        result = buf.getvalue()
        result_dict = json.loads(result)
        buf.close()
        return_result.extend(result_dict['hits']['hits'])

        c1=pycurl.Curl()
        buf1=cStringIO.StringIO()
        c1.setopt(c1.URL,mod_public_config.get_search_service_classify_url())
        query_condition1 = '{\
          "query": { "match": { "tags": "股票" } },\
          "size":60,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(2,30))+ ']}}\
        }'
        print query_condition1
        Logger.infoLogger.info("search classify:"+query_condition1)
        c1.setopt(c1.POSTFIELDS,query_condition1)
        c1.setopt(c1.WRITEFUNCTION, buf1.write)
        c1.perform()
        result1 = buf1.getvalue()
        result_dict1 = json.loads(result1)
        buf1.close()
        return_result.extend(result_dict1['hits']['hits'])
        
        c2=pycurl.Curl()
        buf2=cStringIO.StringIO()
        c2.setopt(c2.URL,mod_public_config.get_search_service_classify_url())
        query_condition2 = '{\
          "query": { "match": { "tags": "房产" } },\
          "size":40,\
          "sort":{"level":{"order":"desc"}},\
          "filter":{"terms":{"insert_date":['+format_date_str(get_days_between_str(2,30))+ ']}}\
        }'
        print query_condition2
        Logger.infoLogger.info("search classify:"+query_condition2)
        c2.setopt(c2.POSTFIELDS,query_condition2)
        c2.setopt(c2.WRITEFUNCTION, buf2.write)
        c2.perform()
        result2 = buf2.getvalue()
        result_dict2 = json.loads(result2)
        buf2.close()
        return_result.extend(result_dict2['hits']['hits'])
        
    except Exception,e:
        Logger.infoLogger.info("get search result error:"+str(e))
    return return_result

def dedup_search_result(result):
    return_result=[]
    titles=set()
    for item in result:
        if item['_source']['title'] not in titles:
            titles.add(item['_source']['title'])
            return_result.append(item)
        else:
            Logger.infoLogger.info("repeat news")
    return return_result


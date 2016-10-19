import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import httplib 
sys.path.append(sys.path[0])


def get_search_service_base_url():
    return 'localhost:9200/finance/_search?pretty'
def get_recommend_service_base_url():
    return "http://127.0.0.1:5200/recommend?"

def service(request):
    page_no=request.form.get("page_no",1)
    num_perpage=request.form.get("num_perpage",5)
    query=request.form.get("query"," ")
    query=query.encode('utf8')
    print "page no:",page_no,"per:",num_perpage,"query:",query

    # get search result from search engine
    return_value=[]
    try:
        c=pycurl.Curl()
        buf=cStringIO.StringIO()
        c.setopt(c.URL,get_search_service_base_url())
        query_condition = '{"query": { "match": { "title": '+ '"'+query+'"'+' } },"size":15}'
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

    
    #get recommend result of key word  from recommend engine
    param_dict={}
    param_dict['query']=query
    param_dict['type']='key_word'
    url=get_recommend_service_base_url()+urllib.urlencode(param_dict)
    recommend=[]
    try:
        req=urllib2.Request(url)
        res_data=urllib2.urlopen(req)
        res=res_data.read()
        print res
        res=res.decode('utf8')
        result_dict_recommend = json.loads(res)
        recommend=result_dict_recommend['data']
    except Exception,e:
        print "get recommend of keyword result error:",e

    #return all result
    return return_value,query.decode('utf8'), recommend

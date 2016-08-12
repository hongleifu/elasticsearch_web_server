import sys
import pycurl
import cStringIO
import json
import urllib 
sys.path.append(sys.path[0])
def service(request):
    page_no=request.form.get("page_no",1)
    num_perpage=request.form.get("num_perpage",5)
    query=request.form.get("query","")
    query=query.encode('utf8')
    print "page no:",page_no,"per:",num_perpage,"query:",query
    c=pycurl.Curl()
    buf=cStringIO.StringIO()
    c.setopt(c.URL,'localhost:9200/finance/_search?pretty')
  #  query_condition = \
 #      '{"query": {"bool": {"should": [{ "match": { "title":'+ query+' } },{ "match": { "content": '+query+' } }]}}}'
    query_condition = '{"query": { "match": { "title": '+ '"'+query+'"'+' } },"size":15}'
   # c.setopt(c.POSTFIELDS,'{"query": { "match_all": {} }}')
    c.setopt(c.POSTFIELDS,query_condition)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    result = buf.getvalue()
#    result = result.decode('utf8')
#    print "result is--------------------------:\n",result
    #print "result type is : ",type(result)
#    result = result.replace('false',"''")
    result_dict = json.loads(result)
#    print "result dict is: ",type(result_dict),result_dict['hits']['hits']
#    print result_dict["hits"]["hits"]
    buf.close()
#    model=[]
#    model.append(result_dict['hits']['hits'])
    return_value=result_dict['hits']['hits'] 
    query_unicode = query.decode('utf8')
    for item in return_value:
        item["_source"]["content"] = item["_source"]["content"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
        item["_source"]["title"] = item["_source"]["title"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
       # print item["_source"]["content"]
    return return_value,query.decode('utf8') 
#    model = []
#    for data in object_list:
#        data_dict = {}
#        data_dict["id"] = data.id
#        data_dict["taskname"] = data.taskname
#        data_dict["tasktype"] = data.tasktype
#        data_dict["host"] = data.host
#        data_dict["dir"] = data.dir
#        data_dict["taskcontent"] = data.taskcontent
#        data_dict["taskstate"] = data.state
#        model.append(data_dict)
#    return model,page_no,len(model),num_perpage

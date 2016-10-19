import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import httplib 
from flask import session
from modules import mod_public_config

def service(request):
  model = {}
  recommend={}

  name = request.form['name']
  password = request.form['password']
  session['userinfo'] = {'name':name}
  model['result'] = True

  #get recommend result of user  from recommend engine
  param_dict={}
  param_dict['type']='user'
  param_dict['name']=name
  url=mod_public_config.get_recommend_service_base_url()+urllib.urlencode(param_dict)
  recommend_like=[]
  try:
      req=urllib2.Request(url)
      res_data=urllib2.urlopen(req)
      res=res_data.read()
      print 'user recommend result is:',res
      res=res.decode('utf8')
      result_dict_recommend = json.loads(res)
      recommend_like=result_dict_recommend['data']
  except Exception,e:
      print "get recommend of keyword result error:",e

  # get search result from search engine
  recommend_query=""
  if len(recommend_like) > 0:
    recommend_query=recommend_like[0]
  print 'recommend key word is:',recommend_query
  recommend_query = recommend_query.encode('utf8')
  return_value=[]
  try:
      c=pycurl.Curl()
      buf=cStringIO.StringIO()
      c.setopt(c.URL,mod_public_config.get_search_service_base_url())
      query_condition = '{"query": { "match": { "title": '+ '"'+recommend_query+'"'+' } },"size":15}'
      c.setopt(c.POSTFIELDS,query_condition)
      c.setopt(c.WRITEFUNCTION, buf.write)
      c.perform()
      result = buf.getvalue()
      result_dict = json.loads(result)
      buf.close()
      return_value=result_dict['hits']['hits'] 
      query_unicode = recommend_query.decode('utf8')
      for item in return_value:
          item["_source"]["content"] = item["_source"]["content"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
          item["_source"]["title"] = item["_source"]["title"].replace(query_unicode,'<font color="red">'+query_unicode+'</font>')
  except Exception,e:
      print "get search result error:",e
  recommend['data']=return_value
  return model,return_value
  #user = mysqldb.User.query.filter_by(name=name,password=password).first()
 # if user is not None:
 # 	session['userinfo'] = {'name':user.name, 'id':user.id}
 # 	model['ret'] = True
 # else:
 # 	model['ret'] = False

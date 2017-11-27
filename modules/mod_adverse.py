#coding=utf-8
import time
import urllib 
import urllib2 
import pycurl 
import cStringIO
import json

from Logger import *

def get_adverse_service_click_base_url():
    return "http://jinrongdao.com:8081/adverse/payment"

def service(request):
    Logger.infoLogger.info("begin record click adverse...")
    result={}
    ip=request.remote_addr
    Logger.infoLogger.info("get ip succ...")
    id=request.form.get('id',0)
    Logger.infoLogger.info("get id succ...")
    query=request.form.get('query','')
    action='click'
    cur_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if id==0 or query == '':
        Logger.infoLogger.info(" id or query exception ..."+str(id)+query)
        result['code']=1
        result['message']='param error. ip or id not correct'
        return json.dumps(result)
    param={}
    param['adverseContractId']=id
    param['ip']=str(ip)
    param['createTime']=cur_time
    param['triggerQuery']=query
    param['action']=action
    c=pycurl.Curl()
    buf=cStringIO.StringIO()
    c.setopt(c.URL,get_adverse_service_click_base_url())
    c.setopt(pycurl.HTTPHEADER,['Content-Type: application/json'])
    c.setopt(c.POSTFIELDS,json.dumps(param))
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    return_value = buf.getvalue()
    buf.close()
    result_dict = json.loads(return_value) 
    if result_dict['code']==0:
        Logger.infoLogger.info("post to "+get_adverse_service_click_base_url()+" succ! and data is: "+json.dumps(param))
        result['code']=0
        result['message']='succ'
    else:    
        result['code']=1
        result['message']='param error. ip or id not correct'
        Logger.infoLogger.info("post to "+get_adverse_service_click_base_url()+\
            " failed! and data is: "+json.dumps(param)+" error reason is: "+json.dumps(result_dict))
    return json.dumps(result)
    

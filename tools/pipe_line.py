#/usr/bin/python
import json
import os 

import time_format 
import mysql_data_process
from text_classify import class_and_fill_level
#pipe line for:
#1.copy mysql data during some time from crawler to finance_no2
#2.classify and rank these data
#3.fill other values to these data such as pagerank
#4.index those data to elastic search
def pipe_line(time_file_list,db_list,table_list,url_index_list):
  id_begin=0
  id_end=0
  for i in range(len(time_file_list)):
    #read time file,get begin time
    print 'now update time file ',time_file_list[i],' db ',db_list[i],' table ',table_list[i]
    time_file=time_file_list[i]
    fp_time=open(time_file)
    lines=fp_time.readlines()
    print time_format.cur_time(),'last update time:',lines[0]
    time_info=json.loads(lines[0])
    time_begin=time_info.get('time_begin')
    if time_begin==None:
      print time_format.cur_time(),'begin time error, quit! -----------------',time_begin
      fp_time.close()
      return
    fp_time.close()

    #copy mysql data
    print time_format.cur_time(),'begin copy mysql data-----------------',time_begin
    time_update,id_begin_cur,id_end_cur=mysql_data_process.do_mysql_data_copy(time_begin,db_list[i],table_list[i],url_index_list[i])
    if i == 0:
      id_begin=id_begin_cur
      id_end=id_end_cur
    if id_begin_cur < id_begin:
      id_begin=id_begin_cur
    if id_end_cur > id_end:
      id_end=id_end_cur
    if time_update != None:
      time_info['time_begin']=time_update
      fp_time=open(time_file,'w')
      fp_time.write(json.dumps(time_info))
      fp_time.close()
    else:
      print time_format.cur_time(),'time_update is none!'
    print time_format.cur_time(),'end copy mysql data-----------------',time_begin,time_update,id_begin,id_end

  #classify and fill tags,level,final_levl info 
  print time_format.cur_time(),'begin class and fill tags,level,final level info-----------------',id_begin,id_end,time_begin,time_update
  if id_begin != 0 and id_end != 0:
    class_and_fill_level.class_and_fill_level(id_begin,id_end)
  else:
    print time_format.cur_time(),'mysql data copy fail,ignore class and fill is none!'
  print time_format.cur_time(),'end class and fill tags,level,final level info-----------------',id_begin,id_end,time_begin,time_update

  #fill other info
  mysql_data_process.fill_insert_date_column(id_begin,id_end)
  print time_format.cur_time(),'end  fill insertdate column-----------------',id_begin,id_end,time_begin,time_update

  #index these data
  print time_format.cur_time(),'begin index data-----------------',id_begin,id_end
  if id_begin != 0 and id_end != 0:
    cmd_copy=' cp ./mysql_article_index.sh /data/yx/svr/finance_one/tools/elasticsearch-jdbc-2.3.4-2.0/bin/'
    os.system(cmd_copy)
    print time_format.cur_time(),cmd_copy

    cmd_index='cd /data/yx/svr/finance_one/tools/elasticsearch-jdbc-2.3.4-2.0/bin/ && ./mysql_article_index.sh '+ str(id_begin)+ ' ' + str(id_end)
    #cmd_index='cd /Users/fuhonglei/Work/elastic_search_jdbc/elasticsearch-jdbc-2.3.4.0/bin/ && ./mysql_article_index.sh '+ str(id_begin)+ ' ' + str(id_end)
    os.system(cmd_index)
    print time_format.cur_time(),cmd_index

  else:
    print time_format.cur_time(),'mysql data copy fail,ignore data index!'
  print time_format.cur_time(),'end index data-----------------',id_begin,id_end

  print time_format.cur_time(),"all pipe finish!",time_begin,time_update,id_begin,id_end

if __name__=='__main__':
  time_file_list=['/data/yx/svr/finance_one/search_web_server/data/crawler_time','/data/yx/svr/finance_one/search_web_server/data/crawler_finance_time']
  db_list=['crawler','crawler_finance']
  table_list=['laws_article','finance_news_article']
  url_index_list=[15,18]
  #'/data/yx/svr/finance_one/search_web_server/data/time'
  pipe_line(time_file_list,db_list,table_list,url_index_list)

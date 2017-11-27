#/usr/bin/python
import json
import os 

import mysql_data_copy
import mysql_data_index

#pipe line for:
#1.copy mysql data during some time from crawler to finance_no2
#2.classify and rank these data
#3.fill other values to these data such as pagerank
#4.index those data to elastic search
def pipe_line(time_file):
  #read time file,get begin time and endtime
  fp_time=open(time_file)
  lines=fp_time.readlines()
  print lines[0]
  time_info=json.loads(lines[0])
  time_begin=time_info.get('time_begin')
  print 'now begin copy mysql data-----------------',time_begin
  if time_begin==None:
    time_begin='1700-01-01 00:00:00'
  fp_time.close()

  #copy mysql data
  time_update,id_begin,id_end=mysql_data_copy.do_mysql_data_copy(time_begin)
  if time_update != None:
    time_info['time_begin']=time_update
    fp_time=open(time_file,'w')
    fp_time.write(json.dumps(time_info))
    fp_time.close()
  else:
    print 'time_update is none!'

  #classify and sort
  print 'now begin class and fill level-----------------',id_begin,id_end,time_begin,time_update
  if id_begin != 0 and id_end != 0:
    #cmd='cd /data/yx/svr/finance_one/tools/machine_learning/program/ && /bin/bash run.sh '+time_begin+' '+time_update+' ' +' > log.txt'
    cmd='cd /data/yx/svr/finance_one/tools/machine_learning/program/ && /bin/bash run.sh '+str(id_begin)+' ' + str(id_end) +'  > log.txt'
    print ' classify cmd is :',cmd
    os.system(cmd)
  else:
    print 'time_update is none!'

  #fill other info

  #index these data
  print 'now begin index data-----------------',id_begin
  #if time_update != None:
  if id_begin != 0 and id_end != 0:
    cmd_copy=' cp ./mysql_article_index.sh /data/yx/svr/finance_one/tools/elasticsearch-jdbc-2.3.4-2.0/bin/'
    os.system(cmd_copy)

    cmd='/data/yx/svr/finance_one/tools/elasticsearch-jdbc-2.3.4-2.0/bin/mysql_article_index.sh '+ str(id_begin) + ' ' + str(id_end)
    os.system(cmd)
  else:
    print 'no new data update!'
  #os.system(cmd)
  print "all pipe succ!",time_begin,time_update,id_begin,id_end

if __name__=='__main__':
  pipe_line('/data/yx/svr/finance_one/search_web_server/tools/time')

#!/usr/bin/python
#encoding=utf8
import MySQLdb
import datetime
import types
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os

def connect(host="127.0.0.1",port=3306,user="root",passwd="123",db="finance_one"):
  conn= MySQLdb.connect(host=host,port = port,user= user,passwd= passwd,db = db,charset="utf8")
  return conn

def classify_day_by_day(begin_date, days,table_name,id_column_name,time_column_name):
  cnn=connect(host="127.0.0.1",port=3306,user="root",passwd="123",db="finance_one")
  for i in range(days):
    from_delta=datetime.timedelta(days=i)
    to_delta=datetime.timedelta(days=i+1)
    from_date=begin_date+from_delta
    to_date=begin_date+to_delta
    id_begin,id_end=get_id_between_date(cnn,from_date,to_date,table_name,id_column_name,time_column_name)
    print from_date,id_begin,to_date,id_end
    if id_begin == 0 or id_end == 0:
      print ' error id_begin or id_end'
      continue
    cmd='cd /data/yx/svr/finance_one/tools/machine_learning/program/ && /bin/bash run.sh '+str(id_begin)+' ' + str(id_end) +'  > log.txt'
    print ' classify cmd is :',cmd
    os.system(cmd)
  cnn.close()

def get_id_between_date(cnn,from_date,to_date,table_name,id_column_name,time_column_name):
  id_begin=0
  id_end=0
  str_from_date=from_date.strftime('%Y-%m-%d %H:%M:%S')
  str_to_date=to_date.strftime('%Y-%m-%d %H:%M:%S')
  sql_id_begin=' select id from '+table_name+' where '+time_column_name+' >= "'+str_from_date+ '" order by '+time_column_name +' asc limit 1'
  sql_id_end=' select id from '+table_name+' where '+time_column_name+' <= "'+str_to_date+ '" order by '+time_column_name +' desc limit 1'
  try:
    cur=cnn.cursor()
    cur.execute(sql_id_begin)
    results=cur.fetchall()
    if results != None and len(results) > 0:
      id_begin=results[0][0]
    cur.execute(sql_id_end)
    results=cur.fetchall()
    if results != None and len(results) > 0:
      id_end=results[0][0]
    cur.close()
  except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    cur.close()
  return id_begin,id_end

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print "param error, please input python mysql_data_classify_day_by_day.py 2017-08-01 15"
  else:
    str_begin_date=sys.argv[1]
    str_begin_date=str_begin_date+' 00:00:00'
    begin_date=datetime.datetime.strptime(str_begin_date, '%Y-%m-%d %H:%M:%S')
    days=sys.argv[2]
    classify_day_by_day(begin_date,int(days),'article','id','insert_time')

#!/usr/bin/python
#coding=utf8
import MySQLdb

#导出法规训练数据、股票训练数据到文件中
#output_file format:
# 法规速递\t内容
# 行业动态\t内容
# 股票\t内容
# 注意，为保证训练数据的准确，行业动态level>4000 法规速递level > 5000
# 为日后验证，导出的所有数据insert_time < 2017-10-20 00:00:00
#def dump_train_data_to_file(output_file,host,port,user,password,db,table_name,charset='utf8',\
#    min_level=7000,max_level=100000,begin_time='2015-10-20 00:00:00',end_time='2017-10-20 00:00:00'):
#    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
#    cur=conn.cursor()
#    
#    fp=open(output_file,'w')   
#    #dump fagui
#    sql_fagui='select tags,content from '+table_name+' where tags="法规速递" \
#        and level >' +str(min_level)+' and level <' +str(max_level) +' and insert_time < "'+end_time+'"'\
#        +' and insert_time > "'+begin_time+'"'
#    cur.execute(sql_fagui)
#    results=cur.fetchall()
#    print "法规速递样本数:",len(results)
#    for result in results:
#        if result[0] == None or result[1]==None:
#            continue
#        fp.write((result[0]+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
#
#    #dump hangye 
#    sql_hangye='select tags,content from '+table_name+' where tags="行业动态" \
#        and level >' +str(min_level)+' and level <' +str(max_level) +' and insert_time < "'+end_time+'"'\
#        +' and insert_time > "'+begin_time+'" limit 6000'
#    cur.execute(sql_hangye)
#    results=cur.fetchall()
#    print "行业动态样本数:",len(results)
#    for result in results:
#        if result[0] == None or result[1]==None:
#            continue
#        fp.write((result[0]+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
#
#    #dump stock data
#    sql_stock='select content from '+table_name+\
#    ' where (url like "%http://finance.sina.com.cn/stock/%" or url like "%http://stock.hexun.com/%") \
#        and insert_time < "'+end_time+'"'\
#        +' and insert_time > "'+begin_time+'" limit 5000'
#    cur.execute(sql_stock)
#    results=cur.fetchall()
#    print "股票样本数:",len(results)
#    for result in results:
#        fp.write(('股票'.decode('utf8')+'\t'+result[0].replace('\n','')+'\n').encode('utf8'))
#    fp.close()
#
#    cur.close()
#    conn.close()

#导出法规测试数据、股票测试数据到文件中
#output_file format:
# 法规速递\t内容
# 行业动态\t内容
# 股票\t内容
# 注意，为保证训练数据的准确，行业动态level>4000 法规速递level > 5000
# 为日后验证，导出的所有数据insert_time < 2017-10-20 00:00:00
#def dump_test_data_to_file(output_file,host,port,user,password,db,table_name,charset='utf8',\
#    min_level=7000,max_level=100000,begin_time='2015-10-20 00:00:00',end_time='2017-10-20 00:00:00'):
#    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
#    cur=conn.cursor()
#    
#    fp=open(output_file,'w')   
#    #dump fagui
#    sql_fagui='select tags,content from '+table_name+' where tags="法规速递" \
#        and level >' +str(min_level)+' and level <' +str(max_level) +' and insert_time < "'+end_time+'"'\
#        +' and insert_time > "'+begin_time+'"'
#    cur.execute(sql_fagui)
#    results=cur.fetchall()
#    print "法规速递样本数:",len(results)
#    for result in results:
#        if result[0] == None or result[1]==None:
#            continue
#        fp.write((result[0]+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
#
#    #dump hangye 
#    sql_hangye='select tags,content from '+table_name+' where tags="行业动态" \
#        and level >' +str(min_level)+' and level <' +str(max_level) +' and insert_time < "'+end_time+'"'\
#        +' and insert_time > "'+begin_time+'" limit 6000'
#    cur.execute(sql_hangye)
#    results=cur.fetchall()
#    print "行业动态样本数:",len(results)
#    for result in results:
#        if result[0] == None or result[1]==None:
#            continue
#        fp.write((result[0]+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
#
#    #dump stock data
#    sql_stock='select content from '+table_name+\
#    ' where (url like "%http://finance.sina.com.cn/stock/%" or url like "%http://stock.hexun.com/%") \
#        and insert_time < "'+end_time+'"'\
#        +' and insert_time > "'+begin_time+'" limit 5000'
#    cur.execute(sql_stock)
#    results=cur.fetchall()
#    print "股票样本数:",len(results)
#    for result in results:
#        fp.write(('股票'.decode('utf8')+'\t'+result[0].replace('\n','')+'\n').encode('utf8'))
#    fp.close()
#
#    cur.close()
#    conn.close()


#导出某一id范围内的法规训练数据、行业动态训练数据、股票训练数据到文件中
#output_file format:
# 法规速递\t内容
# 行业动态\t内容
# 股票\t内容
#def dump_train_data_during_id_to_file(output_file,host,port,user,password,db,table_name,id_begin,id_end,charset='utf8'):
#    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
#    cur=conn.cursor()
#    
#    fp=open(output_file,'w')   
#    #dump fagui and hangye data
#    sql='select tags,content from '+table_name+' where (id >='+str(id_begin)+\
#        ' and id <='+str(id_end)+') and (tags="法规速递" or tags="行业动态")'
#    cur.execute(sql)
#    results=cur.fetchall()
#    for result in results:
#        fp.write((result[0]+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
#    #dump stock data
#    sql_stock='select content from '+table_name+' where (id >='+str(id_begin)+\
#        ' and id <='+str(id_end)+') and (url like "%http://finance.sina.com.cn/stock/%" or url like "%http://stock.hexun.com/%")'
#    cur.execute(sql_stock)
#    results=cur.fetchall()
#    for result in results:
#        if result[0] == None:
#            continue
#        fp.write(('股票'.decode('utf8')+'\t'+result[0].replace('\n','')+'\n').encode('utf8'))
#    fp.close()
#
#    cur.close()
#    conn.close()

#导出股票、房产、行业动态训练数据到文件中
#output_file format:
# 股票\t内容
# 房产\t内容
#def dump_train_data_to_file(host,port,user,password,db,table_name,charset,id_begin,id_end,output_dir):
#   dump_house_data_during_id_to_file(host,port,user,password,db,table_name,\
#       charset,id_begin,id_end,output_dir+'/train_data_house') 
#   dump_stock_data_during_id_to_file(host,port,user,password,db,table_name,\
#       charset,id_begin,id_end,output_dir+'/train_data_stock') 
#   dump_hangye_data_during_id_to_file(host,port,user,password,db,table_name,\
#       charset,id_begin,id_end,output_dir+'/train_data_hangye') 
  # try:
  #     print 'output train data to ',output_dir+'/mysql_train_data'
  #     fp_all=open(output_dir+'/mysql_train_data','w')
  #     fp_house=open(output_dir+'/train_data_house','r')
  #     fp_all.write(fp_house.read())
  #     fp_stock=open(output_dir+'/train_data_stock','r')
  #     fp_all.write(fp_stock.read())
  #     fp_hangye=open(output_dir+'/train_data_hangye','r')
  #     fp_all.write(fp_hangye.read())
  # finally:
  #     fp_all.close()
  #     fp_house.close()
  #     fp_stock.close()
  #     fp_hangye.close()


def merge_file(file_list,output_file):
    print 'merge data to ',output_file
    try:
        fp_all=open(output_file,'w')
        for name in file_list:
            print 'now merge file ',name
            fp_cur=open(name,'r')
            fp_all.write(fp_cur.read())
            fp_cur.close()
    finally:
        fp_all.close()

#导出股票、房产、行业动态测试数据到文件中
#output_file format:
# 股票\t内容
# 房产\t内容
#def dump_test_data_to_file(host,port,user,password,db,table_name,charset,id_begin,id_end,output_dir):
#   dump_house_data_during_id_to_file(host,port,user,password,db,table_name,\
#       charset,id_begin,id_end,output_dir+'/test_data_house') 
#   dump_stock_data_during_id_to_file(host,port,user,password,db,table_name,\
#       charset,id_begin,id_end,output_dir+'/test_data_stock') 
#   dump_hangye_data_during_id_to_file(host,port,user,password,db,table_name,\
#       charset,id_begin,id_end,output_dir+'/test_data_hangye') 
#   try:
#       print 'output test data to ',output_dir+'/mysql_test_data'
#       fp_all=open(output_dir+'/mysql_test_data','w')
#       fp_house=open(output_dir+'/test_data_house','r')
#       fp_all.write(fp_house.read())
#       fp_stock=open(output_dir+'/test_data_stock','r')
#       fp_all.write(fp_stock.read())
#       fp_hangye=open(output_dir+'/test_data_hangye','r')
#       fp_all.write(fp_hangye.read())
#   finally:
#       fp_all.close()
#       fp_house.close()
#       fp_stock.close()
#       fp_hangye.close()

#导出某一id范围内的数据到文件中
#output_file format:
# id\t内容
# id\t内容
# id\t内容
def dump_to_be_classify_data_during_id_to_file(host,port,user,password,db,table_name,id_begin,id_end,charset,output_file):
    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
    cur=conn.cursor()
    
    fp=open(output_file,'w')   
    sql='select id,content from '+table_name+' where (id >='+str(id_begin)+\
        ' and id <='+str(id_end)+') '
    cur.execute(sql)
    results=cur.fetchall()
    for result in results:
        fp.write((str(result[0])+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
    fp.close()

    cur.close()
    conn.close()

#导出某一id范围内的训练数据到文件中
#output_file format:
# tag\t内容
# tag\t内容
# tag\t内容
def dump_house_data_during_id_to_file(host,port,user,password,db,table_name,charset,id_begin,id_end,output_file):
    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
    cur=conn.cursor()
    
    fp=open(output_file,'w')   
    sql='select tags,content from '+table_name+' where (id >='+str(id_begin)+\
        ' and id <='+str(id_end)+') and (url like "%house%") and (url not like "%xinhuanet%") and (url not like "%jrj.com%")'
    print sql
    cur.execute(sql)
    results=cur.fetchall()
    for result in results:
        fp.write(('房产'.decode('utf8')+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
    fp.close()

    cur.close()
    conn.close()

#导出某一id范围内的股票数据到文件中
#output_file format:
# tag\t内容
# tag\t内容
# tag\t内容
def dump_stock_data_during_id_to_file(host,port,user,password,db,table_name,charset,id_begin,id_end,output_file):
    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
    cur=conn.cursor()
    
    fp=open(output_file,'w')   
    sql='select tags,content from '+table_name+' where (id >='+str(id_begin)+\
        ' and id <='+str(id_end)+') and (url like "%stock.hexun.com%") '
    print sql
    cur.execute(sql)
    results=cur.fetchall()
    for result in results:
        fp.write(('股票'.decode('utf8')+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
    fp.close()

    cur.close()
    conn.close()

#导出某一id范围内的行业动态数据到文件中
#output_file format:
# tag\t内容
# tag\t内容
# tag\t内容
def dump_hangye_data_during_id_to_file(host,port,user,password,db,table_name,charset,id_begin,id_end,output_file):
    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
    cur=conn.cursor()
    
    fp=open(output_file,'w')   
    #and (url like "%tech%" or url like "%p2p%" or url like "%futures%" or url like "%iof%" or url like "%insurance%" or url like "%money%") )'
    sql='select tags,content from '+table_name+' where (id >='+str(id_begin)+\
        ' and id <='+str(id_end)+') and (url like "%hexun%" \
        and (url like "%tech%" or url like "%p2p%" or url like "%futures%" or url like "%iof%" or url like "%insurance%" or url like "%money%") )'
    print sql
    cur.execute(sql)
    results=cur.fetchall()
    for result in results:
        fp.write(('行业动态'.decode('utf8')+'\t'+result[1].replace('\n','')+'\n').encode('utf8'))
    fp.close()

    cur.close()
    conn.close()


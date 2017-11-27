#!/usr/bin/python
# encoding=utf8
import MySQLdb
import datetime
import types

import sys
import read_ranker_data

reload(sys)
sys.setdefaultencoding("utf-8")
import os
import urllib

import time_format

alexa_index = 26
pr_index = 25
#url_index = 15
#level_index = 8

#get database connect
def connect(host="127.0.0.1", port=3306, user="root", passwd="123", db="crawler_copy"):
    conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset="utf8")
    return conn


# copy data from source table to target table,whole copy
def data_copy(conn_source, conn_target, db_source, table_name_source, db_target, table_name_target, pid_file,
              time_begin, update_time_str, update_time_index,url_index):
    # if last copy not finish, exist
    pid_file=pid_file.strip()
    if os.path.exists(pid_file):
        print time_format.cur_time(),"last copy have not finish!exist\n"
        return None,0,0

    end_time = "0"
    id_begin=0
    id_end=0
    sql_insert_when_error = ""

    try:
        # record is running
        fp = open(pid_file, 'w')
        fp.write("runing")
        fp.close()

        print time_format.cur_time(),'begin read rank data from dict'
        pr_dict, alexa_dict = read_ranker_data.read()  # add by lxx 2017-08-23
        print time_format.cur_time(),'end read rank data from dict'

        # get db connection of source and target
        cur_source = conn_source.cursor()
        cur_target = conn_target.cursor()
        
        #get id_begin
        sql_max_id= 'select max(id) from ' + table_name_target
        cur_target.execute(sql_max_id)
        results_max_id=cur_target.fetchall()
        if len(results_max_id)>0:
            id_begin=results_max_id[0][0]+1 
            id_end=id_begin

        # copy data from source to target
        sql_column_name = "SELECT column_name FROM information_schema.columns WHERE table_schema='" + db_source + "' AND table_name='" + table_name_source + "'"
        cur_source.execute(sql_column_name)
        results = cur_source.fetchall()
        column_names = column_result_to_str(results)
        print time_format.cur_time(),'column names str is ----------------------',column_names

        sql_select = 'select * from ' + table_name_source + ' where ' + update_time_str + ' > ' + "'" + time_begin + "'"
        print time_format.cur_time(),'source select is ----------------------',sql_select
        cur_source.execute(sql_select)
        results = cur_source.fetchall()
        print time_format.cur_time(),'select result count:', len(results)
        for item in results:
            # update time id_begin and id_end
            if str(item[update_time_index]) > end_time:
                end_time = str(item[update_time_index])
            ult_to_strql_insert = "insert into " + table_name_target + "(" + column_names + ")" + " values(" + tuple_to_str(item,
                                                                                                                   pr_dict,
                                                                                                                   alexa_dict,url_index) + ")"
            sql_insert_when_error = ult_to_strql_insert
            cur_target.execute(ult_to_strql_insert)
            conn_target.commit()
            id_end += 1

        #get id_end
        sql_max_id= 'select max(id) from ' + table_name_target
        cur_target.execute(sql_max_id)
        results_max_id=cur_target.fetchall()
        if len(results_max_id)>0:
            id_end=results_max_id[0][0] 

        # close db connection
        cur_source.close()
        cur_target.close()

        # delete runing file
        print time_format.cur_time(),'rm pid running file',pid_file
        os.remove(pid_file)

    except MySQLdb.Error, e:
        print time_format.cur_time(),"Mysql Error %d: %s" % (e.args[0], e.args[1])
       # print time_format.cur_time(),"when error, sql_insert is :", sql_insert_when_error
        # delete runing file
        os.remove(pid_file)
    print time_format.cur_time(),"begin_time,end_time,begin_id,end_id :",time_begin, end_time,id_begin,id_end
    return end_time,id_begin,id_end


# select result to str like '1,"2017-08-21 17:50:50","law news"......'
def tuple_to_str(result, pr_dict, alexa_dict,url_index):
    str_list = []
    item_info = ""
    #for item in result:
    for i in range(len(result)):
        if i==0:
            continue
        item=result[i]
        if isinstance(item, unicode):
            item_info = MySQLdb.escape_string(item)
            item_info = "'" + item_info + "'"
        elif isinstance(item, datetime.datetime):
            item_info = "'" + str(item) + "'"
        elif isinstance(item, types.NoneType):
            item_info = "null"
        else:
            item_info = str(item)
        str_list.append(item_info)
    str_list = add_rank(result, str_list, pr_dict, alexa_dict,url_index)
    return ','.join(str_list)

# add rank column name for insert sql
def add_rank_column_name(str_list):
    str_list.append('pr')
    str_list.append('alexa')
    str_list.append('all_rank')
    return str_list

# add page rank value for data to be inserted to database 
def add_rank(item, str_list, pr_dict, alexa_dict,url_index):
    proto, rest = urllib.splittype(item[url_index])
    res, rest = urllib.splithost(rest)
    if res in pr_dict:
        str_list.append(str(pr_dict[res]))
        str_list.append(str(alexa_dict[res]))
        str_list.append(str(pr_dict[res]*100))
       # if item[level_index]:
       #     print level_index,res,pr_dict[res],item[level_index]
       #     all_rank = item[level_index]+1000-pr_dict[res]*100
       #     str_list.append(str(int(all_rank)))
       # else:
       #     str_list.append(str(1000-pr_dict[res]*100))
    else:
        str_list.append('0')
        str_list.append('0')
        str_list.append('0')
       # if item[level_index]:
       #     str_list.append(str(item[level_index]))
       # else:
       #     str_list.append('0')
    return str_list


# column name to str like 'id,update_time,title....'
def column_result_to_str(column_result):
    str_list = []
    for i in range(len(column_result)):
        if i==0:
            continue
        item=column_result[i]
        str_list.append(str(item[0]))
    str_list=add_rank_column_name(str_list)
    return ','.join(str_list)

def valid(time_begin):
    result = True
    try:
        now = datetime.datetime.now()
        two_days_ago=now + datetime.timedelta(days=-3)
        time_to_valid=datetime.datetime.strptime(time_begin,'%Y-%m-%d %H:%M:%S')
        if time_to_valid < two_days_ago:
           result=False
           print time_format.cur_time(),'time_begin is invalid:',time_begin
    except Exception,e: 
        result=False
        print time_format.cur_time(),'time_begin is invalid:',time_begin
    return result

def correct_time_begin(conn_target):
    cur=conn_target.cursor()
    sql='select max(insert_time) from article'
    cur.execute(sql)
    results=cur.fetchall()
    new_time_begin=datetime.datetime.strftime(results[0][0],'%Y-%m-%d %H:%M:%S')
    cur.close()
    print time_format.cur_time(),'correct time begin is :',new_time_begin
    return new_time_begin

def do_mysql_data_copy(time_begin,db_source,table_source,url_index):
    conn_source = connect(host="127.0.0.1", port=3306, user="root", passwd="123", db=db_source)
    conn_target = connect(host="127.0.0.1", port=3306, user="root", passwd="123", db="finance_one")
    #if time_begin is invalid, set it's value to max insert_time in conn_target
    correct_time=time_begin
    if valid(time_begin) == False:
        correct_time=correct_time_begin(conn_target)
    update_time,id_begin,id_end=data_copy(conn_source, conn_target, db_source, table_source, 'finance_one', 'article', './pid_file',\
              correct_time, 'insert_time', 1,url_index)
    conn_source.close()
    conn_target.close()
    return update_time,id_begin,id_end

def fill_insert_date_column(id_begin,id_end,db_name='finance_one',table_name='article'):
    conn = connect(host="127.0.0.1", port=3306, user="root", passwd="123", db=db_name)
    cur=conn.cursor()
    sql_select='select id,insert_time from '+table_name+' where id>='+str(id_begin)+' and id<='+str(id_end) 
    try:
        cur.execute(sql_select)
        results=cur.fetchall()
        for result in results:
            insert_time=datetime.datetime.strftime(result[1],'%Y-%m-%d %H:%M:%S')
            insert_date=int(insert_time[0:10].replace('-',''))
            sql_insert='update '+table_name+' set insert_date='+str(insert_date)+' where id='+str(result[0])
            cur.execute(sql_insert)
        conn.commit() 
    except MySQLdb.Error, e:
        print time_format.cur_time(),"Mysql Error %d: %s" % (e.args[0], e.args[1])
    cur.close()
    conn.close()

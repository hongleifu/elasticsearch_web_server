#!/usr/bin/python
#coding=utf8
import MySQLdb
def update_result_to_mysql(predict_result_file,id_file,tag_dict,host,port,user,password,db,table_name,charset='utf8'):
    tagnum_to_value_index={'2':1,'3':2,'4':3}
    fp_predict=open(predict_result_file,'r')     
    lines=fp_predict.readlines()
    lines_predict=lines[1:]
     
    fp_id=open(id_file,'r')
    lines_id=fp_id.readlines()
    
    conn=MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset=charset)
    cur=conn.cursor()
    if len(lines_predict) != len(lines_id):
        print 'error data, predict is not equal to id'
    else:
        for i in range(len(lines_id)):
            predict_split=lines_predict[i].split(' ')
            data_id=int(lines_id[i])
            level=int(float(predict_split[tagnum_to_value_index[predict_split[0]]])*10000)
            #print predict_split[0],tagnum_to_value_index[predict_split[0]],predict_split[tagnum_to_value_index[predict_split[0]]],level
            tags=tag_dict[predict_split[0]]
            final_level=level+(get_all_rank_from_id(data_id,table_name,cur))
            sql=' update '+table_name+' set level='+str(level)+',tags="'+tags+'"'+ ',\
                final_level='+str(final_level)+' where id='+str(data_id)
            cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    fp_id.close()
    fp_predict.close()     


def get_all_rank_from_id(data_id,table_name,cur):
    all_rank=0
    sql='select all_rank from '+table_name+' where id='+str(data_id)
    cur.execute(sql)
    results=cur.fetchall()
    if len(results)>0:
        all_rank=int(results[0][0])
    return all_rank

#get train data of house. rm 股票内容
def get_train_data_house(predict_result,ori_data,output_file):
    fp_predict=open(predict_result,'r')
    fp_ori=open(ori_data,'r')
    lines_predict=fp_predict.readlines()
    lines_ori=fp_ori.readlines()
    if len(lines_predict) != len(lines_ori)+1:
        print 'error data! lines_predict != lines_ori+1'
    else:
        fp=open(output_file,'w')
        for i in range(len(lines_ori)):
            split=lines_predict[i+1].split(' ')
            if len(split)>0 and (split[0]=='3' or split[0]=='2'):
                print i,' stock content'
                continue
            fp.write(lines_ori[i])
        fp.close()
    fp_ori.close()
    fp_predict.close()

#!/usr/bin/python
#coding=utf8
import dump_mysql_data
import format_data
import output_word_dict 
import word_segment 
def get_train_data():
    print 'now dump train data to file ./data/mysql_train_data'
    dump_mysql_data.dump_hangye_data_during_id_to_file('127.0.0.1',3306,'root','123','finance_one','article','utf8',1,20700000,'./data/train_data_hangye')
    dump_mysql_data.dump_stock_data_during_id_to_file('127.0.0.1',3306,'root','123','finance_one','article','utf8',19500000,20800000,'./data/train_data_stock')
    dump_mysql_data.dump_house_data_during_id_to_file('127.0.0.1',3306,'root','123','crawler_finance','finance_news_article','utf8',1,134000,'./data/train_data_house')
    dump_mysql_data.merge_file(['./data/train_data_hangye','./data/train_data_stock','./data/train_data_house'],'./data/mysql_train_data')

    #dump_mysql_data.dump_hangye_data_during_id_to_file('127.0.0.1',3306,'root','root','finance_one','article','utf8',18000000,20800000,'./data/train_data_hangye')
    #dump_mysql_data.dump_stock_data_during_id_to_file('127.0.0.1',3306,'root','root','finance_one','article','utf8',20000000,20800000,'./data/train_data_stock')
    #dump_mysql_data.dump_house_data_during_id_to_file('127.0.0.1',3306,'root','root','crawler_finance','finance_news_article','utf8',1,130000,'./data/train_data_house')
    #dump_mysql_data.merge_file(['./data/train_data_hangye','./data/train_data_stock','./data/train_data_house'],'./data/mysql_train_data')
    #dump_mysql_data.merge_file(['./data/train_data_stock','./data/train_data_house'],'./data/mysql_train_data')

    print 'now seg word and rm stop_word  to file ./data/seg_data'
    word_segment.data_segment_word_and_rm_stop_word('./data/'+'mysql_train_data',\
        './data/seg_data','./model/stop_word','./data/all_tag','./data/all_word')
    print 'now output word_dict by kafang to:./model/word_dict'
    output_word_dict.ouput_word_dict('./data/seg_data','./model/word_dict','./data/tag_top_n_word',top_n=1500)
    tag_order={}
    tag_order['法规速递'.decode('utf8')]='1'
    tag_order['行业动态'.decode('utf8')]='2'
    tag_order['股票'.decode('utf8')]='3'
    tag_order['房产'.decode('utf8')]='4'
    print 'now format data TF guiyi to:./data/train_data'
    max_word_count=format_data.format_train_data('./data/seg_data','./model/word_dict',\
       tag_order,'./data/train_data','./model/average','./model/std')
    print 'max_word_conut :',max_word_count

if __name__=='__main__':
    get_train_data()

#!/usr/bin/python
#coding=utf8
import dump_mysql_data
import format_data
import output_word_dict 
import word_segment 
def get_test_data():
    print 'now dump test data to file ./data/mysql_data_test'
    #dump_mysql_data.dump_test_data_to_file('./data/mysql_data_test','127.0.0.1',3306,'root','root','finance_one','article',charset='utf8',\
    #    min_level=7000,max_level=100000,begin_time='2017-10-20 00:00:00',end_time='2018-10-20 00:00:00')
    dump_mysql_data.dump_hangye_data_during_id_to_file('127.0.0.1',3306,'root','123','finance_one','article','utf8',20700000,30850000,'./data/test_data_hangye')
    dump_mysql_data.dump_stock_data_during_id_to_file('127.0.0.1',3306,'root','123','finance_one','article','utf8',1,18700000,'./data/test_data_stock')
    dump_mysql_data.dump_house_data_during_id_to_file('127.0.0.1',3306,'root','123','crawler_finance','finance_news_article','utf8',134000,20840000,'./data/test_data_house')
    dump_mysql_data.merge_file(['./data/test_data_hangye','./data/test_data_stock','./data/test_data_house'],'./data/mysql_test_data')
    word_segment.data_segment_word_and_rm_stop_word('./data/mysql_test_data','./data/seg_data_test','./data/stop_word','/tmp/all_tag_test','/tmp/all_word_test')
    tag_order={}
    tag_order['法规速递'.decode('utf8')]='1'
    tag_order['行业动态'.decode('utf8')]='2'
    tag_order['股票'.decode('utf8')]='3'
    tag_order['房产'.decode('utf8')]='4'
    format_data.format_test_data('./data/seg_data_test','./data/word_dict',\
        './data/average','./data/std',tag_order,'./data/test_data')

if __name__=='__main__':
    get_test_data()

#!/usr/bin/python
#coding=utf8
#pipe line of dump new data,classify them and fill result to mysql
import os
import sys 
import dump_mysql_data
import word_segment 
import format_data 
import process_predict_result 
 
def class_and_fill_level(id_begin,id_end,host='127.0.0.1',port=3306,user='root',\
    password='123',db='finance_one',table_name='article',base_path='./text_classify/'):
    # dump mysql data to be classified
    class_data_file=base_path+'data/to_class_data'
    stop_words_file=base_path+'model/stop_word'
    class_data_segment_word_file=base_path+'data/to_class_data_segment'
    word_dict_file=base_path+'model/word_dict'
    average_file=base_path+'model/average'
    std_deviation_file=base_path+'model/std'
    output_to_be_classify_file=base_path+'data/to_class_data_format'
    output_id_file=base_path+'data/id'
    svm_path=base_path+'../../../tools/libsvm-3.22/'
    model_file_path=base_path+'model/train_data.model'
    predict_result_file=base_path+'data/predict_result'

   # print 'dump data to be class....',id_begin,id_end,' to file ',class_data_file
    dump_mysql_data.dump_to_be_classify_data_during_id_to_file(\
        host,port,user,password,db,table_name,id_begin,id_end,\
        charset='utf8',output_file=class_data_file)
    # word segment the data
    print ' word segment to file :',class_data_segment_word_file
    word_segment.data_segment_word_and_rm_stop_word_only(class_data_file,\
        stop_words_file,class_data_segment_word_file)
    # format the data
    print ' format the data to file :',output_to_be_classify_file
    format_data.format_to_classify_data(class_data_segment_word_file,\
        word_dict_file,average_file,std_deviation_file,\
        output_to_be_classify_file,output_id_file)
    # classify the data
    cmd=svm_path+'/svm-predict -b 1 '+output_to_be_classify_file+' '+model_file_path+' '+predict_result_file
    print cmd
    os.system(cmd)
    # fill result to mysql
    tag_dict={'1':'法规速递','2':'行业动态','3':'股票','4':'房产'}
    print ' update predict result'
    process_predict_result.update_result_to_mysql(predict_result_file,\
        output_id_file,tag_dict,host,port,user,password,db,table_name,charset='utf8')

if __name__=='__main__':
    class_and_fill_level(int(sys.argv[1]),int(sys.argv[2]))

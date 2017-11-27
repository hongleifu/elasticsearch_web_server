#!/usr/bin/python
#coding=utf8

from numpy import *

#guiyi feature value.
def regular_feature_value(value):
    result=value
   # if result>15:
   #     result=15
   # if result<0.1:
   #     result=0.1
    return result

# format train data to libsvm:
# data_file format:
# tag\t词 词 词....
# tag\t词 词 词....
# tag\t词 词 词....
# .....

# word_dict_file format:
# 词\t编号
# 词\t编号
# 词\t编号
# ....

# tag_order:
# is a dict which content is fixed{"法规速递":"1","行业动态":"2","股票":"3"}

# output_train_data_file:输出的训练数据文件
# tag编号\t词序号:词权重 词序号:词权重 词序号:词权重....
# tag编号\t词序号:词权重 词序号:词权重 词序号:词权重....
# tag编号\t词序号:词权重 词序号:词权重 词序号:词权重....
# ....
# 词权重用TF值的归一化表示

# output_average_file:输出的均值文件
# 第一维均值\t第二维均值\t......

# output_std_deviation_file:输出的标准差文件
# 第一维标准差\t第二维标准差\t......

def format_train_data(data_file,word_dict_file,tag_order,output_train_data_file,output_average_file,output_std_deviation_file):
    #load useful word dict {"股票":"1","基金":"2"....}
    word_dict_list=[]
    word_dict={}
    fp_word=open(word_dict_file,'r')
    lines=fp_word.readlines()
    for line in lines:
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        if len(line_split) < 2:
            continue
        word_dict[line_split[0]]=line_split[1]
        word_dict_list.append(line_split[0])
    fp_word.close()
    #print 'word_dict: ',word_dict
    
    #cal TF of word
    fp_data=open(data_file,'r')
    lines_ori=fp_data.readlines()
    lines=[]
    for line in lines_ori:
        line_data=line.strip()
        line_data=line_data.decode('utf8')
        line_split=line_data.split('\t')
        if len(line_split) < 2:
            print 'error line:',line
            continue
        lines.append(line)
    fp_data.close()
    max_word_count=0
    #["法规速递","股票","股票","行业动态".....]
    tag_list=[]
    #[{"国务院":12,"银监会":19...},{"大盘":30,"涨停":20...}]
    #word_tf_list=[]
    line_total=len(lines)
    line_count=0
    TF_mat_list=mat(zeros((len(lines),len(word_dict)))).tolist()
    mat_index_list=[]
    for line in lines:
        if line_count%2000==0:
            print 'total line:',line_total,' have process:',line_count
        word_tf={}
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        if len(line_split) < 2:
            print 'error line:',line
            continue
        line_count+=1
        words=line_split[1].split(' ')
        for word in words:
            if word not in word_dict:
                continue 
            if word not in word_tf:
                word_tf[word]=0
            #print word
            word_tf[word]=word_tf[word]+1
            if max_word_count < word_tf[word]:
               max_word_count = word_tf[word]
        #print 'line: ',line_count,' tag:',line_split[0],' word_tf: ',word_tf
        for word in word_tf:
            TF_mat_list[line_count-1][int(word_dict[word])-1]=word_tf[word]
        mat_index_list.append(line_count-1)
        tag_list.append(line_split[0])

    #cal average,stand devition, and var value
    TF_mat=mat(TF_mat_list)
    average=TF_mat.sum(axis=0)/shape(TF_mat)[0] 
    average_list=average.tolist()
    std_deviation=std(array(TF_mat),axis=0) 
    std_deviation_list=std_deviation.tolist()
    
    #ouput average_file, devition_file
    fp_average=open(output_average_file,'w')
    average_output=[]
    for i in range(shape(TF_mat)[1]):
        average_output.append(str(average_list[0][i]))
    fp_average.write('\t'.join(average_output)+'\n')
    fp_average.close()

    fp_std_deviation=open(output_std_deviation_file,'w')
    std_deviation_output=[]
    for i in range(shape(TF_mat)[1]):
        std_deviation_output.append(str(std_deviation_list[i]))
    fp_std_deviation.write('\t'.join(std_deviation_output)+'\n')
    fp_std_deviation.close()
    
    for i in range(shape(TF_mat)[0]):
        for j in range(shape(TF_mat)[1]):
            if TF_mat_list[i][j] != 0.0 and std_deviation_list[j]!=0:
                TF_mat_list[i][j]=float(TF_mat_list[i][j]-average_list[0][j])/std_deviation_list[j]
    
    fp_output=open(output_train_data_file,'w')
    max_feature_value=0
    min_feature_value=100
    feature_value_list=set()
    for line_index in mat_index_list:
        if tag_list[line_index] not in tag_order:
            print 'error data',tag_list[line_index]
            continue
        format_word_tf=[]
        for column_index in range(shape(TF_mat)[1]): 
            if TF_mat_list[line_index][column_index] != 0:
                #format_word_tf.append(word_dict_list[column_index]+':'+str(TF_mat_list[line_index][column_index]))
                if TF_mat_list[line_index][column_index]>max_feature_value:
                    max_feature_value=TF_mat_list[line_index][column_index]
                if TF_mat_list[line_index][column_index]<min_feature_value:
                    min_feature_value=TF_mat_list[line_index][column_index]
                feature_value_list.add(str(regular_feature_value(TF_mat_list[line_index][column_index])))
                format_word_tf.append(str(column_index+1)+':'+str(regular_feature_value(TF_mat_list[line_index][column_index])))
        fp_output.write(tag_order[tag_list[line_index]]+'\t'+' '.join(format_word_tf)+'\n')
        #fp_output.write((tag_list[line_index]+'\t'+' '.join(format_word_tf)+'\n').encode('utf8'))
    fp_output.close()

    print 'max word count',max_word_count,' max_feature_value ',max_feature_value,' min_feature_value ',min_feature_value
    print '\n'.join(feature_value_list)
    return max_word_count

# format test data to libsvm:
# data_file format:
# tag\t词 词 词....
# tag\t词 词 词....
# tag\t词 词 词....
# .....

# word_dict_file format:
# 词\t编号
# 词\t编号
# 词\t编号
# ....

#  max_word_count:归一化时的分母

# output_test_data_file
# tag编号\t词序号:词权重 词序号:词权重 词序号:词权重....
# tag编号\t词序号:词权重 词序号:词权重 词序号:词权重....
# tag编号\t词序号:词权重 词序号:词权重 词序号:词权重....
# ....
# 词权重用TF值的归一化表示

# tag_order:
# is a dict which content is fixed{"法规速递":"1","行业动态":"2","股票":"3"}
def format_test_data(data_file,word_dict_file,average_file,std_deviation_file,tag_order,output_test_data_file):
    #load useful word dict {"股票":"1","基金":"2"....}
    word_dict_list=[]
    word_dict={}
    fp_word=open(word_dict_file,'r')
    lines=fp_word.readlines()
    for line in lines:
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        word_dict[line_split[0]]=line_split[1]
        word_dict_list.append(line_split[0])
    fp_word.close()
    
    #cal TF of word
    fp_data=open(data_file,'r')
    lines_ori=fp_data.readlines()
    lines=[]
    for line in lines_ori:
        line_data=line.strip()
        line_data=line_data.decode('utf8')
        line_split=line_data.split('\t')
        if len(line_split) < 2:
            print 'error line:',line
            continue
        lines.append(line)
    fp_data.close()
    #["法规速递","股票","股票","行业动态".....]
    tag_list=[]
    line_total=len(lines)
    line_count=0
    TF_mat_list=mat(zeros((len(lines),len(word_dict)))).tolist()
    mat_index_list=[]
    for line in lines:
        if line_count%2000==0:
            print 'total line:',line_total,' have process:',line_count
        word_tf={}
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        if len(line_split) < 2:
            print 'error line:',line
            continue
        line_count+=1
        words=line_split[1].split(' ')
        for word in words:
            if word not in word_dict:
                continue 
            if word not in word_tf:
                word_tf[word]=0
            word_tf[word]=word_tf[word]+1
        for word in word_tf:
            TF_mat_list[line_count-1][int(word_dict[word])-1]=word_tf[word]
        mat_index_list.append(line_count-1)
        tag_list.append(line_split[0])

    #get average,stand devition
    TF_mat=mat(TF_mat_list)
    fp_average=open(average_file,'r')
    lines=fp_average.readlines()
    line=lines[0]
    line=line.strip()
    line_split=line.split('\t')
    average_list=[]
    for item in line_split:
        average_list.append(float(item)) 
    fp_average.close()
    fp_deviation=open(std_deviation_file,'r')
    lines=fp_deviation.readlines()
    line=lines[0]
    line=line.strip()
    line_split=line.split('\t')
    std_deviation_list=[]
    for item in line_split:
        std_deviation_list.append(float(item)) 
    fp_deviation.close()
    
    #cal var value
    for i in range(shape(TF_mat)[0]):
        for j in range(shape(TF_mat)[1]):
            if TF_mat_list[i][j] != 0.0 and std_deviation_list[j]!=0:
                TF_mat_list[i][j]=float(TF_mat_list[i][j]-average_list[j])/std_deviation_list[j]
    fp_output=open(output_test_data_file,'w')
    for line_index in mat_index_list:
        if tag_list[line_index] not in tag_order:
            print 'error data',tag_list[line_index]
            continue
        format_word_tf=[]
        for column_index in range(shape(TF_mat)[1]): 
            if TF_mat_list[line_index][column_index] != 0:
                format_word_tf.append(str(column_index+1)+':'+str(regular_feature_value(TF_mat_list[line_index][column_index])))
        fp_output.write(tag_order[tag_list[line_index]]+'\t'+' '.join(format_word_tf)+'\n')
    fp_output.close()



# format to be classified data to libsvm:
# data_file format:
# id\t词 词 词....
# id\t词 词 词....
# id\t词 词 词....
# .....

# word_dict_file format:
# 词\t编号
# 词\t编号
# 词\t编号
# ....

# output_to_be_classified_file
# id\t词序号:词权重 词序号:词权重 词序号:词权重....
# id\t词序号:词权重 词序号:词权重 词序号:词权重....
# id\t词序号:词权重 词序号:词权重 词序号:词权重....
# ....
# 词权重用TF值的归一化表示

# output_id_file
# id
# id
# id
# ....

def format_to_classify_data(data_file,word_dict_file,average_file,std_deviation_file,output_to_be_classify_file,output_id_file):
    #load useful word dict {"股票":"1","基金":"2"....}
    word_dict_list=[]
    word_dict={}
    fp_word=open(word_dict_file,'r')
    lines=fp_word.readlines()
    for line in lines:
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        word_dict[line_split[0]]=line_split[1]
        word_dict_list.append(line_split[0])
    fp_word.close()
    
    #cal TF of word
    fp_data=open(data_file,'r')
    lines_ori=fp_data.readlines()
    lines=[]
    for line in lines_ori:
        line_data=line.strip()
        line_data=line_data.decode('utf8')
        line_split=line_data.split('\t')
        if len(line_split) < 2:
            print 'error line:',line
            continue
        lines.append(line)
    fp_data.close()
    #['1000','2011','2012'....]
    id_list=[]
    line_total=len(lines)
    line_count=0
    TF_mat_list=mat(zeros((len(lines),len(word_dict)))).tolist()
    mat_index_list=[]
    for line in lines:
        if line_count%2000==0:
            print 'total line:',line_total,' have process:',line_count
        word_tf={}
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        if len(line_split) < 2:
            print 'error line:',line
            continue
        line_count+=1
        words=line_split[1].split(' ')
        for word in words:
            if word not in word_dict:
                continue 
            if word not in word_tf:
                word_tf[word]=0
            word_tf[word]=word_tf[word]+1
        for word in word_tf:
            TF_mat_list[line_count-1][int(word_dict[word])-1]=word_tf[word]
        mat_index_list.append(line_count-1)
        id_list.append(line_split[0])

    #get average,stand devition
    TF_mat=mat(TF_mat_list)
    fp_average=open(average_file,'r')
    lines=fp_average.readlines()
    line=lines[0]
    line=line.strip()
    line_split=line.split('\t')
    average_list=[]
    for item in line_split:
        average_list.append(float(item)) 
    fp_average.close()
    fp_deviation=open(std_deviation_file,'r')
    lines=fp_deviation.readlines()
    line=lines[0]
    line=line.strip()
    line_split=line.split('\t')
    std_deviation_list=[]
    for item in line_split:
        std_deviation_list.append(float(item)) 
    fp_deviation.close()
    
    #cal var value
    for i in range(shape(TF_mat)[0]):
        for j in range(shape(TF_mat)[1]):
            if TF_mat_list[i][j] != 0.0 and std_deviation_list[j]!=0:
                TF_mat_list[i][j]=float(TF_mat_list[i][j]-average_list[j])/std_deviation_list[j]
    # output to be classify file
    fp_output=open(output_to_be_classify_file,'w')
    #fp_output_show=open(output_to_be_classify_file+'.show','w')
    for line_index in mat_index_list:
        format_word_tf=[]
        #ouput
        #output_format_word_tf=[]
        for column_index in range(shape(TF_mat)[1]): 
            if TF_mat_list[line_index][column_index] != 0:
                format_word_tf.append(str(column_index+1)+':'+str(regular_feature_value(TF_mat_list[line_index][column_index])))
                #output_format_word_tf.append(word_dict_list[column_index]+':'+str(regular_feature_value(TF_mat_list[line_index][column_index])))
        fp_output.write(id_list[line_index]+'\t'+' '.join(format_word_tf)+'\n')
        #fp_output_show.write(id_list[line_index]+'\t'+' '.join(output_format_word_tf)+'\n')
    fp_output.close()
    #fp_output_show.close()
    # ouput id file
    fp_id=open(output_id_file,'w')
    fp_id.write('\n'.join(id_list))
    fp_id.close() 


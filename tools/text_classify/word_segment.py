#!/usr/bin/python
#coding=utf8

# segment word for train data,and remove stop words
 
import jieba
# load stop words
# file_name: file which save stop words.
#   format is:
#     word
#     word
#     ....
# return: a set of stop word
def load_stop_words(file_name):
    result=set()
    fp=open(file_name,'r')
    for line in fp.readlines():
        result.add(line.strip().decode('utf8'))
    fp.close()
    return result

# seg word for train data and rm stop word at the same time
# input_file: file which save train data
# format is:
#   分类\t文章内容
#   分类\t文章内容
#   .....
# output_file: result of seg word and rm stop word for train data
# format is:
#   分类\t词 词 词...
#   分类\t词 词 词...
#   .....
# stop_words_file: file which save stop words.
# format is:
#   word
#   word
#   ....
# all_tag_file: file save all tags
# format is:
#   tag1
#   tag2
#   ....
# all_word_file: file save all words
# format is:
#   word1
#   word2
#   ....
def data_segment_word_and_rm_stop_word(input_file,output_file,stop_words_file,all_tag_file,all_word_file):
    #load stop word set
    stop_words_set=load_stop_words(stop_words_file)

    fp_output=open(output_file,'w')
    fp_input=open(input_file,'r')
    lines=fp_input.readlines()
    all_tag=set()
    all_word=set()
    line_total=len(lines)
    line_count=1
    for line in lines:
        if line_count % 2000 == 0:
            print "total line:",line_total,"have process line:",line_count
        line_count+=1
        seg_result_no_stop_word=[]
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        if len(line_split) <2:
            print 'error line:',line
            continue
        if line_split[0] not in all_tag:
            all_tag.add(line_split[0])
        seg_result=jieba.cut(line_split[1],cut_all=False)
        for word in seg_result:
            if word not in stop_words_set:
                seg_result_no_stop_word.append(word)
            if word not in all_word:
                all_word.add(word)
        fp_output.write((line_split[0]+'\t'+' '.join(seg_result_no_stop_word)+'\n').encode('utf8'))
    fp_input.close()
    fp_output.close()
    fp_all_tag=open(all_tag_file,'w')
    for tag in all_tag:
        fp_all_tag.write((tag+'\n').encode('utf8'))
    fp_all_tag.close()
    fp_all_word=open(all_word_file,'w')
    for word in all_word:
        fp_all_word.write((word+'\n').encode('utf8'))
    fp_all_word.close()



# seg word data to be classify and rm stop word at the same time
# input_file: file which save data to be classify
# format is:
#   id\t文章内容
#   id\t文章内容
#   .....
# output_file: result of seg word and rm stop word for data to be classify
# format is:
#   id\t词 词 词...
#   id\t词 词 词...
#   .....
# stop_words_file: file which save stop words.
# format is:
#   word
#   word
#   ....
def data_segment_word_and_rm_stop_word_only(input_file,stop_words_file,output_file):
    #load stop word set
    stop_words_set=load_stop_words(stop_words_file)

    fp_output=open(output_file,'w')
    fp_input=open(input_file,'r')
    lines=fp_input.readlines()
    line_total=len(lines)
    line_count=1
    for line in lines:
        if line_count % 100 == 0:
            print "total line:",line_total,"have process line:",line_count
        line_count+=1
        seg_result_no_stop_word=[]
        line=line.strip()
        line=line.decode('utf8')
        line_split=line.split('\t')
        if len(line_split) <2:
            print 'error line:',line
            continue
        seg_result=jieba.cut(line_split[1],cut_all=False)
        for word in seg_result:
            if word not in stop_words_set:
                seg_result_no_stop_word.append(word)
        fp_output.write((line_split[0]+'\t'+' '.join(seg_result_no_stop_word)+'\n').encode('utf8'))
    fp_input.close()
    fp_output.close()

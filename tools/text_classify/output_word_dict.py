#!/usr/bin/python
#coding=utf8
from copy import deepcopy

# calculate word dict. 计算每一类文档所有单词的卡方检验，取前n个。然后把所有这些求并集，作为字典输出
# input file format: 
#   类别名\t词 词 词....
#   类别名\t词 词 词....
#   .....
# output file format: 
#   词\t编号
#   词\t编号
# top_n: 每一类文档取前n个单词做并集
def print_kafang(t,r,k,out):
    fp=open(out,'w')
    for key in t:
        for word in t[key]:
            fp.write(key.encode('utf8')+'\t'+word.encode('utf8')+'\t'+'YY'+str(r[key][word]['YY'])+'\t'\
                +'YN'+str(r[key][word]['YN'])+'\t'+'NY'+str(r[key][word]['NY'])+'\t'+'NN'+str(r[key][word]['NN'])+'\n')
            fp.write(key.encode('utf8')+'\t'+word.encode('utf8')+'\t'+'YY'+str(t[key][word]['YY'])+'\t'\
                +'YN'+str(t[key][word]['YN'])+'\t'+'NY'+str(t[key][word]['NY'])+'\t'+'NN'+str(t[key][word]['NN'])+'\n')
            fp.write(key.encode('utf8')+'\t'+word.encode('utf8')+'\t'+str(k[key][word])+'\n')
    fp.close()

def print_article_class_word(a,out):
    fp=open(out,'w')
    for item in a:
        w_l=[]
        for key in item:
           for word in item[key]:
               w_l.append(word)
        fp.write((key+'\t'+' '.join(w_l)+'\n').encode('utf8'))         
    fp.close()
    

# 返回每一类文本的所有单词的卡方值，从大到小排序
# input file format: 
#   类别名\t词 词 词....
#   类别名\t词 词 词....
#   .....
def kafang(input_file):
    # all words of class,{'股票':('大盘','蓝筹','涨停'.........),'房产':('出租','出让金'.....)}
    class_word_total={}
    # article word list [{'股票':('大盘'...)},{'股票':('大盘'...)}]
    article_class_word=[]
    # class count. {'股票':1000,'房产':2000,'行业':2000}
    class_count={}

    fp=open(input_file,'r')
    lines=fp.readlines()
    line_total=len(lines)
    line_count=0
    valid_total_count=0
    print ' now static class_word_total, article_class_word and class count... '
    for line in lines:
        line_count +=1
        if line_count%2000==0:
            print "line total: ",line_total," have process:",line_count
        line = line.strip()
        line = line.decode('utf8')
        line_split=line.split('\t')
        if len(line_split) < 2:
            print 'error line:',line
            continue
        valid_total_count += 1
        if line_split[0] not in class_word_total:
           class_word_total[line_split[0]]=set()
        if line_split[0] not in class_count:
           class_count[line_split[0]]=0
        class_count[line_split[0]]+=1
        line_class_word={}
        line_class_word[line_split[0]]=set()

        line_words=line_split[1].split(' ')
        for word in line_words:
            if word not in class_word_total[line_split[0]]:
                class_word_total[line_split[0]].add(word) 
            if word not in line_class_word[line_split[0]]:
                line_class_word[line_split[0]].add(word) 
        article_class_word.append(line_class_word)
    fp.close()
    print ' total valid count :',valid_total_count
    #print_article_class_word(article_class_word,'/tmp/article')
   
    # cal kangfang real count
    print ' cal kangfang real count...'
    # {'股票':{'大盘':{'YY':1,'YN':2,'NY':3,'NN':4},...},...}
    kafang_real={}
    for key in class_word_total:
        for word in class_word_total[key]:
            if key not in kafang_real:
                kafang_real[key]={}
            if word not in kafang_real[key]:
                kafang_real[key][word]={}
            kafang_real[key][word]['YY']=0
            kafang_real[key][word]['YN']=0
            kafang_real[key][word]['NY']=0
            kafang_real[key][word]['NN']=0
    # article class count. {'股票':0.2,'房产':0.4,'行业':0.4}
    class_rate={}
    for key in class_count:
        if key not in class_rate:
            class_rate[key]=0.0
        class_rate[key]=float(class_count[key])/valid_total_count  
    
    for key_class in kafang_real:
        word_total_count=len(kafang_real[key_class])
        word_cur_count=0
        for word in kafang_real[key_class]:
            word_cur_count+=1
            if word_cur_count %2000==0:
                print key_class,' total ',word_total_count,' cur ',word_cur_count
            for item in article_class_word:
                for key_article in item:
                    if key_article == key_class:
                        if word in item[key_article]:
                            #print 'YY',key_article,key_class,word
                            kafang_real[key_class][word]['YY']+=1
                        else:
                            #print 'NY',key_article,key_class,word
                            kafang_real[key_class][word]['NY']+=1
                    else:
                        if word in item[key_article]:
                            #print 'YN',key_article,key_class,word
                            kafang_real[key_class][word]['YN']+=1
                        else:
                            #print 'YN',key_article,key_class,word
                            kafang_real[key_class][word]['NN']+=1

    # cal kangfang theory count
    print ' cal kangfang theory count...'
    kafang_theory=deepcopy(kafang_real) 
    for key_class in kafang_theory:
        for word in kafang_theory[key_class]:
            kafang_theory[key_class][word]['YY']=int((kafang_real[key_class][word]['YY']+\
                kafang_real[key_class][word]['YN'])*class_rate[key_class])
            kafang_theory[key_class][word]['YN']=int((kafang_real[key_class][word]['YY']+\
                kafang_real[key_class][word]['YN'])*(1-class_rate[key_class]))
            kafang_theory[key_class][word]['NY']=int((kafang_real[key_class][word]['NY']+\
                kafang_real[key_class][word]['NN'])*class_rate[key_class])
            kafang_theory[key_class][word]['NN']=int((kafang_real[key_class][word]['NY']+\
                kafang_real[key_class][word]['NN'])*(1-class_rate[key_class]))
      

    # cal kafang value    
    print ' cal kangfang value...'
    real_YY_min=0
    for key in class_count:
        if real_YY_min < class_count[key]*0.05:
            real_YY_min=class_count[key]*0.05
    kafang_value={}
    for key_tag in kafang_real:
        kafang_value[key_tag]={}
        for key_word in kafang_real[key_tag]:
           # kafang_value[key_tag][key_word]=kafang_real[key_tag][key_word]['YY']-kafang_real[key_tag][key_word]['YN']
            real_YY=kafang_real[key_tag][key_word]['YY']
            real_YN=kafang_real[key_tag][key_word]['YN']
            real_NY=kafang_real[key_tag][key_word]['NY']
            real_NN=kafang_real[key_tag][key_word]['NN']
            theory_YY=kafang_theory[key_tag][key_word]['YY']
            theory_YN=kafang_theory[key_tag][key_word]['YN']
            theory_NY=kafang_theory[key_tag][key_word]['NY']
            theory_NN=kafang_theory[key_tag][key_word]['NN']
            if theory_YY==0:
                theory_YY=1
            if theory_YN==0:
                theory_YN=1
            if theory_NY==0:
                theory_NY=1
            if theory_NN==0:
                theory_NN=1
            if real_YY < real_YY_min:
                kafang_value[key_tag][key_word]=0
            else:
                kafang_value[key_tag][key_word]=pow(real_YY-theory_YY,2)/theory_YY+\
                pow(real_YN-theory_YN,2)/theory_YN+pow(real_NY-theory_NY,2)/theory_NY+\
                pow(real_NN-theory_NN,2)/theory_NN
    
    #print_kafang(kafang_theory,kafang_real,kafang_value,'/tmp/kafang')
    # sort kafang value
    print ' sort kafang value...'
    sorted_kafang_value={}
    for key_tag in kafang_value:
        cur_tag_kafang_value=kafang_value[key_tag]
        sorted_dict=sorted(cur_tag_kafang_value.iteritems(),key=lambda d:d[1],reverse=True) 
        sorted_kafang_value[key_tag]=sorted_dict
    return sorted_kafang_value

def ouput_word_dict(input_file,output_file,tag_top_n_word,top_n=50):
    kafang_value=kafang(input_file)
    # get top n kafang value
    print ' get top n kafang value...'
    useful_word=set()
    fp_tag=open(tag_top_n_word,'w')
    for key_tag in kafang_value:
        sorted_dict=kafang_value[key_tag] 
        fp_tag.write((key_tag+'\t'+str(len(sorted_dict))+'------------------------------\n').encode('utf8'))
        print type(sorted_dict)
        n=0
        for i in range(len(sorted_dict)):
            fp_tag.write((sorted_dict[i][0]+'\t'+str(sorted_dict[i][1])+'\n').encode('utf8'))
            if n < top_n and float(sorted_dict[i][1]>1):
                if (sorted_dict[i][0] not in useful_word) and (sorted_dict[i][0]!=None) and (len(sorted_dict[i][0])>0):
                    useful_word.add(sorted_dict[i][0])
                n+=1
            else:
                break
    fp_tag.close()

    #ouput useful word to file 
    print ' ouput useful word...'
    fp_output=open(output_file,'w')
    word_count=1
    for word in useful_word:
        fp_output.write((word+'\t'+str(word_count)+'\n').encode('utf8'))
        word_count+=1
    fp_output.close()

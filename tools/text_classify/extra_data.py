#!/usr/bin/python
#coding=utf8

#导出周律师的历史法规速递数据
# input_file format:
# 训练测试标记\t分类标记\t分词内容\t原始内容
# output_file format:
# 法规速递\t内容
def extra_data_to_file(input_file,output_file,data_type):
    fp_input=open(input_file,'r')
    fp_output=open(output_file,'w')   
    lines=fp_input.readlines()
    for line in lines:
        line=line.strip()
        line=line.decode('utf8') 
        line_split=line.split('\t')
        if len(line_split) < 4:
            print 'error line:',line
            continue
        if line_split[1]==data_type:
            content_split=line_split[3].split('\x01')
            if len(content_split) < 2:
                print 'error line:',line
                continue
            if data_type == '1':
                fp_output.write(('法规速递'.decode('utf8')+'\t'+\
                    content_split[len(content_split)-2].replace('\x02','')+'\n').encode('utf8'))
            if data_type == '0':
                fp_output.write(('行业动态'.decode('utf8')+'\t'+\
                    content_split[len(content_split)-2].replace('\x02','')+'\n').encode('utf8'))
            
    fp_output.close()
    fp_input.close()
    

if __name__=='__main__':
    print 'output data to ./data/extra_fagui_data'
    extra_data_to_file('/Users/fuhonglei/Downloads/docwordseg.txt','./data/extra_fagui_data','1')
    extra_data_to_file('/Users/fuhonglei/Downloads/docwordseg.txt','./data/extra_hangye_data','0')

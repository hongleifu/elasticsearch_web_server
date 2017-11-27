#/usr/bin/python
import sys
def get_crawling_sites(file_name):
    print 'now get sites from ',file_name
    result=[]
    fp=open(file_name,'r')
    lines=fp.readlines()
    for i in range(len(lines)):
        if lines[i].strip().find('repeated-crawl-urls')!= -1:
            result.append(lines[i+1].strip())
    fp.close()
    print 'result is :',result
    return result

def dump_list_to_file(info,file_name):
    print 'now dump sites to ',file_name
    fp=open(file_name,'w')
    fp.write('\n'.join(info).encode('utf8'))
    fp.close()

def get_sites_and_dump_to_file(input_file,output_file):
    dump_list_to_file(get_crawling_sites(input_file),output_file)


if __name__=='__main__':
    if len(sys.argv) != 3:
        print 'error param, you can try python get_crawling_sites.py /tmp/input /tmp/output'
    else:
        get_sites_and_dump_to_file(sys.argv[1],sys.argv[2])
       

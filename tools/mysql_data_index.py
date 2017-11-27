#/usr/bin/python
import os
import sys

if __name__ =="__main__":
  if len(sys.argv) != 2:
    print "error param! you can try mysql_data_index.py /Users/fuhonglei/Work/elastic_search_jdbc/elasticsearch-jdbc-2.3.4.0/bin/mysql-blog.sh" 
  else:
    cmd=str(sys.argv[1])
    os.system(cmd)

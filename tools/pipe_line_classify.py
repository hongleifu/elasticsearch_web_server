#/usr/bin/python
import json
import os 
import sys 

#pipe line for:
#1.copy mysql data during some time from crawler to finance_no2
#2.classify and rank these data
#3.fill other values to these data such as pagerank
#4.index those data to elastic search
def pipe_line_classify(id_begin,id_end):
  #classify and sort
  print 'now begin class and fill level-----------------',id_begin,id_end
  if id_begin != 0 and id_end != 0:
    #cmd='cd /data/yx/svr/finance_one/tools/machine_learning/program/ && /bin/bash run.sh '+time_begin+' '+time_update+' ' +' > log.txt'
    cmd='cd /data/yx/svr/finance_one/tools/machine_learning/program/ && /bin/bash run.sh '+str(id_begin)+' ' + str(id_end) +'  > log.txt'
    print ' classify cmd is :',cmd
    os.system(cmd)
  else:
    print 'id_begin or id_end is 0!'

if __name__=='__main__':
  if len(sys.argv) != 3:
    print "error param! please try python pipe_line_classify.py id_begin id_end"
  else:
    id_begin=sys.argv[1]
    id_end=sys.argv[2]
    print ' now classify data id from ',id_begin,' to ',id_end
    pipe_line_classify(id_begin,id_end)

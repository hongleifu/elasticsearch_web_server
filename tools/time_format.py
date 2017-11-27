#!/usr/local/python/bin/python
# encoding=utf8
import time
def cur_time():
  return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

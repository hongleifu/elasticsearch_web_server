# -*- coding: utf-8 -*-
import logging
import datetime
import os


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger(logging.Logger):
    cur_path =os.getcwd()
    format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    curDate = datetime.date.today() - datetime.timedelta(days=0)
    infoLogName = r'%s%sinfo_%s.log' % (os.getcwd(),'/logs/',curDate)
    # errorLogName = r'/Users/liangxinxin/Desktop/error_%s.log' % curDate
    # errorLogName = r'%s%sserror_%s.log' % (os.getcwd(),'/logs/',curDate)
    formatter = logging.Formatter(format)

    infoLogger = logging.getLogger("infoLogger")
    # errorLogger = logging.getLogger("errorLogger")

    infoLogger.setLevel(logging.INFO)
    # errorLogger.setLevel(logging.ERROR)

    infoHandler = logging.FileHandler(infoLogName, 'a')
    infoHandler.setLevel(logging.INFO)
    infoHandler.setFormatter(formatter)

    # errorHandler = logging.FileHandler(errorLogName, 'a')
    # errorHandler.setLevel(logging.ERROR)
    # errorHandler.setFormatter(formatter)

    testHandler = logging.StreamHandler()
    testHandler.setFormatter(formatter)
    testHandler.setLevel(logging.INFO)

    infoLogger.addHandler(infoHandler)
    infoLogger.addHandler(testHandler)
    # errorLogger.addHandler(errorHandler)  #暂时没有用到


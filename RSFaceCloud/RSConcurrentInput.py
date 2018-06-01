#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

class RsInput:
    '''
    #设置线程或者进程输入
    '''
    def __init__(self,threadId,filelist,host,appid,appsecret):
        self.__threadId = threadId      #线程ID
        self.__filelist = filelist      #图片路径列表
        self.__host = host
        self.__appid = appid
        self.__appsecret = appsecret
    def getThreadId(self):
        return self.__threadId
    def getFileList(self):
        return self.__filelist
    def getHost(self):
        return self.__host
    def getAppId(self):
        return self.__appid
    def getAppSecret(self):
        return self.__appsecret

class statisticsData:
    def __init__(self,request_count=0,request_count_success=0,request_response_time = 0.0):
        self.request_count = request_count                      #请求总数
        self.request_count_success = request_count_success      #请求成功数
        self.request_response_time = request_response_time      #请求成功总耗时
    def add(self,data_statistics):
        self.request_count += data_statistics.request_count
        self.request_count_success += data_statistics.request_count_success
        self.request_response_time += data_statistics.request_response_time
    def getSucccessRate(self):
        try:
            out=float(self.request_count_success / self.request_count)
            return out
        except:
            logging.error('getAverageRate error!!!')
            return 0.0

    def getAverageTime(self):
        try:
            out = float(self.request_response_time / self.request_count_success)
            return out
        except:
            logging.error('getAverageRate error!!!')
            return 0.0

    def toString(self):
        try:
            strOut = '\t请求总次数:\t' +str(self.request_count) + '\n'
            strOut += '\t请求成功总次数:\t' +str(self.request_count_success) +'\n'
            strOut += '\t请求成功总耗时:\t'+ str(self.request_response_time)+ 'ms\n'
            return strOut
        except:
            logging.error('toString error!!!')

    def toTuple(self):
        return self.request_count,self.request_count_success,self.request_response_time

class vStatisticsData:
    def __init__(self):
        self.dete = statisticsData()                    #检测测试结果
        self.recogntion = statisticsData()              #识别测试结果

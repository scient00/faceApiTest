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
    def __repr__(self):
        return 'request_count:\t' + str(self.request_count) +'\nrequest_count_success:\t' + str(self.request_count_success) + '\nrequest_count_success:\t' + str(self.request_count_success)

    def add(self,data_statistics):
        self.request_count += data_statistics.request_count
        self.request_count_success += data_statistics.request_count_success
        self.request_response_time += data_statistics.request_response_time

    def getSucccessRate(self):
        try:
            out=float(self.request_count_success / self.request_count)
            return out
        except:
            return 0.0

    def getAverageTime(self):
        try:
            out = float(self.request_response_time / self.request_count_success)
            return out
        except:
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
        self.detect = statisticsData()                      #检测测试结果
        self.identification = statisticsData()              #识别测试结果
        self.addFaceId = statisticsData()                   #添加faceId
        self.verificationByfaceId = statisticsData()
        self.verificationBypersonid = statisticsData()
        self.imageIdentification = statisticsData()
        self.createPersonId = statisticsData()
        self.deletePersonId = statisticsData()
        self.emptyPerson = statisticsData()
        self.removeFace = statisticsData()
        self.createGroups = statisticsData()
        self.deleteGroups = statisticsData()
        self.addPersonId = statisticsData()
        self.emptyGroups = statisticsData()
        self.removePerson = statisticsData()

    def __repr__(self):
        return 'detect:\n' + str(self.detect) + '\nidentification:\t' + str(self.identification)+\
               'addFaceId:\n' + str(self.addFaceId) + '\nverificationByfaceId:\t' + str(self.verificationByfaceId) +\
               'verificationBypersonid:\n' + str(self.verificationBypersonid) + '\nimageIdentification:\t' + str(self.imageIdentification)+\
               'createPersonId:\n' + str(self.createPersonId) + '\ndeletePersonId:\t' + str(self.deletePersonId)+\
               'emptyPerson:\n' + str(self.emptyPerson) + '\nremoveFace:\t' + str(self.removeFace) +\
               'createGroups:\n' + str(self.createGroups) + '\ndeleteGroups:\t' + str(self.deleteGroups) +\
               'addPersonId:\n' + str(self.addPersonId) + '\nemptyGroups:\t' + str(self.emptyGroups) + '\nremovePerson:\t' + str(self.removePerson)

    def getDict(self):
        try:
            sDict = { 'detect':self.detect,
                      'addFaceId':self.addFaceId,
                      'identification':self.identification,
                      'verificationByfaceId':self.verificationByfaceId,
                      'verificationBypersonid':self.verificationBypersonid,
                      'imageIdentification':self.imageIdentification,
                      'createPersonId':self.createPersonId,
                      'deletePersonId': self.deletePersonId,
                      'emptyPerson': self.emptyPerson,
                      'removeFace': self.removeFace,
                      'createGroups': self.createGroups,
                      'deleteGroups': self.deleteGroups,
                      'addPersonId': self.addPersonId,
                      'emptyGroups': self.emptyGroups,
                      'removePerson':self.removePerson}
            return sDict
        except:
            logging.error('getDict error!!!')
            return {}

    def getDictTuple(self):
        try:
            sDict = {'detect': self.detect.toTuple(),
                     'addFaceId': self.addFaceId.toTuple(),
                     'identification': self.identification.toTuple(),
                     'verificationByfaceId': self.verificationByfaceId.toTuple(),
                     'verificationBypersonid': self.verificationBypersonid.toTuple(),
                     'imageIdentification': self.imageIdentification.toTuple(),
                     'createPersonId': self.createPersonId.toTuple(),
                     'deletePersonId': self.deletePersonId.toTuple(),
                     'emptyPerson': self.emptyPerson.toTuple(),
                     'removeFace': self.removeFace.toTuple(),
                     'createGroups': self.createGroups.toTuple(),
                     'deleteGroups': self.deleteGroups.toTuple(),
                     'addPersonId': self.addPersonId.toTuple(),
                     'emptyGroups': self.emptyGroups.toTuple(),
                     'removePerson': self.removePerson.toTuple()}
            return sDict
        except:
            logging.error('getDict error!!!')
            return {}

    def push(self,dictdata):
        try:
            self.detect.add(statisticsData(dictdata['detect'][0], dictdata['detect'][1], dictdata['detect'][2]))
            self.createPersonId.add(statisticsData(dictdata['createPersonId'][0], dictdata['createPersonId'][1], dictdata['createPersonId'][2]))
            self.createGroups.add(statisticsData(dictdata['createGroups'][0], dictdata['createGroups'][1], dictdata['createGroups'][2]))
            self.addFaceId.add(statisticsData(dictdata['addFaceId'][0], dictdata['addFaceId'][1], dictdata['addFaceId'][2]))
            self.addPersonId.add(statisticsData(dictdata['addPersonId'][0], dictdata['addPersonId'][1], dictdata['addPersonId'][2]))
            self.identification.add(statisticsData(dictdata['identification'][0], dictdata['identification'][1], dictdata['identification'][2]))
            self.verificationByfaceId.add(statisticsData(dictdata['verificationByfaceId'][0], dictdata['verificationByfaceId'][1], dictdata['verificationByfaceId'][2]))
            self.verificationBypersonid.add(statisticsData(dictdata['verificationBypersonid'][0], dictdata['verificationBypersonid'][1], dictdata['verificationBypersonid'][2]))
            self.imageIdentification.add(statisticsData(dictdata['imageIdentification'][0], dictdata['imageIdentification'][1], dictdata['imageIdentification'][2]))
            self.removeFace.add(statisticsData(dictdata['removeFace'][0], dictdata['removeFace'][1], dictdata['removeFace'][2]))
            self.deletePersonId.add(statisticsData(dictdata['deletePersonId'][0], dictdata['deletePersonId'][1], dictdata['deletePersonId'][2]))
            self.deleteGroups.add(statisticsData(dictdata['deleteGroups'][0], dictdata['deleteGroups'][1], dictdata['deleteGroups'][2]))
            self.emptyPerson.add(statisticsData(dictdata['emptyPerson'][0], dictdata['emptyPerson'][1], dictdata['emptyPerson'][2]))
            self.emptyGroups.add(statisticsData(dictdata['emptyGroups'][0], dictdata['emptyGroups'][1], dictdata['emptyGroups'][2]))
            self.removePerson.add(statisticsData(dictdata['removePerson'][0], dictdata['removePerson'][1], dictdata['removePerson'][2]))

        except:
            logging.error('push error!!!')
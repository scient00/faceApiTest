#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import datetime,logging,time
from RSFaceCloud.RSConcurrentInput import *
from RSFaceCloud.RSfaceClientCloud import *

ThreadLock = threading.Lock()

class RsFaceThread(threading.Thread):
    def __init__(self,rsInput):
        threading.Thread.__init__(self)
        self.__rsInput = rsInput
        self.__vStatDataResult = vStatisticsData()


    def run(self):
        try:
            logging.info('Start Thread %d....' % self.__rsInput.getThreadId())
            self.__rsFace = RSFace(self.__rsInput.getHost(), self.__rsInput.getAppId(), self.__rsInput.getAppSecret())

            for k,filepath in enumerate(self.__rsInput.getFileList()):
                #检测测试
                self.__vStatDataResult.dete.request_count +=1
                outResult = self.__rsFace.detect(filepath)
                if outResult != None and outResult[0]['status'] == 'ok':
                    self.__vStatDataResult.dete.request_count_success += 1
                    self.__vStatDataResult.dete.request_response_time += outResult[1]

                    self.__outPrint(outResult[0])

                    #识别测试
                    self.__vStatDataResult.recogntion.request_count +=1
                    faceId = outResult[0]['faces'][0]['face_id']
                    outResult = self.__rsFace.verificationByfaceId(faceId,faceId)
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__outPrint(outResult[0])
                        self.__vStatDataResult.recogntion.request_count_success += 1
                        self.__vStatDataResult.recogntion.request_response_time +=outResult[1]


                    ########################
                    outResult = self.__rsFace.createPersonId(faceId,'rs_' + str(time.time()))
                    if outResult != None and outResult[0]['status'] == 'ok':
                        person_id = outResult[0]['person_id']
                        outResult = self.__rsFace.addFaceId(faceId,person_id)
                        outResult = self.__rsFace.verificationBypersonid(faceId, person_id)
                        outResult = self.__rsFace.removeFace(person_id, faceId)
                        outResult = self.__rsFace.identification(faceId, person_id)

                        outResult = self.__rsFace.createGroups(person_id, 'RsGroups'+str(time.time()))
                        groupsId = outResult[0]['group_id']
                        outResult = self.__rsFace.deleteGroups(groupsId)

                        outResult = self.__rsFace.imageIdentification(filepath, groupsId)
                        outResult = self.__rsFace.addPersonId(person_id, groupsId)

                        outResult = self.__rsFace.removePerson(person_id, groupsId)

                        outResult = self.__rsFace.deletePersonId(person_id)
                        outResult = self.__rsFace.emptyGroups(groupsId)

            logging.info('End of the thread[%d]' % self.__rsInput.getThreadId())
        except:
            logging.error('start thread error!!!')
    def getDataStatistics(self):
        return self.__vStatDataResult

    def __outPrint(self, outResult):
        try:
            #ThreadLock.acquire()
            print(str(datetime.datetime.now()) + '-thread[%d]' % self.__rsInput.getThreadId(), outResult)
            #ThreadLock.release()
        except:
            logging.error('__outPrint error!!!')


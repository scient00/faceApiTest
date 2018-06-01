#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime,logging,time,os
from RSFaceCloud.RSConcurrentInput import *
from multiprocessing import Process,Lock,Queue
from RSFaceCloud.RSfaceClientCloud import *
from BasicMethod.BasicMethod import *
ProcessLock = Lock()
TMP_PATH = './.tmp'
class RsFaceProcesses(Process):
    def __init__(self,rsInput):
        super().__init__()
        self.__rsInput = rsInput
        self.__vStatDataResult = vStatisticsData()

    def run(self):
        try:
            logging.info('Start Processes[%d]...' % self.__rsInput.getThreadId())
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

            self.__writeTmpData()
            logging.info('End of the processes[%d]' % self.__rsInput.getThreadId())

        except:
            logging.error('start processes error!!!')

    def __writeTmpData(self):
        try:
            ProcessLock.acquire()
            CreateFolder(TMP_PATH)
            with open(TMP_PATH + '/processdata.ly', 'a') as wfile:
                for data in list(self.__vStatDataResult.dete.toTuple()):
                    wfile.write(str(data) + ' ')
                for data in list(self.__vStatDataResult.recogntion.toTuple()):
                    wfile.write(str(data) + ' ')
                wfile.write('\n')
            ProcessLock.release()
        except:
            logging.error('__writeTmpData error!!!'+str(self.__rsInput.getThreadId()))

    def __outPrint(self, outResult):
        try:
            #ProcessLock.acquire()
            print(str(datetime.datetime.now()) +'-process[%d]' % self.__rsInput.getThreadId(), outResult)
            #ProcessLock.release()
        except:
            logging.error('__outPrint error!!!')


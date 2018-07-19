#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import datetime,logging,time,random
from RSFaceCloud.RSConcurrentInput import *
from RSFaceCloud.RSfaceClientCloud import *

ThreadLock = threading.Lock()

class RsFaceThread(threading.Thread):
    def __init__(self,rsInput,TestItemdict):
        threading.Thread.__init__(self)
        self.__rsInput = rsInput
        self.__vStatDataResult = vStatisticsData()
        self.__TestItemdict = TestItemdict

    def run(self):
        try:
            logging.info('Start Thread %d....' % self.__rsInput.getThreadId())

            self.__rsFace = RSFace(self.__rsInput.getHost(), self.__rsInput.getAppId(), self.__rsInput.getAppSecret())
            vfaceId = []
            vpersonId = []
            vgroups = []
            # 检测测试
            if self.__TestItemdict['detect'] == 1:
                for k,filepath in enumerate(self.__rsInput.getFileList()):
                    self.__vStatDataResult.detect.request_count +=1
                    outResult = self.__rsFace.detect(filepath)
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.detect.request_count_success += 1
                        self.__vStatDataResult.detect.request_response_time += outResult[1]
                        self.__outPrint(outResult)
                        vfaceId.append(outResult[0]['faces'][0]['face_id'])


            if self.__TestItemdict['createPersonId'] == 1:
                for index,faceId in enumerate(vfaceId):
                    self.__vStatDataResult.createPersonId.request_count += 1
                    outResult = self.__rsFace.createPersonId(faceId,'readsense_person_' + str(self.__rsInput.getThreadId()) + str(index))
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.createPersonId.request_count_success += 1
                        self.__vStatDataResult.createPersonId.request_response_time += outResult[1]
                        self.__outPrint(outResult)
                        vpersonId.append(outResult[0]['person_id'])


            if self.__TestItemdict['createGroups'] == 1:
                for index, personId in enumerate(vpersonId):
                    self.__vStatDataResult.createGroups.request_count += 1
                    outResult = self.__rsFace.createGroups(personId,'readsense_groups_' +str(self.__rsInput.getThreadId()) +  str(index))
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.createGroups.request_count_success += 1
                        self.__vStatDataResult.createGroups.request_response_time += outResult[1]
                        self.__outPrint(outResult)
                        vgroups.append(outResult[0]['group_id'])

            if self.__TestItemdict['addFaceId'] == 1:
                for faceId in vfaceId:
                    self.__vStatDataResult.addFaceId.request_count += 1
                    outResult = self.__rsFace.addFaceId(faceId, vpersonId[random.randint(0,len(vpersonId)-1)])
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.addFaceId.request_count_success += 1
                        self.__vStatDataResult.addFaceId.request_response_time += outResult[1]
                        self.__outPrint(outResult)


            if self.__TestItemdict['addPersonId'] == 1:
                for personId in vpersonId:
                    self.__vStatDataResult.addPersonId.request_count += 1
                    outResult = self.__rsFace.addPersonId(personId, vgroups[random.randint(0,len(vgroups)-1)])
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.addPersonId.request_count_success += 1
                        self.__vStatDataResult.addPersonId.request_response_time += outResult[1]
                        self.__outPrint(outResult)


            if self.__TestItemdict['identification'] == 1:
                for faceId in vfaceId:
                    self.__vStatDataResult.identification.request_count += 1
                    outResult = self.__rsFace.identification(faceId, vgroups[random.randint(0, len(vgroups) - 1)],10)
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.identification.request_count_success += 1
                        self.__vStatDataResult.identification.request_response_time += outResult[1]
                        self.__outPrint(outResult)

            if self.__TestItemdict['verificationByfaceId'] == 1:
                for faceId in vfaceId:
                    self.__vStatDataResult.verificationByfaceId.request_count += 1
                    outResult = self.__rsFace.verificationByfaceId(faceId, vfaceId[random.randint(0, len(vfaceId) - 1)])
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.verificationByfaceId.request_count_success += 1
                        self.__vStatDataResult.verificationByfaceId.request_response_time += outResult[1]
                        self.__outPrint(outResult)


            if self.__TestItemdict['verificationBypersonid'] == 1:
                for faceId in vfaceId:
                    self.__vStatDataResult.verificationBypersonid.request_count += 1
                    outResult = self.__rsFace.verificationBypersonid(faceId, vpersonId[random.randint(0, len(vpersonId) - 1)])
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.verificationBypersonid.request_count_success += 1
                        self.__vStatDataResult.verificationBypersonid.request_response_time += outResult[1]
                        self.__outPrint(outResult)


            if self.__TestItemdict['imageIdentification'] == 1:
                for k,filepath in enumerate(self.__rsInput.getFileList()):
                    self.__vStatDataResult.imageIdentification.request_count +=1
                    outResult = self.__rsFace.imageIdentification(filepath,vgroups[random.randint(0, len(vgroups) - 1)])
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.imageIdentification.request_count_success += 1
                        self.__vStatDataResult.imageIdentification.request_response_time += outResult[1]
                        self.__outPrint(outResult)


            if self.__TestItemdict['removeFace'] == 1:
                for faceId in vfaceId:
                    self.__vStatDataResult.removeFace.request_count += 1
                    outResult = self.__rsFace.removeFace(vpersonId[random.randint(0, len(vpersonId) - 1)],faceId)
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok' or outResult[0]['status']=='not_found':
                        self.__vStatDataResult.removeFace.request_count_success += 1
                        self.__vStatDataResult.removeFace.request_response_time += outResult[1]
                        self.__outPrint(outResult)


            if self.__TestItemdict['deletePersonId'] == 1:
                for personId in vpersonId:
                    self.__vStatDataResult.deletePersonId.request_count += 1
                    outResult = self.__rsFace.deletePersonId(personId)
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.deletePersonId.request_count_success += 1
                        self.__vStatDataResult.deletePersonId.request_response_time += outResult[1]
                        self.__outPrint(outResult)

            if self.__TestItemdict['deleteGroups'] == 1:
                for groups in vgroups:
                    self.__vStatDataResult.deleteGroups.request_count += 1
                    outResult = self.__rsFace.deleteGroups(groups)
                    if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.deleteGroups.request_count_success += 1
                        self.__vStatDataResult.deleteGroups.request_response_time += outResult[1]
                        self.__outPrint(outResult)

            if self.__TestItemdict['emptyPerson'] == 1:
                for personId in vpersonId:
                    self.__vStatDataResult.emptyPerson.request_count += 1
                    outResult = self.__rsFace.emptyPerson(personId)
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.emptyPerson.request_count_success += 1
                        self.__vStatDataResult.emptyPerson.request_response_time += outResult[1]
                        self.__outPrint(outResult)

            if self.__TestItemdict['emptyGroups'] == 1:
                for groups in vgroups:
                    self.__vStatDataResult.emptyGroups.request_count += 1
                    outResult = self.__rsFace.emptyGroups(groups)
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok':
                        self.__vStatDataResult.emptyGroups.request_count_success += 1
                        self.__vStatDataResult.emptyGroups.request_response_time += outResult[1]
                        self.__outPrint(outResult)

            if self.__TestItemdict['removePerson'] == 1:
                for personId in vpersonId:
                    self.__vStatDataResult.removePerson.request_count += 1
                    outResult = self.__rsFace.removePerson(personId,vgroups[random.randint(0, len(vgroups) - 1)])
                    if outResult != None:
                    #if outResult != None and outResult[0]['status'] == 'ok' or outResult[0]['status'] == 'group_not_found':
                        self.__vStatDataResult.removePerson.request_count_success += 1
                        self.__vStatDataResult.removePerson.request_response_time += outResult[1]
                        self.__outPrint(outResult)

            logging.info('End of the thread[%d]' % self.__rsInput.getThreadId())
        except :
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


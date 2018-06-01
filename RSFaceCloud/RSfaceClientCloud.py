#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json,requests
import threading

class RSFace(object):
    def __init__(self,http_url,api_id,api_secret):
        self.__http_url = http_url
        self.__api_id = api_id
        self.__api_secret = api_secret

    def detect(self,filepath):
        '''
        #用于检测人脸并返回faceid
        :param filepath:
        :return:
        '''
        try:
            http_url_detect = self.__http_url + '/faces/detection'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret
            }
            files = { 'file': ('image.jpg',self.__file2ImageBuffer(filepath), 'image/jpeg')}
            repResult = requests.post(http_url_detect, data=data, files = files)

            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None

    def identification(self,face_id,group_id):
        '''
        # 识别face_id是谁，返回top5最相似的人
        :param face_id:
        :param group_id:
        :return:
        '''
        try:
            http_url_identification = self.__http_url + '/faces/identification'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'face_id': face_id,
                'group_id': group_id
            }
            repResult = requests.post(http_url_identification,data = data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None

    def __file2ImageBuffer(self,path):
        if os.path.exists(path):
            with open(path,'rb') as file:
                data = file.read()
                return data
        else:
            return 0


    def verificationByfaceId(self,face_id1,face_id2):
        '''
        #验证face_id与face_id2是否是同一个人
        :param face_id1:
        :param face_id2:
        :return:
        '''
        try:
            http_url_verification = self.__http_url + '/faces/verification'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'face_id': face_id1,
                'face_id2': face_id2
            }
            repResult = requests.post(http_url_verification,data = data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def verificationBypersonid(self,face_id1,person_id):
        '''
        #face_id与person_id是否是同一个人
        :param face_id1:
        :param person_id:
        :return:
        '''
        try:
            http_url_verification = self.__http_url + '/faces/verification'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'face_id': face_id1,
                'person_id': person_id
            }
            repResult = requests.post(http_url_verification,data = data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def imageIdentification(self,filepath,group_id):
        '''
        #上传一张图片，返回该图片中的人脸信息和识别结果
        :param filepath:
        :param group_id:
        :return:
        '''
        try:
            http_url_image_identication = self.__http_url + '/faces/image_identification'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'group_id':group_id
            }
            files = {'file': ('image.jpg', self.__file2ImageBuffer(filepath), 'image/jpeg')}
            repResult = requests.post(http_url_image_identication, data=data, files=files)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def createPersonId(self,face_id,name):
        '''
        #创建一个Person实例
        :param face_id:
        :param name:
        :return:
        '''
        try:
            http_url_image_createPersonId = self.__http_url + '/people/create'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'face_id':face_id,
                'name': name
            }
            repResult = requests.post(http_url_image_createPersonId, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def deletePersonId(self,person_id):
        '''
        #删除一个Person实例
        :param person_id:
        :return:
        '''
        try:
            http_url_image_deletePersonId = self.__http_url + '/people/delete'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'person_id': person_id
            }
            repResult = requests.post(http_url_image_deletePersonId,data = data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def addFaceId(self,face_id,person_id):
        '''
        #给一个Person实例添加Face
        :param face_id:
        :param person_id:
        :return:
        '''
        try:
            http_url_add_face_id = self.__http_url + '/people/add_face'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'face_id':face_id,
                'person_id': person_id
            }
            repResult = requests.post(http_url_add_face_id,data = data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def emptyPerson(self,person_id):
        '''
        #清空Person实例与Face的关联关系，不会删除Face实例
        :param person_id:
        :return:
        '''
        try:
            http_url_empty_person = self.__http_url + '/people/empty'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'person_id': person_id
            }
            repResult = requests.post(http_url_empty_person, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def removeFace(self,person_id,face_id):
        '''
        #给一个Person实例删除Face
        :param person_id:
        :param face_id:
        :return:
        '''
        try:
            http_url_remove_face = self.__http_url + '/people/remove_face'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'person_id': person_id,
                'face_id': face_id
            }
            repResult = requests.post(http_url_remove_face, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def createGroups(self,person_id,name):
        '''
        #创建Group实例
        :param person_id:
        :param name:
        :return:
        '''
        try:
            http_url_create_groups = self.__http_url + '/groups/create'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'person_id': person_id,
                'name': name
            }
            repResult = requests.post(http_url_create_groups, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def deleteGroups(self,group_id):
        '''
        #删除Group实例
        :param group_id:
        :return:
        '''
        try:
            http_url_delete_groups = self.__http_url + '/groups/delete'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'group_id': group_id
            }
            repResult = requests.post(http_url_delete_groups, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def addPersonId(self,person_id,group_id):
        '''
        #Group实例中添加一个Person
        :param person_id:
        :param group_id:
        :return:
        '''
        try:
            http_url_add_person = self.__http_url + '/groups/add_person'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'person_id':person_id,
                'group_id': group_id
            }
            repResult = requests.post(http_url_add_person, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def emptyGroups(self,group_id):
        '''
        #清空Group与Person的关联关系，不会删除Person实例
        :param group_id:
        :return:
        '''
        try:
            http_url_empty_groups = self.__http_url + '/groups/empty'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'group_id': group_id
            }
            repResult = requests.post(http_url_empty_groups, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None


    def removePerson(self, person_id, group_id):
        '''
        #Group实例中删除一个Person
        :param person_id:
        :param group_id:
        :return:
        '''
        try:
            http_url_remove_person = self.__http_url + '/groups/remove_person'
            data = {
                'api_id': self.__api_id,
                'api_secret': self.__api_secret,
                'person_id': person_id,
                'group_id': group_id
            }
            repResult = requests.post(http_url_remove_person, data=data)
            return repResult.json(),float(repResult.elapsed.microseconds)/1000
        except:
            return None








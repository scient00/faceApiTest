#!/usr/bin/python
# -*- coding: utf-8 -*-

# 矩形框坐标信息
class Rect:
    def __init__(self,x = 0.0,y = 0.0,width = 0.0,height = 0.0):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
    def __repr__(self):
        return 'x='+str(self.__x) + ' y='+str(self.__y)+ ' width='+str(self.__width)+ ' height='+str(self.__height)
    def set(self,x,y,width,height):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def getWidth(self):
        return self.__width
    def getHeight(self):
        return self.__height
    def toTuple(self):
        return self.__x,self.__y,self.__width,self.__height
    def toIntArr(self):
        oRect = (c_int * 4)()
        oRect[0] = self.__x
        oRect[1] = self.__y
        oRect[2] = self.__width
        oRect[3] = self.__height
        return oRect
    def toString(self):
        return 'x=',self.__left,'y=',self.__top,'width=',self.__width,'height=',self.__height

class Point:
    def __init__(self,x,y):
        self.__x = x
        self.__y = y
    def set(self,x,y):
        self.__x = x
        self.__y = y
    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def toString(self):
        return 'x=',self.__x,'y=',self.__y
    def toTuple(self):
        return self.__x,self.__y

class Landmarks:
    def __init__(self):
        self.__size = 0
        self.__vPoint = []
    def add(self,point):
        self.__size += 1
        self.__vPoint.append(point.toTuple())
    def getSize(self):
        return self.__size
    def getPoint(self,index):
        return Point(self.__vPoint[index][0],self.__vPoint[index][1])

class DeteOut:
    def __init__(self,rect,landmarks,age,gender,yaw,roll,pitch,imageWidth,imageHeight,face_id,image_id):
        self.__rect = rect
        self.__landmarks = landmarks
        self.__age = age
        self.__gender = gender
        self.__yaw = yaw
        self.__roll = roll
        self.__pitch = pitch
        self.__imageWidth = imageWidth
        self.__imageHeight = imageHeight
        self.__face_id = face_id
        self.__image_id = image_id
    def set(self,rect,landmarks,age,gender,yaw,roll,pitch,imageWidth,imageHeight,face_id,image_id):
        self.__rect = rect
        self.__landmarks = landmarks
        self.__age = age
        self.__gender = gender
        self.__yaw = yaw
        self.__roll = roll
        self.__pitch = pitch
        self.__imageWidth = imageWidth
        self.__imageHeight = imageHeight
        self.__face_id = face_id
        self.__image_id = image_id
    def getRect(self):
        return self.__rect
    def getLandmarks(self):
        return self.__landmarks
    def getAge(self):
        return self.__age
    def getGender(self):
        return self.__gender
    def getYaw(self):
        return self.__yaw
    def getRoll(self):
        return self.__roll
    def getPitch(self):
        return self.__pitch
    def toString(self):
        return 'rect=',self.__rect,'landmarks=',self.__landmarks,'age=',self.__age,'gender=',self.__gender,'yaw=',self.__yaw,'roll=',self.__roll,'pitch=',self.__pitch,'imageWidth=',self.__imageWidth,'imageHeight=',self.__imageHeight, 'face_id=',self.__face_id,'image_id=',self.__image_id
    def toTuple(self):
        return self.__rect,self.__landmarks,self.__age,self.__gender,self.__yaw,self.__roll,self.__pitch,self.__imageWidth,self.__imageHeight, self.__face_id,self.__image_id

class vDeteOut:
    def __init__(self):
        self.__size = 0
        self.__vOut = []
    def add(self,deteOut):
        self.__size += 1
        self.__vOut.append(deteOut.toTuple())
    def getSize(self):
        return self.__size
    def getDete(self,index):
        return DeteOut(self.__vOut[index][0],self.__vOut[index][1],self.__vOut[index][2],self.__vOut[index][3],self.__vOut[index][4],self.__vOut[index][5],self.__vOut[index][6],self.__vOut[index][7],self.__vOut[index][8],self.__vOut[index][9],self.__vOut[index][10])

class VerificationOut:
    def __init__(self,same_person,confidence,face_id,person_id):
        self.__same_person = same_person
        self.__confidence = confidence
        self.__face_id = face_id
        self.__person_id =person_id
    def set(self,same_person,face_id,person_id):
        self.__same_person = same_person
        self.__face_id = face_id
        self.__person_id =person_id
    def getSamePerson(self):
        return self.__same_person
    def getConfidence(self):
        return self.__confidence
    def getFaceId(self):
        return self.__face_id
    def getPersonId(self):
        return self.__person_id
    def toString(self):
        return 'same_person=',self.__same_person,'confidence=',self.__confidence,'face_id=',self.__face_id,'person_id=',self.__person_id

class Candidates:
    def __init__(self,person_id,name,confidence,register_face_id,register_person_id,register_image_url):
        self.__person_id = person_id
        self.__name = name
        self.__confidence = confidence
        self.__register_face_id = register_face_id
        self.__register_person_id = register_person_id
        self.__register_image_url = register_image_url
    def set(self,person_id,name,confidence,register_face_id,register_person_id,register_image_url):
        self.__person_id = person_id
        self.__name = name
        self.__confidence = confidence
        self.__register_face_id = register_face_id
        self.__register_person_id = register_person_id
        self.__register_image_url = register_image_url
    def getPersonId(self):
        return self.__person_id
    def getName(self):
        return self.__name
    def getConfidence(self):
        return self.__confidence
    def getRegisterFaceId(self):
        return self.__register_face_id
    def getRegisterPersonId(self):
        return self.__register_face_id
    def getRegisterImageUrl(self):
        return self.__register_image_url
    def toString(self):
        return 'person_id=',self.__person_id,'name=',self.__name,'confidence=',self.__confidence,'register_face_id=',self.__register_face_id,'register_person_id=',self.__register_person_id,'register_image_url=',self.__register_image_url
    def toTuple(self):
        return self.__person_id, self.__name, self.__confidence, self.__register_face_id, self.__register_person_id, self.__register_image_url

class vCandidates:
    def __init__(self):
        self.__size = 0
        self.__vOut = []
    def add(self,candidates):
        self.__size += 1
        self.__vOut.append(candidates.toTuple())
    def getSize(self):
        return self.__size
    def getCandidates(self,index):
        return Candidates(self.__vOut[index][0],self.__vOut[index][1],self.__vOut[index][2],self.__vOut[index][3],self.__vOut[index][4],self.__vOut[index][5])
    def toString(self):
        return self.__vOut

class IdentificationOut:
    def __init__(self,face_id,vcandidates):
        self.__face_id = face_id
        self.__candidates = vcandidates
    def set(self,face_id,vcandidates):
        self.__face_id = face_id
        self.__candidates = vcandidates
    def getFaceId(self):
        return self.__face_id
    def getIdentification(self):
        return self.__candidates

class ImageIdentification(DeteOut):
    def __init__(self,deteOut,image_url,group_id,vcandidates):
        self.__deteOut = deteOut
        self.__image_url = image_url
        self.__group_id = group_id
        self.__vcandidates = vcandidates
    def set(self,deteOut,image_url,group_id,vcandidates):
        self.__deteOut = deteOut
        self.__image_url = image_url
        self.__group_id = group_id
        self.__vcandidates = vcandidates
    def getImageUrl(self):
        return self.__image_url
    def getGroupId(self):
        return self.__group_id
    def toString(self):
        return 'image_url=',self.__image_url,'group_id=',self.__group_id,self.__deteOut.toString(),self.__vcandidates.toString()


class faceIdOut:
    def __init__(self,person_id,name,face_count):
        self.__person_id = person_id
        self.__name = name
        self.__face_count = face_count
    def set(self,person_id,name,face_count):
        self.__person_id = person_id
        self.__name = name
        self.__face_count = face_count
    def getPersonId(self):
        return self.__person_id
    def getName(self):
        return self.__name
    def getFaceCount(self):
        return self.__face_count
    def toString(self):
        return 'person=',self.__person,'name=',self.__name,'face_count=',self.__face_count

class personIdOut:
    def __init__(self,person_id,name,person_count):
        self.__person_id = person_id
        self.__name = name
        self.__person_count = person_count
    def set(self,person_id,name,person_count):
        self.__person_id = person_id
        self.__name = name
        self.__person_count = person_count
    def getPersonId(self):
        return self.__person_id
    def getName(self):
        return self.__name
    def getPersonCount(self):
        return self.__person_count
    def toString(self):
        return 'person=',self.__person,'name=',self.__name,'person_count=',self.__person_count



















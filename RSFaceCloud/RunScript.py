#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging,datetime,sys,os,shutil,yaml,string
from openpyxl import *
from RSFaceCloud.RSfaceClientCloud import RSFace
from RSFaceCloud.RSfaceOut import *
from RSFaceCloud.RSThread import *
from RSFaceCloud.RSProcess import *
from BasicMethod.BasicMethod import *
from RSFaceCloud.RSConcurrentInput import *

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

def PartitionSample(samefile,multiNum):
    '''
        :param samefile:输入样本列表文件
        :param multiNum:划分的样本分数
        :return:
    '''
    try:
        with open(samefile,'r') as file:
            AllData = file.readlines()
            out = []
            num = int(len(AllData)/multiNum)
            rem = int(len(AllData)%multiNum)
            for k in range(0,multiNum):
                outTemp = []
                for z in range(0,num):
                    outTemp.append(AllData[k*num + z].split('\n')[0].split('\r')[0])
                if(k==multiNum-1):
                    for x in range(0, rem):
                        outTemp.append(AllData[num * multiNum + x].split('\n')[0].split('\r')[0])
                out.append(outTemp)
            return out
    except:
        return None

def MultiTest(multiNum,samefile,host,appid,appsecret,type = True):
    '''
        :param multiNum: 启动的线程数或者进程数
        :param samefile: 输入样本列表文件
        :param host: url+post
        :param appid:
        :param appsecret:
        :param type: type=True表示多进程运行,type=False表示多线程运行
        :return:并发数，总耗时，测试数据详细见dataStatistics()
    '''
    try:
        try:
            shutil.rmtree(TMP_PATH)
        except:
            logging.warning('delete tmp failed!!!')
        data_statistics = vStatisticsData()
        processSample = PartitionSample(samefile, multiNum)
        multiArray = []

        startTime = datetime.datetime.now()
        for k in range(0, multiNum):
            rsInput = RsInput(k, processSample[k],host,appid,appsecret)
            if type == True:
                rsMultiArray = RsFaceProcesses(rsInput)
            if type == False:
                rsMultiArray = RsFaceThread(rsInput)
            rsMultiArray.start()
            multiArray.append(rsMultiArray)

        # 等待所有进程或线程结束
        for end in multiArray:
            end.join()
            if type == False:
                data_statistics.dete.add(end.getDataStatistics().dete)
                data_statistics.recogntion.add(end.getDataStatistics().recogntion)
        endTime = datetime.datetime.now()
        multiTotalTime = float((endTime-startTime).microseconds*1./1000)

        if type == True:
            #多进程模式读取中间数据
            with open(TMP_PATH + '/processdata.ly', 'r') as rfile:
                for dataLine in rfile.readlines():
                    value = dataLine.split()
                    data_statistics.dete.add(statisticsData( int(value[0]), int(value[1]), float(value[2])) )
                    data_statistics.recogntion.add(statisticsData(int(value[3]), int(value[4]), float(value[5])))

        print('dete:: ', data_statistics.dete.toString())
        print('recognition: ', data_statistics.dete.toString())

        writeTmpData(multiNum, multiTotalTime, data_statistics, './TestResult',type)
        print("Exiting Main Thread")
        return multiNum,multiTotalTime,data_statistics
    except:
        logging.error('MultiTest')
        return 0,0.0,dataStatistics()

def BatchMultiTest(vSampleList,host,appid,appsecret,type = True):
    '''
    :param vSampleList: 样本文件路径列表
    :param host:
    :param appid:
    :param appsecret:
    :return:
    '''
    try:
        TestResult = []
        vMultiNum = readConfFile()
        for samefile in vSampleList:
            for multiNum in vMultiNum:
                outResult = MultiTest(multiNum, samefile, host, appid, appsecret,type)
                TestResult.append(outResult)
            writeExcelReports(TestResult)
    except:
        logging.error('BatchMultiTest error!!!')

def readConfFile(confpath = 'config/IputSetting.yaml'):
    '''
    # 读取配置文件(启动的线程或者进程数量)
    :param confpath:
    :return:
    '''
    try:
        with open(confpath,'r') as cofile:
            conf = yaml.load(cofile)
        return conf.get('MULTI_THREAD_PROCESS_ARRAY')
    except:
        return []

def writeTmpData(multiNum,multiTotalTime,data_statistics = vStatisticsData(),fpath='./TestResult',type =True):
    '''
    #写入中间数据
    :param multiNum:
    :param multiTotalTime:
    :param data_statistics:
    :param fpath:
    :return:
    '''
    try:
        CreateFolder(fpath)
        outfResult = fpath + os.path.sep + '.tmpResult.ly'
        with open(outfResult, 'a') as datafile:
            if type == True:
                datafile.write("启动的进程数:\t" + str(multiNum) + '\n')
            if type == False:
                datafile.write("启动的线程数:\t" + str(multiNum) + '\n')
            datafile.write("总耗时:\t" + str(multiTotalTime) + 'ms\n')
            datafile.write('检测结果:'+data_statistics.dete.toString())
            datafile.write('识别结果'+data_statistics.recogntion.toString())



            datafile.write('\n\n')
    except:
        logging.error('writeTmpData error!!!')

def writeExcelReports(TestResult,excelpath='./TestResult'):
    '''
    # 生成Excel报表
    :param excelpath:
    :return:
    '''
    try:
        data_statistics = vStatisticsData()

        dictLetter = list(string.ascii_uppercase)
        vMultiNum = readConfFile()
        setDataList = [u'并发数',u'总耗时',u'请求检测成功率',u'请求识别成功率',u'成功检测请求平均响应耗时',u'成功识别请求平均响应耗时']
        if not os.path.exists(excelpath):
            os.makedirs(excelpath)

        excelfile = excelpath + os.path.sep + str(datetime.datetime.now().date()) + '_TestResult.xlsx'
        wb = Workbook()
        sheet = wb.active
        sheet.title = u'检测与识别'
        row = 2 + len(vMultiNum) +2
        cols = len(['NO'] + setDataList)

        sheet.merge_cells('A1:%s1' % dictLetter[cols])
        sheet.cell(row=1, column=1, value=u'检测与识别')

        for k,indexName in enumerate(['NO'] + setDataList):
            sheet.cell(row=2, column=k + 1, value=indexName)

        for k,data in enumerate(TestResult):
            sheet.cell(row=k + 3, column=1, value=str(k+1))
            sheet.cell(row=k + 3, column=2,value= data[0])
            sheet.cell(row=k + 3, column=3, value=data[1])

            sheet.cell(row=k + 3, column= 4, value=data_statistics.dete.getSucccessRate() )
            sheet.cell(row=k + 3, column= 5, value=data_statistics.recogntion.getSucccessRate() )
            sheet.cell(row=k + 3, column= 6, value=data_statistics.dete.getAverageTime())
            sheet.cell(row=k + 3, column= 7, value=data_statistics.recogntion.getAverageTime())

        outInfo = u'请求检测成功率:成功检测次数/请求检测总次数\n'
        outInfo += u'请求识别成功率:成功识别次数/请求识别总次数\n'
        outInfo += u'成功检测请求平均响应耗时:成功检测请求响应总耗时/成功检测次数\n'
        outInfo += u'成功识别请求平均响应耗时:成功识别请求响应总耗时/成功识别次数\n'

        sheet.merge_cells('A%d:%s%d' % (row, dictLetter[cols-1], row + 4))
        sheet.cell(row=row, column=1, value=outInfo)
        wb.save(excelfile)

    except:
        logging.error('writeExcelReports error!!!')

def TestExample(host,appid,appsecret):
    '''
    #接口调用示例
    '''
    try:
        RsFace = RSFace(host, appid, appsecret)
        result = RsFace.detect('test.jpg')
        face_id = result[0]['faces'][0]['face_id']
        print('detect', result)

        result = RsFace.createPersonId(face_id, 'readsense')
        print('createPersonId', result)
        person_id = result[0]['person_id']

        result = RsFace.deletePersonId(person_id)
        print('deletePersonId', result)

        person_id = '5366fa2c96e81cdb41bc05ebf43881d7'

        result = RsFace.addFaceId(face_id, person_id)
        print('addFaceId', result)

        # result = RsFace.emptyPerson(person_id)
        # print('emptyPerson',result)

        result = RsFace.verificationByfaceId(face_id, face_id)
        print('verificationByfaceId', result)

        result = RsFace.verificationBypersonid(face_id, person_id)
        print('verificationBypersonid', result)

        result = RsFace.removeFace(person_id,face_id)
        print('removeFace',result)

        result = RsFace.createGroups(person_id, 'RsGroups')
        print('createGroups', result)
        groupsId = result[0]['group_id']
        # result = RsFace.deleteGroups(groupsId)
        # print('deleteGroups',result)

        result = RsFace.imageIdentification('test.jpg',groupsId)
        print('imageIdentification',result)

        result = RsFace.addPersonId(person_id, groupsId)
        print('addPersonId', result)
        result = RsFace.emptyGroups(groupsId)
        print('emptyGroups', result)

        result = RsFace.removePerson(person_id, groupsId)
        print('removePerson', result)

        result = RsFace.identification(face_id, person_id)
        print('identification', result)
    except:
        logging.error('TestExample')





















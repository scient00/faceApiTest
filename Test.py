#!/usr/bin/python
# -*- coding: utf-8 -*-

from RSFaceCloud.RunScript import *
import sys,logging,os,datetime


if len(sys.argv) <= 1:
    host = 'http://114.80.100.146:3002'
    appid = 'b2268f0901893d4f8d5c7f123c602712'
    appsecret = '22c5334624496bdec437945d3e43deb10616f430'
    # host = 'http://120.79.151.3:8011'
    # appid = 'f6f96cec55e5a9823c6115ddcad6ff80'
    # appsecret = 'cc4c90231dd9e6b970fdd8d385e7a782b2bd9f59'
    multiNum = 1
    samefile = 'F:/00_TestSample/samplePath/windows/test.ly'
    vSampleList = ['F:/00_TestSample/samplePath/windows/test.ly'] #Allface
    type = 1
else:
    try:
        print('\t参数1：Url地址(IP+端口)\n'
              '\t参数2：AppId\n'
              '\t参数3：AppSecret\n'
              '\t参数4：启动进程数或者线程数\n'
              '\t参数5：样本文件列表路径\n'
              '\t参数6：0启动多线程,1启动多进程\n')
        host = sys.argv[1]
        appid = sys.argv[2]
        appsecret = sys.argv[3]
        multiNum = int(sys.argv[4])
        vSampleList = [sys.argv[5]]
        type = int(sys.argv[6])
    except:
        logging.error('参数输入错误!!!')
        sys.exit()

if __name__ == '__main__':
    #TestExample(host, appid, appsecret)
    #MultiTest(multiNum, samefile, host, appid, appsecret,type)
    BatchMultiTest(vSampleList, host, appid, appsecret,type)


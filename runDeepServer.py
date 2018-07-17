#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os,sys,datetime,time

port =[9087,9088]

if len(sys.argv) <= 1:
    runscript = 'DeepFaceServer_20180708.bin'
    runType = 1
    gpuType = 1
    appId = '0e4773c50dac1145d3d148da71555c31'
else:
    try:
        print('参数1：启动可执行文件\n'
              '参数2：类型，1表示启动，0表示停止\n'
              '参数3：模型，1表示GPU模型，0表示CPU模型\n'
              '参数4：gpu_device_id，可通过nvidia-smi查看\n'
              '参数5：AppId\n')
        runscript = sys.argv[1]
        runType = int(sys.argv[2])
        if runType == 1:
            gpuType = int(sys.argv[3])
            appId = sys.argv[4]
    except:
        print('参数不匹配！')
        sys.exit()

def writeCfgFile(appId,port,gpuType = 1,cfgname ='config/deepreadsense.cfg' ):
    try:
        fname = cfgname.split('/')[0]
        if not os.path.exists(fname):
            os.mkdir(fname)
        logfile = 'log/readfaceserver_'+ str(port)+'.log'
        pidfile = 'pids/deepface_'+ str(port)+'.pid'
        port = port
        backend = gpuType  # 1: gpu 0: cpu
        device_id = 0
        daemon = 1
        with open(cfgname,'w') as file:
            file.write('app_id='+appId + '\n')
            file.write('logfile='+logfile + '\n')
            file.write('pidfile='+pidfile + '\n')
            file.write('port=' + str(port) + '\n')
            file.write('backend=' + str(backend) + '\n')
            file.write('device_id=' + str(device_id) + '\n')
            file.write('daemon=' + str(daemon) + '\n')
            file.flush()
        return 0
    except:
        print(str(datetime.datetime.now())+': ' + 'writeCfgFile error!')
        return -1

def startUp(appId,runscript,ports,gpuType = 1):
    try:

        command = 'chmod a+x ' + runscript
        if os.system(command) != 0:
            return None

        for index, port in enumerate(ports):
            cfgname = 'config/deepreadsense_' + str(port) + '.cfg'
            if writeCfgFile(appId,port,gpuType =gpuType ,cfgname = cfgname) != 0:
                return None
            command = './' + runscript + ' -c ' + cfgname
            result = os.popen(command).readlines()
            if len(result) == 0:
                print('The startup files was not found!')
                return None
            time.sleep(3)
            command = 'ps -ef|grep ' + cfgname
            result = os.popen(command).readlines()
            if len(result) == 0:
                print(str(datetime.datetime.now())+': ' + '[port=%d] Service startup failed!' % port)
            else:
                print(str(datetime.datetime.now()) + ': ' + '[port=%d] Service startup success!' % port )

    except:
       print(str(datetime.datetime.now())+': ' +'Service startup error!')

def killUp(runscript):
    try:
        command = 'ps -ef|grep ' + runscript
        result = os.popen(command).readlines()
        if len(result) == 0:
            print('No process found!')
            return None
        for name in result:
            if name.find(runscript) != -1:
                pid = int(name.split()[1])
                if os.system('kill -9 ' + str(pid))==0:
                    print(str(datetime.datetime.now())+': ' +'kill %d success'% pid)
    except:
        print(str(datetime.datetime.now())+': ' +'Stop service error!')


if __name__ == '__main__':
    if runType == 1:
        startUp(appId,runscript,port,gpuType)
    elif runType == 0:
        killUp(runscript)
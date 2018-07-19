#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os,logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

def kill():
    try:
        command = 'ps -ef|grep Test.py'
        result = os.popen(command).readlines()
        if len(result) == 0:
            print('未找到启动脚本')
            return None
        for name in result:
            if name.find('python') != -1:
                pid = int(name.split()[1])
                if os.system('kill -9 ' + str(pid))==0:
                    print('kill %d success'% pid)
    except Exception as ex:
       logging.exception(ex)

if __name__ == '__main__':
    kill()

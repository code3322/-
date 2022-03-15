#!/usr/bin/env python
#encoding: utf-8

#-------------------------------------------------------------------------
#头文件
from core_code.scan_core import sec_scan
import time


#-------------------------------------------------------------------------
#全局变量


#-------------------------------------------------------------------------
#类、函数声明与定义
@sec_scan.task
def mass_scan(ip=None, port_list=None, args=None):
    time.sleep(1)
    print('ip: %s, port list: %s, args: %s' % (ip, port_list, args))
    return 'scan start...'

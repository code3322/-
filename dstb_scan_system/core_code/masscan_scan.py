#!/usr/bin/env python
#encoding: utf-8

#-------------------------------------------------------------------------
#头文件
from core_code.scan_core import sec_scan
import time
import masscan


#-------------------------------------------------------------------------
#全局变量


#-------------------------------------------------------------------------
#类、函数声明与定义
@sec_scan.task
def mass_port_scan(ip=None, port_list='1-65535', args='-n -pn --rate 1000'):
    mass = masscan.PortScanner()
    scan_result = mass.scan(ip, ports=port_list, arguments=args)

    result = []
    for key in scan_result['scan'][ip]['tcp'].keys():
        state = scan_result['scan'][ip]['tcp'].get(key)['state']
        if ('open' == state):
            result.append(key)

    if len(result):
        result.insert(0, ip)
    else:
        fail_result = ip + 'All ports is closed'
        return  fail_result

    return result
        
        

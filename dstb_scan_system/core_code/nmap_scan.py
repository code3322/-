#!/usr/bin/env python
#encoding: utf-8

#-------------------------------------------------------------------------
#头文件
from core_code.scan_core import sec_scan
import time
import nmap
import json
import pymysql
import datetime


#-------------------------------------------------------------------------
#全局变量
# mysql数据库连接信息
MysqlHost = '127.0.0.1'
MysqlUser = 'user'
MysqlPwd = 'pwd'
MysqlDBName = 'xxxx'


#-------------------------------------------------------------------------
#类、函数声明与定义
@sec_scan.task
def nmap_service_detect(ip=None, port_list=None, args="-sS -n -sV"):
    #显示一下传过来的参数,调试用
    #print('ip: %s, port list: %s, args: %s' % (ip, port_list, args))

    #执行Nmap并进行扫描
    nm = nmap.PortScanner()
    nm.scan(ip, port_list, args)
    
    #显示被扫描的ip列表,调试用
    #print(nm.all_hosts())

    #显示被扫描的端口列表,调试用
    #print(nm[ip].all_tcp())

    #端口列表排序
    lport = nm[ip].all_tcp()
    lport.sort()

    #分析端口的服务版本信息
    result_list = []
    result_list.append(ip)
    for line in lport:
        if nm[ip].tcp(line)['state'] == 'open':
            #print('ip: %s, port: %d, info: %s, vesion: %s %s' % (ip, line, nm[ip].tcp(line)['name'], nm[ip].tcp(line)['product'], nm[ip].tcp(line)['version']))
            info_dict = {}
            info_dict['port'] = line
            info_dict['info'] = str(nm[ip].tcp(line)['name'])
            info_dict['version'] = str(nm[ip].tcp(line)['product']) + str(nm[ip].tcp(line)['version'])
            result_list.append(info_dict)

    #分析结果, 新数据就入库, 这里可以不用执行, 因为消息中间件已经存储结果,mysql插入数据比较慢, 这里会拖慢进度, 比较懒就另当别论
    if len(result_list) != 0:
        detect_data_isnew_tmp = "select count(*) from scan_result where ip='%s' and port = %d"
        i = 1
        while i < len(result_list):
            detect_sql = detect_data_isnew_tmp % (ip, result_list[i]['port'])
            detect_data = sql_exec(detect_sql, return_data=True)
            if not detect_data[0][0]:
                insert_sql_tmp = "insert into scan_result(ip, port, servicename, version, tasktype, submitter, flags) value('%s', '%d', '%s', '%s', '%s', '%s', '%d')"
                insert_sql = insert_sql_tmp % (ip, result_list[i]['port'], result_list[i]['info'], result_list[i]['version'], 'person', 'xxx', 0)
                sql_exec(insert_sql, return_data=False)
            i += 1

        return result_list


#把结果插入数据库
def sql_exec(sql=None, return_data=False):
    '''执行mysql 语句'''
    conn = pymysql.connect(host=MysqlHost, user=MysqlUser, passwd=MysqlPwd, db=MysqlDBName, port=3306, charset="utf8", connect_timeout=10)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    
    data = cursor.fetchall()
    if return_data:
        return data
    else:
        pass
    
    conn.close()

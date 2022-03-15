#!/usr/bin/env python
#encoding: utf-8


#-------------------------------------------------------------------------
#头文件
import logging
import time
import sys
import datetime
from core_code.masscan_scan import mass_port_scan
from celery.result import AsyncResult
from core_code.nmap_scan import nmap_service_detect


#-------------------------------------------------------------------------
#全局变量
#扫描ip来源, 可为mysql、file、cmdb
#mysql<暂时没实现，后续实现>
MysqlHost = '127.0.0.1'
MysqlUser = 'xxxx'
MysqlPwd = 'xxxx'
MysqlDB = 'xxxx'

#file
ipListName = 'ip.txt'

#运行时日志文件名
logFile = 'error.log'

#运行时日志级别
log_level = 'logging.DEBUG'

#默认要扫描的端口列表,精选经常被用到的业务组件对应的端口,也可以改ip.txt里面的第二个字段
scan_ports = '21,22,23,992,25,53,88,110,111,80,443,135,137,138,139,161,389,636,445,512,873,1025,1433,1723,1512,2049,2181,2375,3128,3306,3389,3690,4899,5432,5631,5900,6379,7001,7002,8000,8012,8069,8080,8649,9043,9200,9300,10250,11211,27017,50000,50070,50075,50090'

#mass默认参数,没事也别改,因为过滤数据时可能会出错,也可改ip.txt里面的第三个字段
mass_arg = '-n -Pn --rate 1000'

#任务成功计数,有需要可导出到看板
success_num = 0

#任务失败计数,有需要可导出到看板
fail_num = 0

#本次要扫描的总ip数
count_num = 0

#是否需要调用nmap来认别服务,mass扫描结果保存的消息中间件,nmap的结果保存在mysql
Nmap_Service_Scan_Trun = True


#-------------------------------------------------------------------------
#类、函数声明与定义
def exec_mass_task(src=None):
    '''执行任务,src表来ip的来源, 可为mysql、cmdb、文本(file)'''
    if src == 'file':
        exec_src_file() 
    elif src == 'mysql':
        '''后续实现'''
        pass
    elif src == 'cmdb':
        '''后续实现'''
        pass
    else:
        sys.exit(0)


def exec_src_file(portlist=None, arg=None):
    '''从文本读取ip并执行,扫描的端口与参数即可用全局变量定义的,也可依实际情况改ip.txt中的格式'''
    task_list = []
    with open(ipListName) as FileOjb:
        for line in FileOjb:
            global count_num
            count_num += 1
            #处理扫描参数
            final_ip = line.split("#")[0].strip()
            final_ports = line.split("#")[1].strip()
            if len(final_ports) == 0:
                final_ports = scan_ports
            final_args = line.split("#")[2].strip()
            if len(final_args) == 0:
                final_args = mass_arg

            #print('ip: %s, ports: %s, args: %s' % (final_ip, final_ports, final_args))
            result = mass_port_scan.delay(final_ip, final_ports, final_args)

            #把执行id存储起来, 用于状态的判断
            ip_dict = {}
            ip_dict['ip'] = final_ip
            ip_dict['task_id'] = str(result.id)
            ip_dict['status'] = str(result.status)
            task_list.append(ip_dict)

    #判断任务的状态,如果成功,调用nmap执行服务认识, 如果失败进行记录
    while True:
        time.sleep(5) 
        #获取任务的结果
        for line in task_list:
            get_ret = AsyncResult(line['task_id'])
            if get_ret.successful():
                global success_num
                success_num += 1
                tmp = get_ret.get()

                #传给Nmap函数扫描的函数
                nmap_scan_ip = str(tmp[0]).strip()
                nmap_scan_ports = str(tmp[1:]).strip()

                #masscan任务执行成功, 接着可调用nmap来认识服务
                if Nmap_Service_Scan_Trun:
                    nmap_result = nmap_service_detect.delay(nmap_scan_ip, nmap_scan_ports)

                #任务执行成功,结果已经获取,不需要再循环查看,从获取队列中删除此任务
                task_list = [item for item in task_list if not item['task_id'] == line['task_id']]
            elif get_ret.failed():
                global fail_num 
                fail_num += 1
                #任务执行失败,结果已经获取,不需要再循环查看,从获取队列中删除此任务
                task_list = [item for item in task_list if not item['task_id'] == line['task_id']]

        if len(task_list) == 0:
            break

    print('The Tasks have: %d' % (count_num))
    print('Success scan: %d' % (success_num))
    print('Fail scan: %d' % (fail_num))



def exec_src_mysql():
    '''从mysql中读取ip并执行, 后续实现'''
    pass

def exec_src_cmdb():
    '''从cmdb读取ip并执行, 后续实现'''
    pass


#-------------------------------------------------------------------------
#主函数
if __name__ == '__main__':
    '''程序运行时的msg'''
    starttime = datetime.datetime.now()
    print('-------------------------------------------------------------------------')
    print('程序将很快执行，现在时间是:',starttime.strftime('%Y-%m-%d %H:%M:%S'))
    print('如遇异常，请查看当前目录下的日志文件 error.log')
    print('正在进行程序初始化, 请稍等.....')
    print('')


    #运行时日志设置
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handle = logging.FileHandler(logFile, mode='a+')
    handle.setLevel(logging.DEBUG)    
    formatter = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)d]  -  %(levelname)s - %(message)s')
    handle.setFormatter(formatter)
    logger.addHandler(handle)


    #核心代码执行
    try:
        #测试任务代码
        #mass_port_scan.delay('61.152.109.30', '22,80,443,3306', '-n -Pn')
        
        #执行代码
        exec_mass_task(src='file') 

    except Exception as e:
        logger.error(str(e), exc_info=True)
        sys.exit(0)


    '''程序运行结束，并显示运行了多久'''
    endtime = datetime.datetime.now()
    seconds = (endtime - starttime).seconds
    print('程序执行完成，一共花费了 %d 秒' % (seconds))
    print('-------------------------------------------------------------------------')

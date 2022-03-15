#!/usr/bin/env python
#encoding: utf-8

#-------------------------------------------------------------------------
#头文件
from celery import Celery


#-------------------------------------------------------------------------
#全局变量


#-------------------------------------------------------------------------
#类、函数声明与定义
#参数include是worker中要处理消息的函数, 需要导出, 导出已经放在scan_config.py中了, 此代码作为参考, core_code为你的项目的名, 也就是目录名, masscan为core_code目录中要执行的python文件名, 导出路径到文件名就行, 不需要连函数名也导出
#sec_scan = Celery("secScan", include = ["core_code.masscan_scan", "core_code.nmap_scan"])

#sec_scan这个是类的对象, 在任务函数中要使用
sec_scan = Celery("secScan") 

#scan_config就是这个这个目录下的scan_config.py文件
sec_scan.config_from_object("core_code.scan_config")


#-------------------------------------------------------------------------
#主函数
#如果不写以下两句, 需要在命令行使用: celery -A core_code.scan_core worker -B -l info 来执行
if __name__ == '__main__':
    sec_scan.start()

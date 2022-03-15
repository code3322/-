#!/usr/bin/env python
#encoding: utf-8

#-------------------------------------------------------------------------
#头文件
from datetime import timedelta
from celery.schedules import crontab


#-------------------------------------------------------------------------
#全局变量
#消息输入的队列, 依情况修改, 此使用redis 0这个库
BROKER_URL = "redis://127.0.0.1:6379/0"

#消息输出的队列, 依情况修改, 使用redis 1这个库
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"

#时区设置
CELERY_TIMEZONE='Asia/Shanghai'

#导出任务, 手动调用、计划任务, 都要导出, 路径只指定到文件名, 里面的函数需要消息发送端来导出并使用
#CELERY_IMPORTS = ('core_code.masscan_scan', 'core_code.nmap_scan', 'core_code.cron_masscan_scan', 'core_code.corn_nmap_scan') 
CELERY_IMPORTS = ('core_code.masscan_scan', 'core_code.nmap_scan')


#定时任务调度器
CELERYBEAT_SCHEDULE={
    #任务名字, 可自定义, 无关联
    'masscan_cron':{
        #任务启动的函数, 指定要具体函数
        'task':'core_code.cron.cron_masscan_scan.mass_scan',
        #定时时间设置，此为每10秒一次
        'schedule':timedelta(seconds=5),
        #传递给函数的参数
        'args':(['127.0.0.1', '1-65535', '-n -pn'])
    },
}

'''
#定时任务调度器, 此为多个任务, 此为参考代码
CELERYBEAT_SCHEDULE={
    #任务名字, 可自定义, 无关联
    'task1':{
        # 任务启动的函数
        'task':'celery_app.task1.add',
        # 定时时间设置，每10秒一次
        'schedule':timedelta(seconds=10),
        # 传递的参数
        'args':(2,8)
    },
    'task2':{
        'task':'celery_app.task2.mul',
        # 定时时间设置，16:45
        'schedule':crontab(hour=16,minute=45),
        'args':(4,5)
    }
}
'''

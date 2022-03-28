### 分布式秒级端口扫描系统

&emsp;&emsp;分布式秒级端口扫描系统，用于快速巡检公司服务器对外的暴露面，此为应对海量服务器!

&emsp;&emsp;项目使用python3 + celery + redis + mysql来实现，具体看部署文档。

&emsp;
### 前提:

&emsp;&emsp;此为分布式端口秒级扫描系统部署文档，秒级扫描系统就是为了以应对海量服务器对外的暴露面，让各位安全大神从此过上没有女朋友的生活！

&emsp;
### 架构

&emsp;&emsp;简单的架构图:
![](/images/arch.jpg)


### 开发环境(仅供参考)
1. 系统: 
    * Debian 10.x x64
    * Centos 7.9 x64

&emsp;&emsp;Debian 10.x 用作消息中间件的承载中心, 也是结果存储的地方, 需要部署python3、pip3、Celery、Redis、Mysql

&emsp;&emsp;Cetos 7.9 只是分布式扫描的一台客户机, 当前用来测试，并与主服务要部署的组件作对比, 客户机只需部署python3、pip3、Celery

2. 使用的组件: 
    * python3<ver: 3.7>
    * pip3<ver: 22.0.4>
    * Celery<ver: 5.2.3 任务调度的组件>
    * Redis<ver: 5.0.14>
    * Mysql<ver: 5.7>

&emsp;
### 部署(注意用到的系统)
* Python3 部署(debian 10.x 与centos 7.9 都适用)

```
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz       //下载python3,国内环境还不如用迅雷下载下来，然后再传服务器
tar zxvf Python-3.7.3.tgz       //解压
cd Python-3.7.3                 //进入这个目录
./configure                     //编译
make && make install            //安装
python3 --version               //显示一下版本
```

* pip3 部署(debian 10.x 与centos 7.9 都适用)

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.for.python3.py   //下载pip3
python3.7 get-pip.for.python3.py   //安装
pip3 --version      //查看一下版本 
```


* Celery 部署(debian 10.x 与centos 7.9 都适用)

```
pip3 install celery	或者 pip3 install "celery[librabbitmq,redis]"            //后续的扫描会改成rabbitmq来作中间件
celery --version   //查看一下版本
```

* Redis 部署(debian 10.x 适用, Centos 7.x 的自己去百度一下)

```
apt-get install redis-server			//安装
systemctl stop redis-server			//停止redis

修改配置文件:
vim redis.conf				        //修改配置文件是让其它服务器能连接过来读写消息队列, 默认配置文件一般在/etc/redis.conf
    a) 修改配置文件redis.conf, 把bind 127.0.0.1 改成bind 0.0.0.0 或者把 bind 127.0.0.1 注释掉
    b) 将protected-mode yes 改为 protected-mode no（3.2之后加入的新特性，目的是禁止公网访问redis cache，增强redis的安全性）

systemctl start redis-server			//开启redis
systemctl enable redis-server			//允许开机启动
systemctl status redis-server			//查看一下状态
```

* Mysql 部署(debian 10.x 适用, Centos 7.x 的自己去百度一下)

```
1. 下载mysql apt源，默认情况下会让你安装最新的mysql
    curl -L -o mysql-apt-config.deb https://dev.mysql.com/get/mysql-apt-config_0.8.16-1_all.deb

2. 修改源, 把里面的8.0改成5.7
    vim /etc/apt/sources.list.d/mysql.list
    deb http://repo.mysql.com/apt/debian/ buster mysql-apt-config
    deb http://repo.mysql.com/apt/debian/ buster mysql-8.0
    deb http://repo.mysql.com/apt/debian/ buster mysql-tools
    #deb http://repo.mysql.com/apt/debian/ buster mysql-tools-preview
    deb-src http://repo.mysql.com/apt/debian/ buster mysql-8.0

3. 更新一下源
    apt-get update

4、配置
dpkg -i mysql-apt-config.deb
    a) 选择 MySQL Server & Cluster（当前默认为：mysql-8.0) 并按 进入
    b) 进入后选择mysql-5.7
    c) 此时，你应该看到 MySQL Server & Cluster（当前选择：mysql-5.7）
    d) 选择倒数第二个ok, 此时配置完成

5、安装
    apt-cache show mysql-server	        //先查一下mysql的版本是否是5.7
    apt-get update				//更新一下源
    apt-get install -y mysql-server		//安装

    mysql -uroot -p         //进入Mysql, 此时你要输入密码
    create database celery  //创建一个库, 用于保存nmap扫描的结果
    exit                    //退出mysql
    mysql -uroot -p celery < nmap_result.sql    //导入表结构, 此时你要输密码
```

&emsp;
<font color=red>以上就是基础环境的部署, 相信有更懒的人会写一键部署脚本，此时你应该写好后再加我, 我也比较懒。</font>


&emsp;
### 配置文件与扫描器参数调整
1、下载代码并上传到你的服务器上, 放哪里随便你们, 我放在/usr/local/src/

&emsp;&emsp;代码下载地址: https://github.com/code3322/PortScan

2、修改配置文件(<font color=red>比较懒的做法就是, redis在哪台服务器就写那台机器的ip</font>),如消息中间件的连接地址, nmap扫描结果要连接的mysql

```
配置消息中间件(依情况修改成你的就好):
    cd /usr/local/src/dstb_scan_system/core_code
    vim scan_config.py
    a) BROKER_URL = "redis://127.0.0.1:6379/0"               //消息输入队列, 使用redis的第一个库, 有密码的按这个格式改: redis://:password@hostname:port/db_number
    b) CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"    //用于保存扫描结果的队列


配置mysql用于保存nmap的扫描结果(依情况修改成你的就好):
    vim nmap_scan.py

    # mysql数据库连接信息
    MysqlHost = '0.0.0.10'
    MysqlUser = 'user'
    MysqlPwd = 'pwd'
    MysqlDBName = 'celery'
```

3、masscan与nmap参数配置(懒得话不用改, 默认够用, 服务器多就改)
```
mass参数(三个地方任选一个, 只是为了方便不同的需求):
1. 第一个地方
    cd /usr/local/src/dstb_scan_system/
    vim port_scan_produce.py            
        scan_ports = '21,22,23'         //修改全局变量即可, 格式 满足masscan格式即可, 因为没有再次对格式进行校验, 改时注意

2.第二个地方
    cd /usr/local/src/dstb_scan_system/core_code/
    vim masscan_scan.py
        def mass_port_scan(....)        //修改函数参数即可

3.第三个地方
    cd /usr/local/src/dstb_scan_system/
    vim ip.txt                  
    ip的格式是这样的(ip + 端口 + masscan参数, 用#号分隔): 
        127.0.0.1#21,22,23#-n -pn
        127.0.0.2#80,443#-n -Pn --rate 2000

nmap参数(nmap只需要改args, 因为它只扫描masscan已经扫描出开放的端口, 且只提取端口与服务版本)
```

&emsp;
<font color=red size=4>ip格式问题, 执行前先看</font>

```
当前只实现了从文件中读取ip并进行扫描, 可实现每个ip都可以调整扫描的端口号与masscan的参数值, 以应对不同需求

    ip的格式是这样的(ip + 端口 + masscan参数, 用#号分隔, 即使使用默认参数也要有两个分隔符): 
    127.0.0.1##
    127.0.0.2#21,22,23#-n -pn
    127.0.0.3#80,443#-n -Pn --rate 2000
```


&emsp;
### 执行
1、先执行那些客户机, 先让他们去消费完堆积的扫描任务
<font color=red>执行的路径是你放代码的路径, 依情况改, 不是照着我给的命令打, 前面已经提及过下载与存放</font>

```
cd /usr/local/src/dstb_scan_system/
celery -A core_code.scan_core worker -l info        //前台执行, 如果需要长期执行, 运行在后台即可, 这样就不用管了
```


2、执行消息队列的生产者(就是有redis服务的那台)

```
cd /usr/local/src/dstb_scan_system/
celery -A core_code.scan_core worker -l info        //前台执行, 如果需要长期执行, 运行在后台即可, 这样就不用管了
```

3、生产ip(在有redis服务的那台机器上再开一个窗口, 如果之前的步骤是后台执行, 那么可用第二步的窗口执行)

```
python3 port_scan_produce.py
```

4、最后等待结果就行
结果保存位置:
* mysql中的celery库中的表scan_result表中
* redis里面也有

&emsp;
### FAQ
部署与执行中的所有问题记录在github, 如出现问题可查看, 如果没有记录到, 请联系我，我去解决并补充到FAQ

FAQ: https://github.com/code3322/PortScan/blob/main/FAQ


&emsp;
### 参考文献
非常原理性的文章：https://blog.csdn.net/kk123a/article/details/74549117                            
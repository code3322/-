### 此为使用秒级扫描系统的FAQ文档，此文件会记录部署中出现的问题

&emsp;
#### 修订记录
| 问题描述 | 记录时间  | 解决时间  | 其它 |
| --: | --: | --: | --: | 
| masscan缺少pcap库 | 2022.3.15 | 2022.3.15 | 安装pcap库解决问题 |
| python3缺少模块<masscan、nmap、pymysql> | 2022.3.15 | 2022.3.15  | 安装相关python模块解决 |

&emsp;
### masscan
<font color=red>1、pcap: failed to load libpcap shared library  HINT: you must install libpcap or WinPcap</font>
&emsp;&emsp;平台: CentOS Linux release 7.9.2009 (Core)
&emsp;&emsp;内核: 3.10.0-1160.59.1.el7.x86_64

解决方法:
```
yum install -y libpcap*

rm -rf masscan				#删除已经下载的masscan
git clone https://github.com/robertdavidgraham/masscan			#下载masscan
cd masscan				#切到masscan目录中
make 					#编译
make install				#安装
```

&emsp;
### Python3
<font color=red>1、ModuleNotFoundError: No module named 'masscan'</font>
&emsp;&emsp;平台: CentOS Linux release 7.9.2009 (Core)
&emsp;&emsp;内核: 3.10.0-1160.59.1.el7.x86_64
	
解决方法:
`pip3 install python-masscan`


<font color=red>2、ModuleNotFoundError: No module named 'pymysql'</font>
&emsp;&emsp;平台: CentOS Linux release 7.9.2009 (Core)
&emsp;&emsp;内核: 3.10.0-1160.59.1.el7.x86_64
	
解决方法:
`pip3 install pymysql`

<font color=red>3、ModuleNotFoundError: No module named 'nmap'</font>
&emsp;&emsp;平台: CentOS Linux release 7.9.2009 (Core)
&emsp;&emsp;内核: 3.10.0-1160.59.1.el7.x86_64
	
解决方法:
`pip3 install python-nmap`

&emsp;
### nmap 

&emsp;
### celery
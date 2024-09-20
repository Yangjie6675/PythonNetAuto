
#>>> 用Python3写一个思科设备网络自动化备份的程序
#**python脚本实现思科设备网络自动化备份**


# -*- coding: utf-8 -*-

import paramiko
import time
from datetime import datetime

# 思科设备登录信息
username = "admin"
password = "passw0rd"

# 思科设备连接列表
devices = {
    'device1': {'ip': '192.168.1.100', 'port': 22},
    'device2': {'ip': '192.168.1.101', 'port': 22}
}

# 日志文件路径
log_path = '/root/logs'

def backup_device(device):
    # 思科设备连接信息
    hostname = device['ip']
    port = device['port']

    try:
        # 连接思科设备
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password, port=port)

        # 获取思科设备的当前时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 生成备份文件名
        backup_file_name = f'syslog_{current_time}.txt'

        # 读取syslog日志并写入backup文件中
        stdin, stdout, stderr = ssh.exec_command('more /noconsoleui logging:Syslog |')
        syslog_data = stdout.read().decode()
        with open(f'{log_path}/{backup_file_name}', 'w') as f:
            f.write(syslog_data)

        # 关闭ssh连接
        ssh.close()

    except paramiko.AuthenticationException:
        print(f'设备{hostname}认证失败!')
    except Exception as e:
        print(f'备份失败：{str(e)}')

if __name__ == '__main__':
    for device in devices.values():
        backup_device(device)

'''**使用步骤**

1.将`username`和`password`替换为您的思科设备登录信息。
2.在`devices`字典中添加您想要备份的设备的ip地址和端口号。
3.将`log_path`路径改成您要存放日志文件的位置。
4.运行脚本，设备将按照上述配置进行自动化备份。

**注意**

* 确保思科设备支持SSH连接，并已安装paramiko库。
* 根据您的具体需求调整日志读取和写入操作，以适应不同的备份策略。
* 确保在生产环境中测试此脚本并进行必要的安全检查以避免意外后果。'''

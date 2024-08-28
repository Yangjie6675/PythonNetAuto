# 实验目的：
# 	使用input()函数和getpass模块实现交互式的SSH用户名和密码输入；
# 	通过for循环同时登录5台交换机SW1~SW5配置vlan10~vlan20。

import paramiko
import time
import getpass

username = input('Username: ')
password = getpass.getpass('Password: ')

for i in range(11,16):
    ip = '192.168.136.' + str(i)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=True)

    print('Successfully connected to ' + ip)

    command = ssh_client.invoke_shell()
    command.send(b'configure terminal\n')
    for n in range(10, 21):
        print('Creating VLAN  ' + str(n))
        command.send('vlan ' + str(n) + '\n')
        command.send('name Python_VLAN ' + str(n) + '\n')
        time.sleep(1)

    command.send(b'end\n')
    command.send(b'write memory\n')
    time.sleep(2)
    output = command.recv(65535)
    print(output.decode('ascii'))

    ssh_client.close()




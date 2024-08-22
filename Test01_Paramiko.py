<<<<<<< HEAD
import paramiko
import time


def backup_device(ip, port, username, password, command, output_file):
    """  
    通过SSH备份网络设备的配置。  

    :param ip: 网络设备的IP地址  
    :param port: SSH端口,默认为22  
    :param username: SSH用户名  
    :param password: SSH密码  
    :param command: 在设备上执行的命令，例如 'show running-config'  
    :param output_file: 保存配置的文件名  
    """
    #  创建一个SSH对象  
    ssh = paramiko.SSHClient()

    # 允许连接不在know_hosts文件中的主机  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接服务器  
        ssh.connect(ip, port, username, password, look_for_keys=False, allow_agent=False)

        # 创建一个SSH会话  
        client = ssh.invoke_shell()

        # 给设备一些时间来响应  
        time.sleep(2)

        # 发送命令  
        client.send(command)

        # 等待命令执行完成  
        time.sleep(2)

        # 接收输出  
        output = client.recv(65535).decode('utf-8')

        # 将输出写入文件  
        with open(output_file, 'w') as f:
            f.write(output)

        print(f"配置已成功保存到 {output_file}")

    except Exception as e:
        print(f"连接或执行命令时出错: {e}")

    finally:
        # 关闭连接  
        ssh.close()

    # 使用示例


=======
import paramiko
import time


def backup_device(ip, port, username, password, command, output_file):
    """  
    通过SSH备份网络设备的配置。  

    :param ip: 网络设备的IP地址  
    :param port: SSH端口,默认为22  
    :param username: SSH用户名  
    :param password: SSH密码  
    :param command: 在设备上执行的命令，例如 'show running-config'  
    :param output_file: 保存配置的文件名  
    """
    #  创建一个SSH对象  
    ssh = paramiko.SSHClient()

    # 允许连接不在know_hosts文件中的主机  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接服务器  
        ssh.connect(ip, port, username, password, look_for_keys=False, allow_agent=False)

        # 创建一个SSH会话  
        client = ssh.invoke_shell()

        # 给设备一些时间来响应  
        time.sleep(2)

        # 发送命令  
        client.send(command)

        # 等待命令执行完成  
        time.sleep(2)

        # 接收输出  
        output = client.recv(65535).decode('utf-8')

        # 将输出写入文件  
        with open(output_file, 'w') as f:
            f.write(output)

        print(f"配置已成功保存到 {output_file}")

    except Exception as e:
        print(f"连接或执行命令时出错: {e}")

    finally:
        # 关闭连接  
        ssh.close()

    # 使用示例


>>>>>>> 32c1d20815e8682e52fbf58a331395ea26e722cb
backup_device('192.168.1.1', 22, 'admin', 'password', 'show running-config\n', 'device_config.txt')
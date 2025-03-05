import pandas as pd
import paramiko
import time

def backup_config(ip, username, password, vendor):
    try:
        # 创建 SSH 对象
        ssh = paramiko.SSHClient()
        # 允许连接不在 know_hosts 文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=ip, port=22, username=username, password=password,look_for_keys=False)
        # 打开一个 Channel 并创建交互式 shell
        shell = ssh.invoke_shell()

        if vendor.lower() == 'huawei':
            # 华为设备配置备份命令
            shell.send('screen-length 0 temporary\n')
            time.sleep(1)
            shell.send('display current-configuration\n')
        elif vendor.lower() == 'cisco':
            # 思科设备配置备份命令
            shell.send('terminal length 0\n')
            time.sleep(1)
            shell.send('show running-config\n')
        else:
            print(f"不支持的厂商型号: {vendor}")
            ssh.close()
            return

        time.sleep(5)  # 等待命令执行完成
        output = shell.recv(65535).decode('utf-8')

        # 保存配置到文件
        with open(f'{ip}_config.txt', 'w', encoding='utf-8') as f:
            f.write(output)

        print(f"设备 {ip} 配置备份成功")
        ssh.close()
    except Exception as e:
        print(f"设备 {ip} 配置备份失败: {e}")

def main():
    # 读取 Excel 文件
    try:
        df = pd.read_excel('device_list.xlsx')
    except FileNotFoundError:
        print("未找到设备清单文件 'device_list.xlsx'")
        return

    # 遍历设备清单
    for index, row in df.iterrows():
        ip = row['IP地址']
        username = row['用户名']
        password = row['密码']
        vendor = row['厂商型号']
        backup_config(ip, username, password, vendor)

if __name__ == "__main__":
    main()
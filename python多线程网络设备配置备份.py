import pandas as pd
import paramiko
from concurrent.futures import ThreadPoolExecutor
import time
import os
import warnings

# 忽略OpenSSL警告
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

def read_devices(excel_file):
    """读取Excel文件中的设备清单"""
    df = pd.read_excel(excel_file)
    devices = df.to_dict('records')
    return devices

def read_commands(txt_file):
    """读取TXT文件中的备份命令"""
    commands = {}
    with open(txt_file, 'r') as f:
        current_vendor = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                vendor, cmd = line.split(':', 1)
                if vendor not in commands:
                    commands[vendor] = []
                commands[vendor].append(cmd)
            else:
                if current_vendor and line:
                    commands[current_vendor].append(line)
    return commands

def backup_device(device, commands_by_vendor):
    """执行单个设备备份"""
    hostname = device['设备名称']
    ip = device['IP地址']
    username = device['用户名']
    password = device['密码']
    vendor = device['厂商']
    
    print(f"Starting backup for {hostname} ({ip})")
    
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, timeout=15)
        
        # 创建交互式shell
        chan = ssh.invoke_shell()
        time.sleep(1)  # 等待会话建立
        
        # 获取设备对应的命令列表
        cmds = commands_by_vendor.get(vendor, [])
        if not cmds:
            print(f"No commands found for {vendor}, skipping {hostname}")
            return

        output = ""
        for cmd in cmds:
            # 发送命令并等待执行
            cmd = cmd.replace('{password}', password)  # 替换密码占位符
            chan.send(cmd + "\n")
            time.sleep(2)  # 根据网络情况调整等待时间
            
            # 读取输出
            while chan.recv_ready():
                output += chan.recv(4096).decode('utf-8', 'ignore')
        
        # 保存备份文件
        backup_dir = 'network_backups'
        os.makedirs(backup_dir, exist_ok=True)
        filename = f"{backup_dir}/{hostname}_{ip}.txt"
        
        with open(filename, 'w') as f:
            f.write(output)
        
        print(f"Backup completed for {hostname} ({ip})")
    
    except Exception as e:
        print(f"Error backing up {hostname}: {str(e)}")
    finally:
        if 'ssh' in locals():
            ssh.close()

def main():
    # 配置文件路径
    devices_file = 'devices.xlsx'
    commands_file = 'commands.txt'
    
    # 读取配置
    devices = read_devices(devices_file)
    commands = read_commands(commands_file)
    
    # 创建线程池（建议5-10个线程）
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for device in devices:
            futures.append(
                executor.submit(
                    backup_device,
                    device=device,
                    commands_by_vendor=commands
                )
            )
        
        # 等待所有任务完成
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Task failed: {e}")

if __name__ == '__main__':
    main()
    
import pandas as pd
import paramiko
import time
import os
from datetime import datetime
import logging
import re
import socket
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='backup.log'
)

class NetworkDevice:
    def __init__(self, name, ip, username, password, vendor):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.vendor = vendor.lower()
        self.ssh = None
        self.backup_dir = "config_backups"
        
    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname=self.ip,
                username=self.username,
                password=self.password,
                timeout=10,
                look_for_keys=False,
                allow_agent=False
            )
            logging.info(f"成功连接到 {self.name}({self.ip})")
            return True
        except paramiko.AuthenticationException:
            logging.error(f"认证失败: {self.name}({self.ip})")
        except (paramiko.SSHException, socket.error) as e:
            logging.error(f"连接失败: {self.name}({self.ip}) - {str(e)}")
        except Exception as e:
            logging.error(f"未知错误: {self.name}({self.ip}) - {str(e)}")
        return False
    
    def disconnect(self):
        if self.ssh:
            self.ssh.close()
            logging.info(f"已断开与 {self.name}({self.ip}) 的连接")
    
    def get_config(self):
        try:
            shell = self.ssh.invoke_shell()
            shell.settimeout(30)
            
            # 根据不同厂商发送不同命令
            if "cisco" in self.vendor:
                shell.send("terminal length 0\n")
                time.sleep(1)
                shell.send("show running-config\n")
            elif "huawei" in self.vendor:
                shell.send("screen-length 0 temporary\n")
                time.sleep(1)
                shell.send("display current-configuration\n")
            elif "h3c" in self.vendor or "hp" in self.vendor:
                shell.send("screen-length disable\n")
                time.sleep(1)
                shell.send("display current-configuration\n")
            elif "juniper" in self.vendor:
                shell.send("set cli screen-length 0\n")
                time.sleep(1)
                shell.send("show configuration\n")
            else:
                logging.warning(f"未知厂商: {self.name}({self.ip}) - 无法获取配置")
                return None
                
            time.sleep(5)  # 等待命令执行完成
            
            # 读取输出
            output = b""
            while True:
                try:
                    if shell.recv_ready():
                        chunk = shell.recv(65535)
                        output += chunk
                        time.sleep(0.5)
                    else:
                        break
                except socket.timeout:
                    break
            
            config = output.decode('utf-8', errors='ignore')
            return config
            
        except Exception as e:
            logging.error(f"获取配置失败: {self.name}({self.ip}) - {str(e)}")
            return None
    
    def save_config(self, config):
        if not config:
            return False
            
        # 创建备份目录
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.backup_dir}/{self.name}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(config)
            logging.info(f"配置已保存到 {filename}")
            return True
        except Exception as e:
            logging.error(f"保存配置失败: {filename} - {str(e)}")
            return False
    
    def backup(self):
        if not self.connect():
            return False
            
        config = self.get_config()
        result = self.save_config(config)
        
        self.disconnect()
        return result

def read_device_list(file_path):
    try:
        df = pd.read_excel(file_path)
        # 检查必要的列是否存在
        required_columns = ['设备名称', 'IP地址', '用户名', '密码', '厂商']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Excel文件缺少必要的列: {col}")
                
        devices = []
        for _, row in df.iterrows():
            device = NetworkDevice(
                name=row['设备名称'],
                ip=row['IP地址'],
                username=row['用户名'],
                password=row['密码'],
                vendor=row['厂商']
            )
            devices.append(device)
            
        logging.info(f"从 {file_path} 成功导入 {len(devices)} 台设备")
        return devices
        
    except Exception as e:
        logging.error(f"读取设备清单失败: {str(e)}")
        return []

def main():
    print("===== 网络设备自动化备份工具 =====")
    file_path = input("请输入Excel设备清单文件路径: ")
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        return
        
    devices = read_device_list(file_path)
    if not devices:
        print("错误: 未能导入任何设备")
        return
        
    total = len(devices)
    success_count = 0
    
    print(f"\n开始备份 {total} 台设备...")
    
    for i, device in enumerate(devices, 1):
        print(f"\n[{i}/{total}] 正在备份: {device.name}({device.ip}) - {device.vendor}")
        result = device.backup()
        
        if result:
            print("✓ 备份成功")
            success_count += 1
        else:
            print("✗ 备份失败")
    
    print(f"\n备份完成! 成功: {success_count}/{total}")
    print(f"详细日志请查看: backup.log")
    print(f"配置文件保存在: {os.path.abspath(device.backup_dir)}")

if __name__ == "__main__":
    main()    
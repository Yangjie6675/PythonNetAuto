import pandas as pd
from netmiko import ConnectHandler, exceptions
import os
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    filename='network_backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 定义厂商配置映射
VENDOR_CONFIG = {
    'cisco_ios': {
        'command': 'show running-config',
        'enable': True
    },
    'huawei': {
        'command': 'display current-configuration',
        'enable': False
    },
    'hp_comware': {
        'command': 'display current-configuration',
        'enable': False
    },
    'juniper_junos': {
        'command': 'show configuration | display set',
        'enable': False
    }
}

def get_vendor_config(vendor_model):
    """根据输入的厂商型号返回对应的配置"""
    vendor_model = vendor_model.lower()
    if 'cisco' in vendor_model:
        return VENDOR_CONFIG['cisco_ios']
    elif 'huawei' in vendor_model:
        return VENDOR_CONFIG['huawei']
    elif 'h3c' in vendor_model or 'hp' in vendor_model:
        return VENDOR_CONFIG['hp_comware']
    elif 'juniper' in vendor_model:
        return VENDOR_CONFIG['juniper_junos']
    else:
        raise ValueError(f"Unsupported vendor/model: {vendor_model}")

def backup_device(device_info, backup_dir):
    """执行单个设备备份"""
    try:
        logging.info(f"Connecting to {device_info['host']}")
        
        with ConnectHandler(**device_info) as conn:
            # 进入特权模式（如果需要）
            if device_info.get('enable', False):
                conn.enable()
            
            # 执行备份命令
            output = conn.send_command(device_info['command'])
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{device_info['host']}_{timestamp}.cfg"
            filepath = os.path.join(backup_dir, filename)
            
            # 保存配置
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output)
            
            logging.info(f"Backup successful for {device_info['host']}")
            return True
            
    except exceptions.NetmikoAuthenticationException:
        logging.error(f"Authentication failed for {device_info['host']}")
    except exceptions.NetmikoTimeoutException:
        logging.error(f"Connection timeout for {device_info['host']}")
    except Exception as e:
        logging.error(f"Error occurred with {device_info['host']}: {str(e)}")
    return False

def main():
    # 创建备份目录
    backup_dir = 'network_backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        # 读取Excel文件
        df = pd.read_excel('devices.xlsx')
        # 转换列名为中文（根据实际情况调整）
        df = df.rename(columns={
            '设备IP地址': 'ip',
            '用户名': 'username',
            '密码': 'password',
            '厂家型号': 'vendor'
        })
    except Exception as e:
        logging.error(f"Failed to read Excel file: {str(e)}")
        return

    # 遍历所有设备
    for _, row in df.iterrows():
        try:
            vendor_config = get_vendor_config(row['vendor'])
        except ValueError as e:
            logging.error(f"Skipping {row['ip']}: {str(e)}")
            continue

        device = {
            'device_type': vendor_config['device_type'],
            'host': row['ip'],
            'username': row['username'],
            'password': row['password'],
            'secret': row.get('enable_password', ''),  # 可选enable密码
            **vendor_config
        }

        backup_device(device, backup_dir)

if __name__ == "__main__":
    main()
    print("Backup process completed. Check network_backup.log for details.")
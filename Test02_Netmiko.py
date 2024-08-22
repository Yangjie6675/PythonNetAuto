<<<<<<< HEAD
from netmiko import ConnectHandler
from datetime import datetime


def backup_device(device):
    """
    使用Netmiko备份网络设备的配置。

    :param device: 一个包含连接信息的字典
    """
    # 尝试连接到设备
    try:
        # 连接到网络设备
        with ConnectHandler(**device) as net_connect:
            # 检查连接是否成功
            print(f"成功连接到 {device['device_type']} 设备 {device['host']}")

            # 获取配置文件
            output = net_connect.send_command('show running-config')

            # 创建一个文件名，包含日期和时间
            filename = f"{device['host']}_config_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

            # 将配置文件写入文件
            with open(filename, 'w') as f:
                f.write(output)

            print(f"配置文件已成功保存到 {filename}")

    except Exception as e:
        print(f"连接或执行命令时出错: {e}")

    #  设备连接信息（请根据你的实际情况修改）


device = {
    'device_type': 'cisco_ios',  # 设备类型，根据Netmiko的文档选择
    'host': '192.168.1.1',  # 设备IP地址
    'username': 'admin',  # SSH用户名
    'password': 'yourpassword',  # SSH密码
    'secret': '',  # 如果需要启用密码，则填写
    'port': 22,  # SSH端口，默认为22
    'verbose': False,  # 是否打印详细信息
}

# 调用函数备份设备配置
=======
from netmiko import ConnectHandler
from datetime import datetime


def backup_device(device):
    """
    使用Netmiko备份网络设备的配置。

    :param device: 一个包含连接信息的字典
    """
    # 尝试连接到设备
    try:
        # 连接到网络设备
        with ConnectHandler(**device) as net_connect:
            # 检查连接是否成功
            print(f"成功连接到 {device['device_type']} 设备 {device['host']}")

            # 获取配置文件
            output = net_connect.send_command('show running-config')

            # 创建一个文件名，包含日期和时间
            filename = f"{device['host']}_config_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

            # 将配置文件写入文件
            with open(filename, 'w') as f:
                f.write(output)

            print(f"配置文件已成功保存到 {filename}")

    except Exception as e:
        print(f"连接或执行命令时出错: {e}")

    #  设备连接信息（请根据你的实际情况修改）


device = {
    'device_type': 'cisco_ios',  # 设备类型，根据Netmiko的文档选择
    'host': '192.168.1.1',  # 设备IP地址
    'username': 'admin',  # SSH用户名
    'password': 'yourpassword',  # SSH密码
    'secret': '',  # 如果需要启用密码，则填写
    'port': 22,  # SSH端口，默认为22
    'verbose': False,  # 是否打印详细信息
}

# 调用函数备份设备配置
>>>>>>> 32c1d20815e8682e52fbf58a331395ea26e722cb
backup_device(device)
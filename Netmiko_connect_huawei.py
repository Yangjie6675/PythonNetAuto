from netmiko import ConnectHandler

SW2 = {
    'device_type': 'huawei',
    'ip': '192.168.136.16',
    'username': 'python',
    'password': '123',
    'secret': '',  # 如果需要特权模式的密码，则设置它；否则可以留空
}

try:
    connect = ConnectHandler(**SW2)
    print("Successfully connected to " + SW2['ip'])

    config_commands = ['interface LoopBack1', 'ip address 2.2.2.2 255.255.255.255']
    output = connect.send_config_set(config_commands)
    print(output)

    # 查看Loopback1接口的配置
    result = connect.send_command('display interface LoopBack1')
    print(result)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    connect.disconnect()
    print("Connection closed.")

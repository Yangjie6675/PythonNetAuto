import pandas as pd  
import paramiko  
import time  
  
def ssh_command(ip, port, username, password, command):  
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    try:  
        ssh.connect(ip, port, username, password, timeout=10)  
        client = ssh.invoke_shell()  
        client.send(command)  
        time.sleep(2)  # 根据需要调整等待时间  
        output = client.recv(65535).decode('utf-8')  
        return output  
    except Exception as e:  
        print(f"Error connecting to {ip}: {str(e)}")  
        return None  
    finally:  
        ssh.close()  
  
def read_excel(file_path):  
    # 假设Excel文件有两列：'IP' 和 'Username'，并且有一个名为'Sheet1'的工作表  
    df = pd.read_excel(file_path, sheet_name='Sheet1')  
    devices = df[['IP', 'Username', 'Password']].to_dict(orient='records')  # 假设还有'Password'列  
    return devices  
  
def read_commands(file_path):  
    # 假设命令文件每行一个命令  
    with open(file_path, 'r') as file:  
        commands = [line.strip() for line in file.readlines()]  
    return commands  
  
def main():  
    device_list_path = 'devices.xlsx'  
    commands_path = 'commands.txt'  
  
    devices = read_excel(device_list_path)  
    commands = read_commands(commands_path)  
  
    for device in devices:  
        ip = device['IP']  
        username = device['Username']  
        password = device['Password']  
  
        for command in commands:  
            output = ssh_command(ip, 22, username, password, command)  
            if output:  
                print(f"Output from {ip} for command '{command}':")  
                print(output)  
  
if __name__ == "__main__":  
    main()
    
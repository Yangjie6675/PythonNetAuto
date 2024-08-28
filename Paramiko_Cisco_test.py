import paramiko
import time

ip = "192.168.136.13"
username = "python"
password = "123"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)

print("Successfully connected to ", ip)

command = ssh_client.invoke_shell()
command.send("configure terminal\n")
command.send("int loop 1\n")
command.send("ip address 3.3.3.3 255.255.255.255\n")
command.send("end\n")
command.send("write memory\n")

time.sleep(2)
output = command.recv(65535)
print(output.decode("ascii"))

ssh_client.close()
import paramiko
from reportlab.lib.pagesizes import letter  # type: ignore
from reportlab.pdfgen import canvas  # type: ignore

# 定义网络设备信息
device_info = {
    'ip': '192.168.136.11',
    'username': 'python',
    'password': 'Cisco@123',
    'secret': 'cisco',
}


def run_inspection():
    try:
        # 创建 SSH 对象
        ssh = paramiko.SSHClient()
        # 允许连接不在 know_hosts 文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=device_info['ip'], username=device_info['username'], password=device_info['password'], look_for_keys=False )

        # 打开一个 Channel 并执行命令
        shell = ssh.invoke_shell()
        # 进入特权模式
        shell.send('enable\n')
        shell.recv(65535).decode()
        shell.send(f"{device_info['secret']}\n")
        shell.recv(65535).decode()

        # 执行巡检命令
        commands = ['show interfaces', 'show version']
        results = {}
        for command in commands:
            shell.send(f"{command}\n")
            output = ""
            while True:
                response = shell.recv(65535).decode()
                output += response
                if '#' in response:
                    break
            results[command] = output

        # 关闭连接
        ssh.close()

        return results

    except Exception as e:
        print(f"发生错误: {e}")
        return None


def generate_pdf_report(results):
    if results is None:
        return

    # 创建 PDF 文件
    pdf_filename = 'network_inspection_report.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # 设置字体和字号
    c.setFont('Helvetica', 16)
    c.drawString(100, 750, '网络设备巡检报告')

    y_position = 700
    for command, output in results.items():
        c.setFont('Helvetica', 12)
        c.drawString(100, y_position, f'命令: {command}')
        y_position -= 20
        c.setFont('Courier', 10)
        lines = output.split('\n')
        for line in lines:
            c.drawString(120, y_position, line)
            y_position -= 12
            if y_position < 50:
                c.showPage()
                y_position = 750

    # 保存 PDF 文件
    c.save()
    print(f"PDF 报告已生成: {pdf_filename}")


if __name__ == "__main__":
    inspection_results = run_inspection()
    generate_pdf_report(inspection_results)
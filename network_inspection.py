from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 定义网络设备信息
device_info = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'your_username',
    'password': 'your_password',
    'secret': 'your_enable_password',
}

def run_inspection():
    try:
        # 连接到设备
        net_connect = ConnectHandler(**device_info)
        net_connect.enable()

        # 执行巡检命令
        commands = ['show interfaces', 'show version']
        results = {}
        for command in commands:
            output = net_connect.send_command(command)
            results[command] = output

        # 断开连接
        net_connect.disconnect()

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
    
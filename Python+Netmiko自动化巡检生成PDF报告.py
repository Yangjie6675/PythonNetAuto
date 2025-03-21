from datetime import datetime
from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import textfsm

def connect_device(device):
    """使用Netmiko连接网络设备"""
    try:
        conn = ConnectHandler(**device)
        print(f"成功连接到 {device['host']}")
        return conn
    except Exception as e:
        print(f"连接 {device['host']} 失败: {str(e)}")
        return None

def execute_commands(conn, commands):
    """执行巡检命令并返回结果"""
    results = {}
    for cmd in commands:
        try:
            output = conn.send_command(cmd)
            results[cmd] = output
        except Exception as e:
            results[cmd] = f"命令执行失败: {str(e)}"
    return results

def parse_interface_status(output):
    """使用TextFSM解析接口状态"""
    with open('cisco_ios_show_interfaces_status.template') as f:
        fsm = textfsm.TextFSM(f)
        result = fsm.ParseText(output)
    return [dict(zip(fsm.header, row)) for row in result]

def generate_pdf(report_data, filename):
    """生成PDF报告"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # 标题
    title = Paragraph("网络设备巡检报告", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # 生成时间
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_info = Paragraph(f"生成时间: {time_str}", styles['Normal'])
    story.append(time_info)
    story.append(Spacer(1, 24))
    
    # 遍历每个设备的检查结果
    for device in report_data:
        # 设备信息
        dev_header = Paragraph(f"设备: {device['ip']} ({device['type']})", styles['Heading2'])
        story.append(dev_header)
        story.append(Spacer(1, 12))
        
        # 检查结果表格
        data = [['检查项', '结果', '状态']]
        for check in device['checks']:
            status = "正常" if check['status'] else "异常"
            row = [check['name'], check['result'], status]
            data.append(row)
        
        # 创建表格
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 24))
    
    # 生成PDF
    doc.build(story)
    print(f"报告已生成: {filename}")

def main():
    # 设备列表
    devices = [
        {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'password',
            'secret': 'enablepass',
            'commands': [
                'show version',
                'show interfaces status',
                'show running-config | include logging'
            ]
        }
    ]

    report_data = []

    for dev in devices:
        device_info = {
            'ip': dev['host'],
            'type': dev['device_type'],
            'checks': []
        }
        
        # 连接设备
        conn = connect_device(dev)
        if not conn:
            continue
            
        # 进入特权模式
        conn.enable()
        
        # 执行命令
        results = execute_commands(conn, dev['commands'])
        
        # 分析结果
        # 示例1：检查软件版本
        version_output = results.get('show version', '')
        if 'Version 15.2' in version_output:
            device_info['checks'].append({
                'name': '系统版本检查',
                'result': '版本符合要求 (15.2)',
                'status': True
            })
        else:
            device_info['checks'].append({
                'name': '系统版本检查',
                'result': f"发现异常版本: {version_output.split('Version')[1].split()[0] if 'Version' in version_output else '未知'}",
                'status': False
            })
            
        # 示例2：检查接口状态
        intf_output = results.get('show interfaces status', '')
        parsed_intf = parse_interface_status(intf_output)
        err_intf = [intf for intf in parsed_intf if intf['status'] != 'connected']
        
        if len(err_intf) == 0:
            device_info['checks'].append({
                'name': '接口状态检查',
                'result': '所有接口状态正常',
                'status': True
            })
        else:
            device_info['checks'].append({
                'name': '接口状态检查',
                'result': f"发现 {len(err_intf)} 个异常接口",
                'status': False
            })
        
        report_data.append(device_info)
        conn.disconnect()

    # 生成报告文件名
    filename = f"Network_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    generate_pdf(report_data, filename)

if __name__ == "__main__":
    main()
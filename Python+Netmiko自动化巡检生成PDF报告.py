from datetime import datetime
from netmiko import ConnectHandler
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textfsm

def connect_device(conn_params):  # 仅接收连接参数
    try:
        conn = ConnectHandler(**conn_params)
        print(f"成功连接到 {conn_params['host']}")
        return conn
    except Exception as e:
        print(f"连接 {conn_params['host']} 失败: {str(e)}")
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
    pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))
    
    with open('cisco_ios_show_interfaces_status.textfsm') as f:
        fsm = textfsm.TextFSM(f)
        result = fsm.ParseText(output)
    return [dict(zip(fsm.header, row)) for row in result]

def generate_pdf(report_data, filename):
    """生成PDF报告"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # 自定义中文字体样式
    chinese_style = styles["Normal"]
    chinese_style.fontName = 'SimSun'  # 使用注册的字体名称
    chinese_style.fontSize = 12
    
    # 标题样式
    title_style = styles["Title"]
    title_style.fontName = 'SimSun'
    
    # 使用自定义样式替换默认样式
    story = []
    title = Paragraph("网络设备巡检报告", title_style)
    story.append(title)
    
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
        'connection': {  # 连接参数单独存放
            'device_type': 'cisco_ios',
            'host': '192.168.136.11',
            'username': 'python',
            'password': 'Cisco@123',
            'secret': 'cisco',
        },
        'commands': [  # 命令列表独立存放
            'show version',
            'show interfaces status',
            'show running-config | include logging'
        ]
    }
    ]

    report_data = []

    for dev in devices:
        device_info = {
        'ip': dev['connection']['host'],
        'type': dev['connection']['device_type'],
        'checks': []
        }
        
        # 连接设备
        conn = connect_device(dev['connection'])
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
        err_intf = [intf for intf in parsed_intf if intf['STATUS'] != 'connected']
        
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
    
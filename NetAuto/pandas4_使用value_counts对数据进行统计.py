import pandas as pd

data = {
    'IP地址': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.1'],
    '响应时间(ms)': [10, 15, 7, 12, 10],
    '状态': ['正常', '正常', '正常', '异常', '正常']
}

df = pd.DataFrame(data)

# 统计 IP地址 出现次数
print("IP地址 出现次数统计:")
print(df['IP地址'].value_counts())

# 统计 状态 出现次数
print("\n状态 出现次数统计:")
print(df['状态'].value_counts())
import pandas as pd

data = {
    'IP地址': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
    '响应时间(ms)': [10, 15, 7, 12]
}

df = pd.DataFrame(data)

# 插入新列
df['状态'] = ['正常', '正常', '正常', '异常']
print("插入新列后的 DataFrame:")
print(df)

# 插入新行
new_row = {'IP地址': '192.168.1.5', '响应时间(ms)': 20, '状态': '正常'}
df = df._append(new_row, ignore_index=True)
print("\n插入新行后的 DataFrame:")
print(df)

import pandas as pd

data = {
    'IP地址': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
    '响应时间(ms)': [10, 15, 7, 12]
}

df = pd.DataFrame(data)

# 使用 iloc 索引
print("使用 iloc 索引第1行的数据：")
print(df.iloc[0])

print("\n使用 iloc 索引第1行、第2列的数据：")
print(df.iloc[0, 1])

# 使用 loc 索引
print("\n使用 loc 索引第1行的数据：")
print(df.loc[0])

print("\n使用 loc 索引IP地址和响应时间的数据：")
print(df.loc[:, ['IP地址', '响应时间(ms)']])
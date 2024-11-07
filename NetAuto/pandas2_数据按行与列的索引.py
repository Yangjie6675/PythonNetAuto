import pandas as pd

data ={
    'IP地址':['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
    '响应时间(ms)':[10, 15, 7, 12]
}

df = pd.DataFrame(data)

# iloc和loc都是先行后列
print(df.iloc[: , 0]) # .iloc的列显示只能是整数数字索引
print(df.iloc[1])
print(df.iloc[1,1])


print(df.loc[: , 'IP地址']) # .loc的列显示可以用整数或列表名称来索引

print(df.loc[:, :])

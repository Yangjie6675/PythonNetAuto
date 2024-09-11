import pandas as pd

data ={
    'IP地址':['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'],
    '响应时间(ms)':[10, 15, 7, 12]
}

df = pd.DataFrame(data)

#print(df.loc[1])

print(df.iloc[1])

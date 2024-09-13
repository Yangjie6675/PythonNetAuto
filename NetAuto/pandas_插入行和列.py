import pandas as pd

# 创建一个示例 DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}
df = pd.DataFrame(data)

# 添加新列 'C'
df['C'] = [7, 8, 9]

print(df)

df = df.assign(D=[10, 11, 12])

print(df)

now_row = {'A': 4, 'B':5, "C":6, 'D':7}

df = df._append(now_row, ignore_index=True)

print(df)

df.loc[1] = [0, 0, 0, 0]

print(df)

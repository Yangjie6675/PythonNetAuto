import pandas as pd

# 创建一个示例 DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}
df = pd.DataFrame(data)


now_row = {'A': 4, 'B':5}

df_new = df._append(now_row, ignore_index=True)

print(df_new)
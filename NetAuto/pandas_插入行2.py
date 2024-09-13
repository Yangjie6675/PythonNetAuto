import pandas as pd

# 创建一个示例 DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}
df = pd.DataFrame(data)

# 创建一个新行
new_row = pd.Series([7, 8], index=['A', 'B'])

# 使用 concat 添加新行
df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

print(df)
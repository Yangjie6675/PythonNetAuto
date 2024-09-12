import pandas as pd

excel_file = "inventory.xlsx"
df = pd.read_excel(excel_file)
print(df)

   
import pandas as pd
df = pd.read_excel('device_list.xlsx')
devices = df.to_dict('records')
print (devices)

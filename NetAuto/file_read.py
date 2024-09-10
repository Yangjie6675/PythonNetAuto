import pandas

online_path = "http://192.168.136.100:9000/bulestorm/inventory.xlsx"
data = pandas.read_excel(online_path)
print(data)


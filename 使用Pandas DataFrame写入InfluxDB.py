from pandas import DataFrame
from influxdb_client import InfluxDBClient, Point, WritePrecision

# 连接到InfluxDB，这里需要修改括号里面的参数为你的信息
client = InfluxDBClient(url="http://192.168.136.100:3032", token="BlueStorm", org="BlueStorm")

# 获取写API实例
write_api = client.write_api(write_options=SYNCHRONOUS)

# 示例数据
dataframe = DataFrame({
    'temperature': [23.0, 24.0, 22.5],
    'humidity': [50.0, 52.0, 49.5]
}, index=['2023-04-01T00:00', '2023-04-02T00:00', '2023-04-03T00:00'])

# 将DataFrame转换为InfluxDB的Point列表
points = []
for i in range(len(dataframe)):
    point = Point("measurement").tag("location", "home").field("temperature", dataframe['temperature'][i]).field("humidity", dataframe['humidity'][i])
    points.append(point)

# 写入数据到InfluxDB
write_api.write(bucket="your-bucket", org="your-org", record=points)

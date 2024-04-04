# 四川大学 陈德宏
# 开发时间：2024年4月4日 22点33分
# 此文件提供了一个后端调试的代码
import requests

# 一个例子
response = requests.get('http://127.0.0.1:5000/query_results?start_date=2024-04-01&end_date=2024-05-03&location_remark=123')

if response.status_code == 200:
    print(response.text)
else:
    print("Error:", response.status_code)

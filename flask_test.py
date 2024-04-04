# 四川大学 陈德宏
# 此文件提供了一个后端调试的代码
import requests

# get例子
get_params = {
    'start_date': '2024-04-01',
    'end_date': '2024-05-03',
    'location_remark': '123'
}
response = requests.get('http://127.0.0.1:5000/query_results', params=get_params)

if response.status_code == 200:
    print(response.text)
else:
    print("Error:", response.status_code)


# post例子
data = {'key': 'value'}

response2 = requests.post('example/interface', data=data)
if response.status_code == 200:
    # 打印响应内容
    print(response.text)
else:
    # 若请求失败，打印错误信息
    print("Error:", response.status_code)
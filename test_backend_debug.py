# 四川大学 陈德宏
# 此文件提供了一个后端调试的代码
import pytest
import requests

# 测试一
@pytest.fixture
def base_url():
    return 'http://127.0.0.1:5000'

def test_get_request(base_url):
    get_params = {
        'start_date': '2024-04-01',
        'end_date': '2024-05-03',
        'location_remark': '123'
    }
    response = requests.get(f'{base_url}/query_results', params=get_params)
    assert response.status_code == 200
    assert len(response.text)
    print(response.text)

# 测试二
def test_post_request(base_url):
    data = {'key': 'value'}
    response = requests.post(f'{base_url}/example/interface', data=data)
    assert response.status_code != 200  # 例子，不符合预期，test的时候会过
    
if __name__ == '__main__':
    pytest.main(['-s test_backend_debug.py'])


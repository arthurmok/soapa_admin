# --*-- coding: utf-8 --*--
import json

import requests

header = {
    # "Host": ob['domain'],
    # "Connection": "keep-alive",
    # "Pragma": "no-cache",
    # "Cache-Control": "no-cache",
    # "Referer": item['refer'],
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    # "Accept-Encoding": "gzip, deflate",
    # # "Cookie": ob.get('cookie')
    "Content-Type": "application/json; charset=utf-8",
}


def test_ops_save_fields():
    url = "http://127.0.0.1:8092/ops/api/v1.0/save_fields"
    resp = requests.post(url)
    print json.dumps(resp.json())


def test_ops_rule_type_get():
    url = "http://127.0.0.1:8092/log_an/api/v1.0/ops/rule/types"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_sec_field_type_get():
    url = "http://127.0.0.1:8092/ops/api/v1.0/sec_field_types"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_sec_field_get():
    url = "http://127.0.0.1:8092/ops/api/v1.0/sec_fields"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_expert_post():

    data = dict(
        name="欧阳锋",
        phone="13838383838",
        email="13838383838@qq.com",
        resume="网络安全专家",
        expert_field_ids=[4, 4, 6],
        expert_rule_ids=[31108, 31166]
    )
    json_data = json.dumps(data)
    print json_data
    url = "http://127.0.0.1:8092/ops/api/v1.0/experts"
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_expert_del():
    url = "http://127.0.0.1:8092/ops/api/v1.0/experts/1"
    resp = requests.delete(url)
    print json.dumps(resp.json())


def test_expert_put():

    data = dict(
        name="欧阳锋",
        phone="13838383338",
        email="13838383338@qq.com",
        resume="网络安全专家",
        expert_field_ids=[4, 3, 6],
        expert_rule_ids=[31108, 31166]
    )
    json_data = json.dumps(data)
    print json_data
    url = "http://127.0.0.1:8092/ops/api/v1.0/experts/1"
    resp = requests.put(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_experts_get():
    url = "http://127.0.0.1:8092/ops/api/v1.0/experts"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_experts_get_rules():
    url = "http://127.0.0.1:8092/ops/api/v1.0/experts/2"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_log_get_experts():
    url = "http://127.0.0.1:8092/log_an/api/v1.0/log/experts/31108"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_expert_search_post():

    data = dict(
        name="欧阳锋",
        phone="13838383838",
        email="13838383838@qq.com",
        resume="网络安全专家",
        expert_field_ids=[9, 10, 11],
        expert_rule_ids=[31108, 31166]
    )
    json_data = json.dumps(data)
    print json_data
    url = "http://127.0.0.1:8092/ops/api/v1.0/search/experts"
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_solution_post():
    import os
    from config import D_UP_LOADS
    file_name = os.path.join(D_UP_LOADS, "资产管理示例.xlsx")
    # print file_name
    files = {"file": open(file_name, 'rb')}
    data = dict(
        solution_info="网络安全解决方案",
        describe="网络安全解决方案",
        rule_id=31108,
    )
    json_data = json.dumps(data)
    print json_data
    url = "http://127.0.0.1:8092/ops/api/v1.0/solutions"
    # resp = requests.post(url, json=data, headers=header)
    # print json.dumps(resp.json())


def test_solution_files_post():
    import os
    from config import D_UP_LOADS
    file_name1 = os.path.join(D_UP_LOADS, "资产管理示例.xlsx")
    file_name = os.path.join(D_UP_LOADS, "资产管理子系统.docx")
    # print file_name
    files = {'file1': open(file_name1, 'rb'), 'file2': open(file_name, 'rb'), }
    url = "http://127.0.0.1:8092/ops/api/v1.0/solution/files/1"
    resp = requests.post(url, files=files)
    print json.dumps(resp.json())


def test_solution_get():
    url = "http://127.0.0.1:8092/ops/api/v1.0/solutions"
    resp = requests.get(url)
    print json.dumps(resp.json())


if __name__ == '__main__':
    # test_ops_save_fields()
    # test_sec_field_type_get()
    # test_ops_rule_type_get()
    # test_sec_field_get()

    # test_expert_post()
    # test_expert_put()
    # test_expert_del()
    # test_experts_get()
    # test_experts_get_rules()
    # test_log_get_experts()
    # test_expert_search_post()
    # test_solution_post()
    # test_solution_files_post()
    test_solution_get()
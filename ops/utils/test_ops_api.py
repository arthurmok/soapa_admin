# --*-- coding: utf-8 --*--
import json
import requests
from requests.auth import HTTPDigestAuth

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

AGENT_USER = 'soapa'
AGENT_PWD = 'SF@yjxt17'
AGENT_URL = 'https://114.55.219.41:55000'


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
    url = "http://114.55.219.41:8092/ops/api/v1.0/experts"
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
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


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
    url = "http://127.0.0.1:8092/ops/api/v1.0/solutions?" \
          "page=1&per_page=10&rule_id=31108&rule_desc=Ignored&solution_info="
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_solution_delete():
    url = "http://127.0.0.1:8092/ops/api/v1.0/solutions/1"
    resp = requests.delete(url)
    print json.dumps(resp.json())


def test_solution_put():

    data = dict(
        solution_info="网络安全解决方案修改",
        describe="网络安全解决方案修改",
        rule_id=31108,
    )
    json_data = json.dumps(data)
    print json_data
    url = "http://127.0.0.1:8092/ops/api/v1.0/solutions/2"
    resp = requests.put(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_rules_upload_for_server():
    import os
    from config import D_UP_LOADS
    file_name1 = os.path.join(D_UP_LOADS, "0245-web_rules.xml")
    f = open(file_name1, 'rb')
    print f
    files = {"name": "0245-web_rules.xml",  "data": open(file_name1, 'rb')}
    url = "http://114.55.219.41:55000/rules/upload"
    resp = requests.post(url, files=files)
    print resp.status_code, resp.headers
    print json.dumps(resp.json())


def test_agents_get():
    url = "%s/agents?pretty&offset=0&limit=5&sort=-ip,name" % AGENT_URL
    # print url
    resp = requests.get(url, auth=(AGENT_USER, AGENT_PWD), verify=False)
    # url = 'http://127.0.0.1:8092/ops/api/v1.0/agents?page=1&per_page=10&sort=-ip,name'
    # resp = requests.get(url)
    print resp.json()
    print json.dumps(resp.json())


def test_agents_get_by_id():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents/000'
    resp = requests.get(url)
    print resp.json()
    print json.dumps(resp.json())


def test_agents_get_key():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents/001?key'
    resp = requests.get(url)
    print resp.json()
    print json.dumps(resp.json())


def test_agents_del_by_id():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents/003'
    resp = requests.delete(url)
    print resp.json()
    print json.dumps(resp.json())


def test_agents_post():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents'
    data = dict(
        name="test_agent",
        ip="192.168.0.111"
    )
    json_data = json.dumps(data)
    print json_data
    resp = requests.post(url, json=data, headers=header)
    print resp.json()
    print json.dumps(resp.json())


# 重启部分agent
def test_agents_post_restart():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents?restart=yes'
    data = dict(
        ids=['000', '001']
    )
    json_data = json.dumps(data)
    print json_data
    resp = requests.post(url, json=data, headers=header)
    print resp.json()
    print json.dumps(resp.json())


# 重启所有
def test_agents_put():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents'
    resp = requests.put(url)
    print resp.json()
    print json.dumps(resp.json())


def test_agents_summary():

    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents/summary'
    resp = requests.get(url)
    print resp.json()
    print json.dumps(resp.json())


def test_agents_os():

    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents/summary?os'
    resp = requests.get(url)
    print resp.json()
    print json.dumps(resp.json())


def test_agents_rule_apply():

    url = 'http://127.0.0.1:8092/ops/api/v1.0/agents/rules/apply'
    resp = requests.put(url)
    print resp.json()
    print json.dumps(resp.json())


def test_conf_get():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/conf'
    resp = requests.get(url)
    print resp.json()
    print json.dumps(resp.json())

def test_conf_post():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/conf'
    data = dict(
        conf_name="test_conf",
        conf_value="test_value"
    )
    json_data = json.dumps(data)
    print json_data
    resp = requests.post(url, json=data, headers=header)
    print resp.json()
    print json.dumps(resp.json())

def test_conf_put():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/conf/1'
    data = dict(
        conf_name="ES_URL",
        conf_value="114.55.219.41:9200"
    )
    json_data = json.dumps(data)
    print json_data
    resp = requests.put(url, json=data, headers=header)
    print resp.json()
    print json.dumps(resp.json())


def test_conf_del():
    url = 'http://127.0.0.1:8092/ops/api/v1.0/conf/1'
    resp = requests.delete(url)
    print resp.json()
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
    # test_solution_get()
    # test_solution_delete()
    # test_solution_put()
    # test_rules_upload_for_server()
    # test_agents_get()
    # test_agents_get_by_id()
    # test_agents_get_key()
    # test_agents_post()
    # test_agents_del_by_id()
    # test_agents_put()
    # test_agents_post_restart()
    # test_agents_summary()
    # test_agents_os()
    # test_agents_rule_apply()
    # test_conf_get()
    # test_conf_put()
    # test_conf_del()
    test_conf_post()

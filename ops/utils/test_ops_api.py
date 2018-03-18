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
        expert_field_ids=[3, 4, 5],
        expert_rule_ids=[31103, 31166]
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

def test_asset_get_by_id():
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets/4"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_asset_update():
    data = dict(
        serial_no="HZSP1401",
        name="思科防护墙",
        location="杭州XA分公司",
        owner="王五xx",
        owner_contact="wang@shuofanginfo.com",
        type_id=3,
        ip="114.15.12.14",
        agent_type_id=2,
        port=None,
        network="DMZ",
        manufacturer="思科",
        describe="思科防护墙"
    )
    json_data = json.dumps(data)
    print json_data
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets/12"
    resp = requests.put(url, json=data)

    print json.dumps(resp.json())


def test_asset_delete():
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets/4"
    resp = requests.delete(url)
    print json.dumps(resp.json())


def test_asset_uploads():
    import os
    from config import D_UP_LOADS
    file_name = os.path.join(D_UP_LOADS, "资产管理示例.xlsx")
    # print file_name
    files = {'file': open(file_name, 'rb')}
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets/file"
    resp = requests.post(url, files=files)
    print json.dumps(resp.json())


if __name__ == '__main__':
    # test_sec_field_type_get()
    # test_sec_field_get()
    # test_expert_post()
    # test_ops_rule_type_get()
    test_expert_del()

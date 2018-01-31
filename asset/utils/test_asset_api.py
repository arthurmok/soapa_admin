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


def test_asset_type_get():
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets_types"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_asset_agent_type_get():
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets_agent_types"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_asset_get():
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_asset_post():
    data = dict(
        serial_no="HZSP1001",
        name="思科防护墙",
        location="杭州XA分公司",
        owner="王XX",
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
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets"
    resp = requests.post(url, json=json_data, headers=header)
    print json.dumps(resp.json())


def test_asset_get_by_id():
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets/4"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_asset_update():
    data = dict(
        serial_no="HZSP1001",
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
    url = "http://127.0.0.1:8092/asset/api/v1.0/assets/4"
    resp = requests.put(url, json=json_data)

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
    # test_asset_post()
    # test_asset_get()
    # test_asset_type_get()
    # test_asset_agent_type_get()
    # test_asset_get_by_id()
    # test_asset_update()
    # test_asset_delete()
    test_asset_uploads()
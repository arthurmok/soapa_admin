# --*-- coding: utf-8 --*--
import json

import requests
import os
from config import D_UP_LOADS
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


def test_inspect_system_post():
    data = dict(
        system_name="等保系统测试",
        system_no="Ksegeuiree",
        describe="testeweset"
    )
    json_data = json.dumps(data)
    file_name = os.path.join(D_UP_LOADS, "资产管理示例.xlsx")
    files = {'file': open(file_name, 'rb')}
    print json_data
    url = "http://127.0.0.1:8092/insp/api/v1.0/systems"
    resp = requests.post(url, data=data, files=files)
    print json.dumps(resp.json())


def test_get_system_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/systems/assess/1"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_post_system_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/systems/assess/1"
    data_dict = {
        "system_id": 1,
        "业务信息安全保护等级自评": {
            "社会秩序、公共利益": {
                "严重损害": False,
                "特别严重损害": False,
                "一般损害": True
            },
            "国家安全": {
                "严重损害": False,
                "特别严重损害": False,
                "一般损害": True
            },
            "公民、法人和其他组织的合法权益": {
                "严重损害": False,
                "特别严重损害": False,
                "一般损害": True
            }
        },
        "系统服务安全保护等级自评": {
            "社会秩序、公共利益": {
                "严重损害": True,
                "特别严重损害": False,
                "一般损害": False
            },
            "国家安全": {
                "严重损害": True,
                "特别严重损害": False,
                "一般损害": False
            },
            "公民、法人和其他组织的合法权益": {
                "严重损害": True,
                "特别严重损害": False,
                "一般损害": False
            }
        }
    }

    resp = requests.post(url, json=json.dumps(data_dict), headers=header)
    print json.dumps(resp.json())


def test_post_demands():
    url = "http://127.0.0.1:8092/insp/api/v1.0/demands"
    requests.post(url)


def test_get_tech_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/tech/assess/1"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_post_tech_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/tech/assess/1"
    data_list = [
        "应限制网络最大流量数及网络连接数",
        "访问控制的粒度应达到主体为用户级或进程级，客体为文件、数据库表、记录和字段级",
        "应不允许数据带通用协议通过",
        "应不开放远程拨号访问功能"
    ]
    resp = requests.post(url, json=json.dumps(data_list), headers=header)
    print json.dumps(resp.json())


if __name__ == '__main__':
    # test_inspect_system_post()
    # test_get_system_assess()
    # test_post_system_assess()
    # test_post_demands()
    test_get_tech_assess()
    # test_post_tech_assess()

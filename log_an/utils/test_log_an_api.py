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


def test_post_rule_type():
    data = dict(
        type_name="web",
        describe="web类日志规则"
    )
    json_data = json.dumps(data)

    print json_data
    url = "http://127.0.0.1:8092/log_an/api/v1.0/rule/types"
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_get_rule_type():
    url = "http://127.0.0.1:8092/log_an/api/v1.0/rule/types"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_post_rule_file():
    import os
    from config import D_UP_LOADS
    file_name = os.path.join(D_UP_LOADS, "0245-web_rules.xml")
    # print file_name
    files = {'file': open(file_name, 'rb')}
    url = "http://127.0.0.1:8092/log_an/api/v1.0/rule/types/file/1"
    resp = requests.post(url, files=files)
    print json.dumps(resp.json())


def test_get_rule_rules():
    url = 'http://127.0.0.1:8092/log_an/api/v1.0/rule/rules/1'
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_get_log_logs():
    url = 'http://127.0.0.1:8092/log_an/api/v1.0/log/logs?page=1&per_page=10'
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_get_log_detail():
    url = 'http://127.0.0.1:8092/log_an/api/v1.0/log/logs/AV-zlLW4-avDnWrhyh-h'
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_post_log_logs():
    url = 'http://127.0.0.1:8092/log_an/api/v1.0/log/logs?page=1&per_page=10'
    data = dict(
        level=6,
        dealing=1,
        start_time=None,
        end_time=None,
        describe='',
        srcip='',
        dstip='',
        asset_type=None,
        server_os=None,
    )
    json_data = json.dumps(data)

    print json_data
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


if __name__ == '__main__':
    # test_post_rule_type()
    # test_get_rule_type()
    # test_post_rule_file()
    # test_get_rule_rules()
    # test_get_log_logs()
    # test_get_log_detail()
    test_post_log_logs()

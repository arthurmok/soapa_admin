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


def test_selector_get():
    url = "http://127.0.0.1:8092/selector/api/v1.0/selectors"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_selector_post():
    data = dict(
        name='test_selector',
        cname='test_selector',
        kind='测试权限'
    )
    json_data = json.dumps(data)

    print json_data
    url = "http://127.0.0.1:8092/selector/api/v1.0/selectors"
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_selector_put():
    data = dict(
        name='test_selector11',
        cname='test_selector11',
        kind='测试权限11'
    )
    json_data = json.dumps(data)

    print json_data
    url = "http://127.0.0.1:8092/selector/api/v1.0/selectors/2"
    resp = requests.put(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_selector_delete():
    url = "http://127.0.0.1:8092/selector/api/v1.0/selectors/2"
    resp = requests.delete(url)
    print json.dumps(resp.json())


if __name__ == '__main__':
    # test_selector_get()
    # test_selector_post()
    # test_selector_put()
    test_selector_delete()
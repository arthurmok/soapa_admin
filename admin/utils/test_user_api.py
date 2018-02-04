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


def test_user_get():
    url = "http://127.0.0.1:8092/user/api/v1.0/users"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_user_post():
    data = dict(
        name='test_user',
        cname='test_user',
        email='44455555223@qq.com',
        mobile='15007713434',
        department='department1',
        group_ids='1,2',
        status=True,
        password='abcd.1234'
    )
    json_data = json.dumps(data)

    print json_data
    url = "http://127.0.0.1:8092/user/api/v1.0/users"
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_user_put():
    data = dict(
        name='test_user1',
        cname='test_user1',
        email='44455555223@qq.com',
        mobile='15007713434',
        department='department11',
        group_ids='1,2',
        status=True
    )
    json_data = json.dumps(data)

    print json_data
    url = "http://127.0.0.1:8092/user/api/v1.0/users/2"
    resp = requests.put(url, json=data, headers=header)
    print json.dumps(resp.json())


def test_user_delete():
    url = "http://127.0.0.1:8092/user/api/v1.0/users/2"
    resp = requests.delete(url)
    print json.dumps(resp.json())


def test_user_login():

    data = dict(
        username='test_user',
        password='test_user',
        auth_code='44455555223@qq.com',
    )
    json_data = json.dumps(data)

    print json_data
    url = "http://127.0.0.1:8092/login"
    resp = requests.post(url, json=data, headers=header)
    print json.dumps(resp.json())


if __name__ == '__main__':
    # test_user_get()
    # test_user_post()
    # test_user_put()
    # test_user_delete()
    test_user_login()
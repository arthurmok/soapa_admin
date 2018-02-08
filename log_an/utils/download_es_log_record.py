#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import threading

reload(sys)
sys.setdefaultencoding('utf8')
import datetime
from time import sleep
from config import ES_URL
import json
import httplib2
from log_an.models.log_an_model import LogLogs

http = httplib2.Http(timeout=30)
headers = {"connection": "keep-alive", "user-agent": "Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)"}


def get_scroll_id(run_day, size=8000):
    '''
    滚动查询第一步，先获得查询id和部分数据
    waf-record索引是记录所有异常IP的访问记录
    record true:未被waf识别  false:被waf识别
    upstream_cache_status: "-", 未命中缓存的
    :param size 每次滚动查询返回的记录条数，取值在200～1000之间比较合适
    :param run_day: 查询日期
    :return: scroll_id ,result_list 部分查询记录
    '''
    try:
        index = "waf-record-%s" % run_day
        url = "http://%s/%s/_search?scroll=1m" % (ES_URL, index)
        body = {"size": size,
                "_source": ["path", "remote_addr", "method", "req_body", "req_headers",
                            "http_host", "request_id", "waf_mode", "waf_checkmode", "status", "request_url"],
                "query": {"bool": {"must": [{"term": {"upstream_cache_status": "-"}},
                                            {"regexp": {"path": ".*?(php|asp|jsp|aspx|jspx|cgi).*?"}}
                                            # , {"term": {"method": "PUT"}},
                                            ],
                                   "must_not": [{"prefix": {"remote_addr": "180.97.106."}},  # 百度云观测扫描IP
                                                {"prefix": {"remote_addr": "115.239.212."}},  # 百度云观测扫描IP
                                                {
                                                    "term": {"method": "GET"}
                                                },
                                                ]
                                   }}}

        # 过滤扫描器IP
        # body = get_new_body(run_day=run_day, body=body)
        body_json = json.dumps(body)

        res, content = http.request(url, method='POST', body=body_json, headers=headers)
        if res and res.status == 200:
            scroll_id = json.loads(content)['_scroll_id']
            result_list = json.loads(content)['hits']['hits']
            return scroll_id, result_list
    except Exception, e:
        print str(e)


def scroll_search(scroll_id):
    '''
    滚动查询第二步，根据获得的scroll_id查询剩余的记录
    :param scroll_id:
    :return: result_list 结果列表，每个元素的['_source']就是查询到的记录内容
    '''
    try:
        body = json.dumps({"scroll": "10m", "scroll_id": scroll_id})
        url = "http://%s/_search/scroll" % ES_URL
        res, content = http.request(url, method='POST', body=body, headers=headers)
        if res and res.status == 200 and content:
            result_list = json.loads(content)['hits']['hits']
            return result_list
    except Exception, e:
        print str(e)
        return []


def delete_scroll_api(scroll_id):
    '''
    删除scroll查询api，查询结束时调用（查询结果['hits']['hits']为空）
    不调此函数也可以
    但维持api需要一定的性能开销，所以建议查询结束时主动调此函数，尤其是反复调试测试时
    :param scroll_id:
    :return:
    '''
    url = "http://%s/_search/scroll" % ES_URL
    body = json.dumps({"scroll_id": scroll_id})
    http.request(url, method='DELETE', body=body)


class EsProducer(threading.Thread):
    def __init__(self, re_queue, path_queue, date_str, re_queue_words, re_queue_scoring, waf_queue, db_queue,
                 header_queue=None):
        threading.Thread.__init__(self)
        self.re_queue = re_queue
        self.path_queue = path_queue
        self.date_str = date_str
        self.re_queue_words = re_queue_words
        self.re_queue_scoring = re_queue_scoring
        self.waf_queue = waf_queue
        self.db_queue = db_queue
        self.header_queue = header_queue

    def run(self):
        '''
        队列生产者，从ES拉取日志
        :param run_day: 拉取日志的日期  2017-01-01
        :param queue: 队列，q_es2record
        :return:
        '''
        i = 0
        scroll_id, result_list1 = get_scroll_id(run_day=self.date_str)
        i += 1000
        for result in result_list1:
            log_dict = result['_source']
            '''request_id, remote_addr, path, method, request_url, req_headers, req_body, http_host, waf_mode
                 , waf_checkmode, status'''
            # log = Log(log_dict.get('request_id'), log_dict.get('remote_addr'), log_dict.get('path'),
            #           log_dict.get('method'), log_dict.get('request_url'), log_dict.get('req_headers'),
            #           log_dict.get('req_body'), log_dict.get('http_host'), log_dict.get('waf_mode'),
            #           log_dict.get('waf_checkmode'), log_dict.get('status'), 0, {}, {})
            # if log.body:
            if log_dict.get('req_body'):
                self.re_queue.put(log_dict)
            else:
                log = Log(log_dict.get('request_id'), log_dict.get('remote_addr'), log_dict.get('path'),
                          log_dict.get('method'), log_dict.get('request_url'), log_dict.get('req_headers'),
                          log_dict.get('req_body'), log_dict.get('http_host'), log_dict.get('waf_mode'),
                          log_dict.get('waf_checkmode'), log_dict.get('status'), 0, {}, {})
                self.path_queue.put(log)
            # header values analy
            if self.header_queue:
                self.header_queue.put(log_dict.get('req_headers'))
        flag = 0
        count = 0
        while True:
            result_list2 = scroll_search(scroll_id)
            if not result_list2:
                # delete_scroll_api(scroll_id)  # 销毁scroll_id 供单进程调用，多进程会报错
                flag += 1  # 拉取日志失败则flag加1
                # print "拉取ES日志失败%d 次, 重试中..." % flag
            else:
                flag = 0  # 拉取日志成功则重置flag

                for result in result_list2:

                    log_dict = result['_source']
                    while self.re_queue.full() or self.path_queue.full():
                        sleep(0.5)
                    # log = Log(log_dict.get('request_id'), log_dict.get('remote_addr'), log_dict.get('path'),
                    #           log_dict.get('method'), log_dict.get('request_url'), log_dict.get('req_headers'),
                    #           log_dict.get('req_body'), log_dict.get('http_host'), log_dict.get('waf_mode'),
                    #           log_dict.get('waf_checkmode'), log_dict.get('status'), 0, {}, {})
                    # if log.body:
                    if log_dict.get('req_body'):
                        self.re_queue.put(log_dict)
                    else:
                        log = Log(log_dict.get('request_id'), log_dict.get('remote_addr'), log_dict.get('path'),
                                  log_dict.get('method'), log_dict.get('request_url'), log_dict.get('req_headers'),
                                  log_dict.get('req_body'), log_dict.get('http_host'), log_dict.get('waf_mode'),
                                  log_dict.get('waf_checkmode'), log_dict.get('status'), 0, {}, {})
                        self.path_queue.put(log)
                    # header values analy
                    if self.header_queue:
                        self.header_queue.put(log_dict.get('req_headers'))
                    i += 1
                    count += 1
            if flag > 0:
                sleep(flag * 3)
                if flag > 5:  # 连续多次拉不到日志，就break
                    break
            if not count % 100:
                print 'count:%d re_queue:%d, path_queue:%d, re_queue_words:%d, re_queue_scoring:%d, db_queue:%d, ' \
                      'header_queue:%d, waf_queue:%d' % (count, self.re_queue.qsize(), self.path_queue.qsize(),
                                                         self.re_queue_words.qsize(), self.re_queue_scoring.qsize(),
                                                         self.db_queue.qsize()
                                                         , self.header_queue.qsize() if self.header_queue else 0,
                                                         self.waf_queue.qsize())


if __name__ == '__main__':
    from Queue import Queue

    re_queue = Queue(7000)
    path_queue = Queue(7000)
    date_str = '2017-10-31'
    pro = EsProducer(re_queue, path_queue, date_str)
    pro.start()

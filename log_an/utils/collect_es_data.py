#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from time import sleep
from elasticsearch import Elasticsearch
from config import ES_URL


def get_es_data(index, dstip_list):
    sleep(0.1)
    es = Elasticsearch(ES_URL)
    try:
        res = es.search(index=index,
                        body={
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "terms": {
                                                # "dstip": dstip_list
                                                "agent.ip": dstip_list
                                            }
                                        }
                                    ],
                                    "must_not": [],
                                    "should": []
                                }
                            },
                            "size": 10000
                        },
                        request_timeout=30
                        )
    except:
        sleep(1)
        res = es.search(index=index,
                        body={
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "terms": {
                                                "dstip": dstip_list
                                            }
                                        }
                                    ],
                                    "must_not": [],
                                    "should": []
                                }
                            },
                            "size": 10000
                        },
                        request_timeout=30
                        )
    return res['hits']


def collect_data(run_day, dstip_list=[]):
    index = 'wazuh-alerts-' + run_day
    res_dict = get_es_data(index, dstip_list)
    return res_dict['hits']


if __name__ == '__main__':
    yesterday = '2017.11.13'
    dstip_list = ['172.25.0.101']
    res_list = collect_data(run_day=yesterday, dstip_list=dstip_list)
    for log_dict in res_list:
        pass
    print json.dumps(res_list)

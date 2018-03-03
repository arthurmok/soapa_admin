#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from time import sleep
from elasticsearch import Elasticsearch
from config import ES_URL
from log_an.models.log_an_model import LogLogs, db


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


def _save_log(date_str, dstip_list=[]):

    res_list = collect_data(run_day=date_str, dstip_list=dstip_list)
    for log_dict in res_list:
        log_id = log_dict['_id']
        city_name = log_dict['_source']['GeoLocation']['city_name']
        country_name = log_dict['_source']['GeoLocation']['country_name']
        url = log_dict['_source'].get('url')
        attack_time = log_dict['_source'].get('@timestamp')
        host = log_dict['_source'].get('host')
        rule_id = log_dict['_source'].get('rule').get('id') if log_dict['_source'].get('rule') else None
        source = log_dict['_source'].get('source')
        agent_id = log_dict['_source'].get('agent')['id'] if log_dict['_source'].get('agent') else None
        full_log = log_dict['_source'].get('full_log')
        decoder_name = log_dict['_source'].get('decoder')['name'] if log_dict['_source'].get('decoder') else None
        srcip = log_dict['_source'].get('srcip')
        location = log_dict['_source'].get('location')
        dstip = log_dict['_source'].get('dstip')
        dstport = log_dict['_source'].get('dstport')
        log = LogLogs(log_id, city_name, country_name, url, attack_time, host, rule_id,
                      source, agent_id, full_log, decoder_name, srcip, location, dstip, dstport)
        db.session.add(log)
        db.session.commit()


if __name__ == '__main__':
    yesterday = '2017.11.13'
    dstip_list = ['172.25.0.101']
    _save_log(yesterday, dstip_list)

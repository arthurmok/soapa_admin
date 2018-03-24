#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from time import sleep
from elasticsearch import Elasticsearch
from dateutil import parser
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
    # print res_list
    for log_dict in res_list:
        log_id = log_dict['_id']
        city_name = log_dict['_source']['GeoLocation']['city_name']
        country_name = log_dict['_source']['GeoLocation']['country_name']
        url = log_dict['_source'].get('url')
        attack_time = parser.parse(log_dict['_source'].get('@timestamp'), ignoretz=True)
        host = log_dict['_source'].get('host')
        hostname = log_dict['_source'].get('hostname')
        rule_id = log_dict['_source'].get('rule').get('id') if log_dict['_source'].get('rule') else None
        source = log_dict['_source'].get('source')
        agent_id = log_dict['_source'].get('agent')['id'] if log_dict['_source'].get('agent') else None
        full_log = log_dict['_source'].get('full_log')
        decoder_name = log_dict['_source'].get('decoder')['name'] if log_dict['_source'].get('decoder') else None
        srcip = log_dict['_source'].get('srcip')
        location = log_dict['_source'].get('location')
        dstip = log_dict['_source'].get('dstip')
        dstport = log_dict['_source'].get('dstport')
        log_level = log_dict['_source'].get('rule').get('level') if log_dict['_source'].get('rule') else 0
        describe = log_dict['_source'].get('rule').get('description') if \
            log_dict['_source'].get('rule') else None
        server_os = log_dict['_source'].get('system_name')
        if log_level in [1, 2]:
            level = 1
        elif log_level in [3, 4, 5]:
            level = 2
        elif log_level in [6, 7, 8]:
            level = 3
        elif log_level in [9, 10, 11]:
            level = 4
        elif log_level in [12]:
            level = 5
        elif log_level in [13, 14, 15]:
            level = 6
        else:
            level = 0
        if not db.session.query(LogLogs).filter(LogLogs.log_id == log_id).first():
            log = LogLogs(log_id, city_name, country_name, url, attack_time, host, rule_id,
                          source, agent_id, full_log, decoder_name, srcip, location, dstip,
                          dstport, level=level, describe=describe, hostname=hostname,
                          server_os=server_os)
            db.session.add(log)
            db.session.commit()


if __name__ == '__main__':
    yesterday = '2017.11.14'
    dstip_list = ['172.25.0.101']
    _save_log(yesterday, dstip_list)

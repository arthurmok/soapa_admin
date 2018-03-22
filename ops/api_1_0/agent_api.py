# --*-- coding: utf-8 --*--
import json
from flask import jsonify, request
from flask_restful import Resource
import requests

from common.pagenate import get_page_items
from config import AGENT_URL, AGENT_USER, AGENT_PWD
from ops import logger, api

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
    "Content-Type": "application/json",
}


class AgentsApi(Resource):
    def get(self, id=None):
        try:
            if id:
                if request.values.has_key('key'):
                    url = "%s/agents/%s/key?pretty" % (AGENT_URL, id)
                    resp = requests.get(url, auth=(AGENT_USER, AGENT_PWD), verify=False)
                    agent_dict = resp.json()
                    if agent_dict.get('error'):
                        logger.error(json.dumps(agent_dict))
                        return jsonify({"status": False, "desc": "获取agent的key信息失败"})
                    return jsonify({"status": True, "agent_key": agent_dict.get('data')})
                url = "%s/agents/%s?pretty" % (AGENT_URL, id)
                resp = requests.get(url, auth=(AGENT_USER, AGENT_PWD), verify=False)
                agent_dict = resp.json()
                if agent_dict.get('error'):
                    logger.error(json.dumps(agent_dict))
                    return jsonify({"status": False, "desc": "获取agent信息失败"})
                return jsonify({"status": True, "agent": agent_dict.get('data')})
            page, per_page, offset, search_msg = get_page_items()
            sort = request.values.get('sort', '-ip,name')
            url = "%s/agents?pretty&offset=%d&limit=%d&sort=%s" % (AGENT_URL, offset, per_page, sort)
            resp = requests.get(url, auth=(AGENT_USER, AGENT_PWD), verify=False)
            agents = resp.json()
            if agents.get('error'):
                logger.error(json.dumps(agents))
                return jsonify({"status": False, "desc": "获取agent列表失败"})

        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取agent信息失败"})
        return jsonify({"status": True, "agents": agents.get('data')})

    def post(self):

        try:
            agent_dict = request.get_json()
            if request.values.has_key('restart'):
                try:
                    print request.values.has_key('restart')
                    url = "%s/agents/restart?pretty" % AGENT_URL
                    resp = requests.post(url=url, json=agent_dict, headers=header, auth=(AGENT_USER, AGENT_PWD),
                                         verify=False)
                    res_dict = resp.json()
                    if res_dict.get('error'):
                        logger.error(json.dumps(res_dict))
                        return jsonify({"status": False, "desc": "重启agents失败"})
                except Exception, e:
                    logger.error(e)
                    return jsonify({"status": False, "desc": "重启agents失败"})
                return jsonify({"status": True, "desc": "重启agents成功"})
            url = "%s/agents?pretty" % AGENT_URL
            resp = requests.post(url=url, json=agent_dict, headers=header, auth=(AGENT_USER, AGENT_PWD), verify=False)
            res_dict = resp.json()
            if res_dict.get('error'):
                logger.error(json.dumps(res_dict))
                return jsonify({"status": False, "desc": "增加agent失败"})
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "增加agent失败"})
        return jsonify({"status": True, "desc": "增加agent成功,id为:%s" % res_dict.get('data')})

    def delete(self, id):
        try:
            url = "%s/agents/%s?pretty" % (AGENT_URL, id)
            resp = requests.delete(url, auth=(AGENT_USER, AGENT_PWD), verify=False)
            res_dict = resp.json()
            if res_dict.get('error'):
                logger.error(json.dumps(res_dict))
                return jsonify({"status": False, "desc": "删除agent失败"})
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "删除agent失败"})
        return jsonify({"status": True, "desc": "删除agent成功"})

    # 重启所有agent
    def put(self):
        try:

            url = "%s/agents/restart?pretty" % AGENT_URL
            resp = requests.put(url=url, auth=(AGENT_USER, AGENT_PWD), verify=False)
            res_dict = resp.json()
            if res_dict.get('error'):
                logger.error(json.dumps(res_dict))
                return jsonify({"status": False, "desc": "重启所有agent失败"})
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "重启所有agent失败"})
        return jsonify({"status": True, "desc": "重启所有agent成功"})


api.add_resource(AgentsApi, '/ops/api/v1.0/agents', methods=['GET', 'POST', 'PUT'], endpoint='ops_agents')
api.add_resource(AgentsApi, '/ops/api/v1.0/agents/<string:id>', methods=['GET', 'DELETE'], endpoint='ops_agents_id')
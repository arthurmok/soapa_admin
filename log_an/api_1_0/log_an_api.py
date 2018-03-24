# --*-- coding: utf-8 --*--
import json

import os
from xml.dom.minidom import parse
import xml.dom.minidom
from flask import request, jsonify, send_file
from flask_restful import Resource

from asset.models.assets import AssetAssets
from common.pagenate import get_page_items
from config import D_UP_LOADS
from log_an import api, db, logger
from log_an.models.log_an_model import LogRuleType, LogRules, LogLogs
from ops.models.ops_model import SecuritySolution


class LogRuleTypeApi(Resource):
    def get(self):
        try:
            rule_types = db.session.query(LogRuleType).all()
            rule_type_list = [rule_type._to_dict() for rule_type in rule_types]
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "规则类型信息获取失败"})
        return jsonify({"status": True, "rule_type_list": rule_type_list})

    def post(self):
        try:
            rule_type_dict = request.get_json()
            rule_type = LogRuleType._from_dict(rule_type_dict)
            db.session.add(rule_type)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "规则类型创建失败,检查是否重复创建"})
        return jsonify({"status": True, "desc": "规则类型创建成功"})

    def delete(self, type_id):
        try:
            db.session.query(LogRules).filter(LogRules.rule_type_id == type_id).delete()
            db.session.commit()
            db.session.query(LogRuleType).filter(LogRuleType.id == type_id).delete()
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            logger.error(e)
            return jsonify({"status": False, "desc": "规则类型删除失败"})
        return jsonify({"status": True, "desc": "规则类型删除成功"})


class LogRuleFile(Resource):
    def get(self, rule_type_id):
        try:
            rule_type = db.session.query(LogRuleType).filter(LogRuleType.id == rule_type_id).first()
            if not rule_type:
                raise Exception
            file_name = rule_type.rule_file
            return send_file(file_name, mimetype="application/xml", as_attachment=True)
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "规则文件下载失败"})

    def post(self, rule_type_id):
        try:
            rule_type = db.session.query(LogRuleType).filter(LogRuleType.id == rule_type_id).first()
            files = request.files
            if files and files.get('file'):
                f = files['file']
                # file_name = secure_filename(f.filename)
                file_name = f.filename
                file_name_list = file_name.split('.')
                if file_name_list[1] != 'xml':
                    return jsonify({"status": False, "desc": "文件类型错误"})
                rule_file_name = os.path.join(D_UP_LOADS, file_name)
                f.save(rule_file_name)

                # parse and save rules
                parse_rule_file(rule_file_name, rule_type_id)
                # update rule_type
                rule_type.rule_file = rule_file_name
                db.session.add(rule_type)
                db.session.commit()

            else:
                return jsonify({"status": False, "desc": "上传规则文件错误"})

        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "上传规则文件错误"})
        return jsonify({"status": True, "desc": "上传规则文件成功"})


def parse_rule_file(file_name, rule_type_id):
    # delete rules before parse rules
    db.session.query(LogRules).filter(LogRules.rule_type_id == rule_type_id).delete()
    db.session.commit()

    DOMTree = xml.dom.minidom.parse(file_name)
    collection = DOMTree.documentElement
    rules = collection.getElementsByTagName("rule")
    for rule in rules:
        rule_id = rule.getAttribute("id")
        level = rule.getAttribute("level")
        description = rule.getElementsByTagName('description')[0]
        describe = description.childNodes[0].data
        rule = LogRules(rule_id, level, describe, rule_type_id)
        db.session.add(rule)
    db.session.commit()


class LogRulesApi(Resource):
    def get(self, rule_type_id):
        try:
           rules = db.session.query(LogRules).filter(LogRules.rule_type_id == rule_type_id).all()
           rule_list = [rule._to_dict() for rule in rules]
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "读取规则信息失败"})
        return jsonify({"status": True, "rules": rule_list})


class LogLogsApi(Resource):
    def get(self, log_id=None):
        try:
            if log_id:
                log = db.session.query(LogLogs).filter(LogLogs.log_id == log_id).first()
                log_detail = log._get_log_detail()
                solution = None
                if log.rule_id:
                    solution = db.session.query(SecuritySolution).filter(SecuritySolution.rule_id
                                                                         == log.rule_id).first()
                log_detail['solution'] = solution.solution_info if solution else None
                return jsonify({"status": True, "log_detail": log_detail})
            page, per_page, offset, search_msg = get_page_items()
            query = db.session.query(LogLogs)
            logs = query.limit(per_page).offset(offset).all()
            total = query.count()
            log_list = [log._to_dict() for log in logs]
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取日志信息失败"})
        return jsonify({"status": True, "page": page, "per_page": per_page,
                        "total": total, "logs": log_list})

    def post(self):
        try:
            search_dict = request.get_json()
            page, per_page, offset, search_msg = get_page_items()
            if search_dict.get('asset_type'):
                query = db.session.query(LogLogs).join(AssetAssets, LogLogs.dstip == AssetAssets.ip
                                                       ).filter(AssetAssets.app_type.in_(search_dict.get('asset_type')))
            else:
                query = db.session.query(LogLogs)
            if search_dict.get('level'):
                level_list = [int(level_str) for level_str in search_dict.get('level')]
                query = query.filter(LogLogs.level.in_(level_list))
            if search_dict.get('dealing'):
                query = query.filter(LogLogs.dealing == search_dict.get('dealing'))
            if search_dict.get('start_time'):
                query = query.filter(LogLogs.attack_time >= search_dict.get('start_time'))
            if search_dict.get('end_time'):
                query = query.filter(LogLogs.attack_time <= search_dict.get('end_time'))
            if search_dict.get('describe'):
                query = query.filter(LogLogs.describe.like(search_dict.get('describe')))
            if search_dict.get('srcip'):
                query = query.filter(LogLogs.srcip.like(search_dict.get('srcip')))
            if search_dict.get('dstip'):
                query = query.filter(LogLogs.srcip.like(search_dict.get('dstip')))
            if search_dict.get('server_os'):
                query = query.filter(LogLogs.srcip.in_(search_dict.get('server_os')))
            logs = query.limit(per_page).offset(offset).all()
            total = query.count()
            log_list = [log._to_dict() for log in logs]
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取日志信息失败"})
        return jsonify({"status": True, "page": page, "per_page": per_page,
                        "total": total, "logs": log_list})

    def put(self, log_id):
        try:
            dealing_dict = request.get_json()
            dealing = dealing_dict['dealing']
            log = db.session.query(LogLogs).filter(LogLogs.log_id == log_id).first()
            if not log:
                raise Exception

            log.dealing = int(dealing)
            db.session.add(log)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "修改日志状态失败"})
        return jsonify({"status": True, "desc": "修改日志状态成功"})


api.add_resource(LogLogsApi, '/log_an/api/v1.0/log/logs', endpoint='log_logs')
api.add_resource(LogLogsApi, '/log_an/api/v1.0/log/logs/<string:log_id>', endpoint='log_detail')
api.add_resource(LogRuleTypeApi, '/log_an/api/v1.0/rule/types', endpoint='rule_types', methods=['GET', 'POST'])
api.add_resource(LogRuleTypeApi, '/log_an/api/v1.0/rule/types/<int:type_id>',
                 endpoint='rule_types_del', methods=['DELETE'])
api.add_resource(LogRuleFile, '/log_an/api/v1.0/rule/types/file/<int:rule_type_id>', endpoint='rule_types_file')
api.add_resource(LogRulesApi, '/log_an/api/v1.0/rule/rules/<int:rule_type_id>', endpoint='rule_rules')



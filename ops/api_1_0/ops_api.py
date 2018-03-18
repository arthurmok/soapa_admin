# --*-- coding: utf-8 --*--
from flask import jsonify, request
from flask_restful import Resource
from ops.models.ops_model import SecurityField, SecurityFieldType, SecurityExpert, SecurityExpertRuleRela
from log_an.models.log_an_model import LogRuleType
from ops import db, logger, api


class LogRuleTypeApi(Resource):
    def get(self):
        try:
            log_rule_types = db.session.query(LogRuleType).all()
            rule_types_list = [rule_type._to_dict_for_ops() for rule_type in log_rule_types]

        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取规则类型失败"})
        return jsonify({"status": True, "log_rule_types": rule_types_list})


class SecurityFieldTypeApi(Resource):
    def get(self):
        try:
            sec_field_types = db.session.query(SecurityFieldType).all()
            field_type_list = [sec_field_type._to_dict() for sec_field_type in sec_field_types]

        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取安全领域类型失败"})
        return jsonify({"status": True, "security_field_types": field_type_list})


class SecurityFieldApi(Resource):
    def get(self):
        try:
            fields_dict = {}
            sec_fields = db.session.query(SecurityField).all()
            for sec_field in sec_fields:
                field_type, field_name = sec_field._to_tuple()
                if not fields_dict.has_key(field_type):
                    fields_dict[field_type] = [field_name]
                else:
                    fields_dict[field_type].append(field_name)

        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取安全领域失败"})
        return jsonify({"status": True, "security_fields": fields_dict})


class SecurityExpertApi(Resource):
    def get(self, id=None):
        pass

    def post(self):
        try:
            expert_dict = request.get_json()
            name = expert_dict["name"]
            phone = expert_dict["phone"]
            email = expert_dict["email"]
            resume = expert_dict["resume"]
            expert_filed_ids = expert_dict['expert_field_ids']
            expert_rule_ids = expert_dict['expert_rule_ids']
            expert = SecurityExpert(name, phone, email, resume)
            expert_field_list = []
            for expert_field_id in expert_filed_ids:
                expert_field = db.session.query(SecurityField).filter(SecurityField.id == expert_field_id).first()
                expert_field_list.append(expert_field)
            expert.fields = expert_field_list
            db.session.add(expert)
            db.session.flush()
            expert_id = expert.id
            db.session.commit()
            for rule_id in expert_rule_ids:
                expert_rule_rela = SecurityExpertRuleRela(expert_id, rule_id)
                db.session.add(expert_rule_rela)
                db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息添加失败"})
        return jsonify({"status": True, "desc": "专家信息添加成功"})

    def delete(self, id):
        try:
            expert_query = db.session.query(SecurityExpert).filter(SecurityExpert.id == id)
            expert = expert_query.first()
            expert.fields = []
            db.session.commit()
            expert_query.delete()
            db.session.query(SecurityExpertRuleRela).filter(SecurityExpertRuleRela.expert_id == id).delete()
            db.session.commit()
        except Exception, e:
            print e
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息删除失败"})
        return jsonify({"status": True, "desc": "专家信息删除成功"})


api.add_resource(SecurityFieldApi, '/ops/api/v1.0/sec_fields', endpoint='sec_fields')
api.add_resource(SecurityFieldTypeApi, '/ops/api/v1.0/sec_field_types', endpoint='sec_field_types')
api.add_resource(SecurityExpertApi, '/ops/api/v1.0/experts', endpoint='sec_experts', methods=['GET', 'POST'])
api.add_resource(SecurityExpertApi, '/ops/api/v1.0/experts/<int:id>',
                 endpoint='sec_experts_id', methods=['GET', 'DELETE'])
api.add_resource(LogRuleTypeApi, '/log_an/api/v1.0/ops/rule/types', endpoint='ops_rule_types')
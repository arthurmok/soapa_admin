# --*-- coding: utf-8 --*--
import os
from flask import jsonify, request, url_for
from flask_restful import Resource

from config import D_UP_LOADS
from ops.models.ops_model import SecurityField, SecurityFieldType, SecurityExpert, SecurityExpertRuleRela, \
    SecuritySolution, SolutionFiles
from log_an.models.log_an_model import LogRuleType, LogRules
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
        try:
            if id:

                expert_rules = db.session.query(SecurityExpertRuleRela.rule_id
                                                   ).filter(SecurityExpertRuleRela.expert_id == id).all()
                expert_rule_ids = [expert_rule[0] for expert_rule in expert_rules]
                rules = db.session.query(LogRules).filter(LogRules.rule_id.in_(expert_rule_ids)).all()
                expert_rules = [rule._to_dict_for_ops() for rule in rules]
                return jsonify({"status": True, "expert_rules": expert_rules})
            experts = db.session.query(SecurityExpert).all()
            experts_list = [expert._to_dict() for expert in experts]
        except Exception, e:
            print e
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息获取失败"})
        return jsonify({"status": True, "experts": experts_list})

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
            db.session.commit()
            expert_id = expert.id
            for rule_id in expert_rule_ids:
                expert_rule_rela = SecurityExpertRuleRela(expert_id, rule_id)
                db.session.add(expert_rule_rela)
                db.session.commit()
        except Exception, e:
            print e
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息添加失败"})
        return jsonify({"status": True, "desc": "专家信息添加成功"})

    def put(self, id):
        try:
            expert = db.session.query(SecurityExpert).filter(SecurityExpert.id == id).first()
            expert_id = expert.id
            expert_dict = request.get_json()
            expert.name = expert_dict["name"]
            expert.phone = expert_dict["phone"]
            expert.email = expert_dict["email"]
            expert.resume = expert_dict["resume"]
            expert_filed_ids = expert_dict['expert_field_ids']
            expert_rule_ids = expert_dict['expert_rule_ids']
            expert_field_list = []
            for expert_field_id in expert_filed_ids:
                expert_field = db.session.query(SecurityField).filter(SecurityField.id == expert_field_id).first()
                expert_field_list.append(expert_field)
            expert.fields = expert_field_list
            db.session.add(expert)
            db.session.query(SecurityExpertRuleRela).filter(SecurityExpertRuleRela.expert_id == id).delete()
            for rule_id in expert_rule_ids:
                expert_rule_rela = SecurityExpertRuleRela(expert_id, rule_id)
                db.session.add(expert_rule_rela)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息修改失败"})
        return jsonify({"status": True, "desc": "专家信息修改成功"})

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
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息删除失败"})
        return jsonify({"status": True, "desc": "专家信息删除成功"})


class ExpertRuleRelaApi(Resource):
    def get(self, rule_id):
        try:
            rule_experts = db.session.query(SecurityExpertRuleRela.expert_id
                                            ).filter(SecurityExpertRuleRela.rule_id == rule_id).all()
            if rule_experts:
                rule_expert_ids = [rule_expert[0] for rule_expert in rule_experts]
                experts = db.session.query(SecurityExpert).filter(SecurityExpert.id.in_(rule_expert_ids)).all()
                rule_experts = [expert._to_dict() for expert in experts]
            else:
                raise Exception
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息查询失败"})
        return jsonify({"status": True, "log_experts": rule_experts})


class ExpertSearchApi(Resource):
    def post(self):
        try:
            expert_dict = request.get_json()
            name = expert_dict.get("name")
            phone = expert_dict.get("phone")
            email = expert_dict.get("email")
            resume = expert_dict.get("resume")
            expert_filed_ids = expert_dict.get('expert_field_ids')
            query = db.session.query(SecurityExpert)
            if name:
                query = query.filter(SecurityExpert.name.like(name))
            if phone:
                query = query.filter(SecurityExpert.phone.like(phone))
            if email:
                query = query.filter(SecurityExpert.email.like(email))
            if resume:
                query = query.filter(SecurityExpert.resume.like(resume))
            if expert_filed_ids:
                experts_list = []
                experts = query.all()
                for expert in experts:
                    field_ids = [field.id for field in expert.fields]
                    if set(field_ids).intersection(set(expert_filed_ids)):
                        experts_list.append(expert._to_dict())
            else:
                experts = query.all()
                if experts:
                    experts_list = [expert._to_dict() for expert in experts]
                else:
                    experts_list = []
        except Exception, e:
            print e
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "专家信息搜索失败"})

        return jsonify({"status": True, "experts": experts_list})


class SecuritySolutionApi(Resource):
    def get(self):
        try:
            solution_list = []
            solutions = db.session.query(SecuritySolution).all()
            for solution in solutions:
                solution_dict = solution._to_dict()
                if solution_dict['rule_id']:
                    rule = db.session.query(LogRules).filter(LogRules.rule_id == solution_dict['rule_id']).first()
                    if rule:
                        rule_dict = rule._to_dict_for_ops()
                        solution_dict['rule_id'] = rule_dict
                solution_list.append(solution_dict)
        except Exception, e:

            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "处理方案列表查询失败"})
        return jsonify({"status": True, "solutions": solution_list})

    def post(self):
        try:
            solution_dict = request.get_json()
            solution_info = solution_dict.get('solution_info')
            if not solution_info:
                raise Exception
            describe = solution_dict.get('describe')
            rule_id = solution_dict.get('rule_id')

            solution = SecuritySolution(solution_info, describe, rule_id)
            db.session.add(solution)
            db.session.commit()

        except Exception, e:

            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "处理方案添加失败"})
        return jsonify({"status": True, "desc": "处理方案添加成功"})

    def delete(self, id):
        pass

    def put(self, id):
        pass


class SecuritySolutionFilesApi(Resource):
    def post(self, id):
        try:
            files = request.files
            if not files:
                raise Exception
            for file in files.values():
                file_name = file.filename
                file_dir = os.path.join(D_UP_LOADS, file_name)
                file.save(file_dir)
                file.close()
                exist_file = db.session.query(SolutionFiles).filter(SolutionFiles.file_name == file_name).first()
                if not exist_file:
                    solution_file = SolutionFiles(file_name, id)
                    db.session.add(solution_file)
                    db.session.commit()
                    db.session.flush()
                    solution_file.file_url = url_for('solution_files', id=solution_file.id)
                    db.session.add(solution_file)
                    db.session.commit()

        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "处理方案文件上传失败"})
        return jsonify({"status": True, "desc": "处理方案文件上传成功"})


api.add_resource(SecurityFieldApi, '/ops/api/v1.0/sec_fields', endpoint='sec_fields')
api.add_resource(SecurityFieldTypeApi, '/ops/api/v1.0/sec_field_types', endpoint='sec_field_types')
api.add_resource(SecurityExpertApi, '/ops/api/v1.0/experts', endpoint='sec_experts', methods=['GET', 'POST'])
api.add_resource(SecurityExpertApi, '/ops/api/v1.0/experts/<int:id>',
                 endpoint='sec_experts_id', methods=['GET', 'DELETE', 'PUT'])
api.add_resource(LogRuleTypeApi, '/log_an/api/v1.0/ops/rule/types', endpoint='ops_rule_types')
api.add_resource(ExpertRuleRelaApi, '/log_an/api/v1.0/log/experts/<int:rule_id>', endpoint='log_experts')
api.add_resource(ExpertSearchApi, '/ops/api/v1.0/search/experts', methods=['POST'], endpoint='search_experts')
api.add_resource(SecuritySolutionApi, '/ops/api/v1.0/solutions', methods=['POST', 'GET'], endpoint='solutions')
api.add_resource(SecuritySolutionFilesApi, '/ops/api/v1.0/solution/files/<int:id>',
                 # upload: id=solution_id, download/delete:id=file_id
                 methods=['POST', 'GET'], endpoint='solution_files')
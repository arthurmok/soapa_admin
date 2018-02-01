# --*-- coding: utf-8 --*--
import json
import os
import random
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.sql import func
from insp import db, logger, api
from insp.models.inspect_model import InspectSystems, InspectSystemsAssess, InspectAssessType, \
    InspectObject, InspectInjureLevel, InspectObjectLevelRela, InspectTechAssess, InspectTechDemands
from config import D_UP_LOADS


class InspectSystemApi(Resource):
    def get(self):
        pass

    def post(self):
        try:
            # sys_json = request.get_json()
            sys_dict = dict(
                system_name=request.values.get('system_name'),
                system_no=request.values.get('system_no'),
                describe=request.values.get('describe')
            )
            # sys_dict = json.loads(sys_json)
            files = request.files
            f = files['file']
            if f:
                # file_name = secure_filename(f.filename)
                file_name = f.filename
                file_name_list = file_name.split('.')
                word_file_name = file_name_list[0] + datetime.now().strftime('%Y%m%d%H%M%S') + \
                                 str(random.randint(0, 99)) + '.' + file_name_list[1]
                word_file_dir = os.path.join(D_UP_LOADS, word_file_name)
                f.save(word_file_dir)
                sys_dict['system_word'] = word_file_dir
            sys_dict['update_time'] = datetime.now()
            inspect_system = InspectSystems._from_dict(sys_dict)
            db.session.add(inspect_system)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "等保系统创建失败"})
        return jsonify({"status": True, "desc": "等保系统创建成功"})


class InspectSystemsAssessApi(Resource):
    def get(self, system_id):
        try:
            system_assess_dict = {'system_id': system_id}
            for assess_type in db.session.query(InspectAssessType).all():
                system_assess_dict[assess_type.name] = {}
                for assess_object in db.session.query(InspectObject).all():
                    system_assess_dict[assess_type.name][assess_object.name] = {}
                    for level in db.session.query(InspectInjureLevel).all():
                        system_assess_dict[assess_type.name][assess_object.name][level.name] = False
            a = json.dumps(system_assess_dict)
            system_assess = db.session.query(InspectSystemsAssess).filter(InspectSystemsAssess.system_id == system_id).all()
            for assess in system_assess:
                assess_dict = assess._to_dict()
                system_assess_dict[assess_dict['assess_type']][assess_dict['assess']['object_name']][assess_dict['assess']['level_name']] = True
            b = json.dumps(system_assess_dict)
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取安全保护等级自评信息失败"})
        return jsonify({"status": True, "assess": system_assess_dict})

    def post(self, system_id):
        try:
            max_business_level = 0
            max_system_level = 0
            insp_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            data_json = request.get_json()
            data_dict = json.loads(data_json)
            business_dict = data_dict.get('business_assess')
            if business_dict:
                assess_type_id = InspectAssessType._get_id('business_assess')
                db.session.query(InspectSystemsAssess).filter(InspectSystemsAssess.system_id == system_id,
                                                              InspectSystemsAssess.assess_type_id ==
                                                              assess_type_id).delete()
                db.session.commit()
                for object_name in business_dict:
                    object_id = InspectObject._get_id(object_name)
                    level_dict = business_dict.get(object_name)
                    for level in level_dict:
                        if level_dict.get(level):
                            level_id = InspectInjureLevel._get_id(level)
                            object_level_rela_id = InspectObjectLevelRela._get_id(object_id, level_id)
                            system_assess = InspectSystemsAssess(system_id, assess_type_id, object_level_rela_id)
                            db.session.add(system_assess)
                            db.session.commit()
                # update business_level
                max_business_level = db.session.query(func.max(InspectObjectLevelRela.level)).join\
                    (InspectSystemsAssess, InspectObjectLevelRela.id == InspectSystemsAssess.object_level_rela_id
                     ).filter(InspectSystemsAssess.system_id == system_id, InspectSystemsAssess.assess_type_id
                              == assess_type_id).first()[0]
                insp_system.business_level = max_business_level
                db.session.add(insp_system)
                db.session.commit()

            system_dict = data_dict.get('system_assess')
            if system_dict:
                assess_type_id = InspectAssessType._get_id('system_assess')
                db.session.query(InspectSystemsAssess).filter(InspectSystemsAssess.system_id == system_id,
                                                              InspectSystemsAssess.assess_type_id ==
                                                              assess_type_id).delete()
                db.session.commit()
                for object_name in system_dict:
                    object_id = InspectObject._get_id(object_name)
                    level_dict = system_dict.get(object_name)
                    for level in level_dict:
                        if level_dict.get(level):
                            level_id = InspectInjureLevel._get_id(level)
                            object_level_rela_id = InspectObjectLevelRela._get_id(object_id, level_id)
                            system_assess = InspectSystemsAssess(system_id, assess_type_id, object_level_rela_id)
                            db.session.add(system_assess)
                            db.session.commit()


                #  update system_level
                max_system_level = db.session.query(func.max(InspectObjectLevelRela.level)).join \
                    (InspectSystemsAssess, InspectObjectLevelRela.id == InspectSystemsAssess.object_level_rela_id
                     ).filter(InspectSystemsAssess.system_id == system_id,
                              InspectSystemsAssess.assess_type_id
                              == assess_type_id).first()[0]
                insp_system.system_level = max_system_level
                db.session.add(insp_system)
                db.session.commit()
            # update security_level
            insp_system.security_level = max(max_business_level, max_system_level)
            db.session.add(insp_system)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "安全保护等级自评信息提交失败"})
        return jsonify({"status": True, "desc": "安全保护等级自评信息提交成功"})


class InspectTechAssessApi(Resource):
    def get(self, system_id):
        try:
            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            if not inspect_system or inspect_system.security_level == 0:
                return jsonify({"status": False, "desc": "安全保护等级自评尚未完成"})

            tech_assess_dict = {
                'system_id': system_id,
                'security_level': inspect_system.security_level,
                'tech_assess': {}
            }

            for demand_assess in db.session.query(InspectTechAssess).filter(InspectTechAssess.system_id == system_id).all():

                tech_assess_dict['tech_assess'][demand_assess.tech_demand.name] = demand_assess.tech_demand_check
            # b = json.dumps(tech_assess_dict)
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取安全保护等级技术细则自评信息失败"})
        tech_assess_dict["status"] = True
        return jsonify(tech_assess_dict)

    def post(self, system_id):
        try:
            demands_json = request.get_json()
            demands_assess_dict = json.loads(demands_json)
            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            if not inspect_system or inspect_system.security_level == 0:
                return jsonify({"status": False, "desc": "安全保护等级自评尚未完成"})
            db.session.query(InspectTechAssess).filter(InspectTechAssess.system_id == system_id).delete()
            for tech_demand in db.session.query(InspectTechDemands).filter(
                        InspectTechDemands.level == inspect_system.security_level).all():
                tech_demand_id = tech_demand.id
                tech_demand_check = demands_assess_dict['tech_assess'].get(tech_demand.name, False)
                tech_demand_assess = InspectTechAssess(system_id, tech_demand_id, tech_demand_check)
                db.session.add(tech_demand_assess)
                db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "安全保护等级技术细则自评失败"})
        return jsonify({"status": True, "desc": "安全保护等级技术细则自评成功"})


api.add_resource(InspectSystemApi, '/insp/api/v1.0/systems', endpoint='inspect_system')
api.add_resource(InspectSystemsAssessApi, '/insp/api/v1.0/systems/assess/<int:system_id>',
                 endpoint='inspect_system_assess')
api.add_resource(InspectTechAssessApi, '/insp/api/v1.0/tech/assess/<int:system_id>', endpoint='inspect_tech_assess')

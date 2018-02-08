# --*-- coding: utf-8 --*--
import json
import os
import sys

from common.pagenate import get_page_items

reload(sys)
sys.setdefaultencoding('utf-8')
import random
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import request, jsonify, send_file
from flask_restful import Resource, abort
from sqlalchemy.sql import func
from insp import db, logger, api
from insp.models.inspect_model import InspectSystems, InspectSystemsAssess, InspectAssessType, \
    InspectObject, InspectInjureLevel, InspectObjectLevelRela, InspectTechAssess, InspectTechDemands, \
    InspectObjectInjureLevel
from insp.models.insp_manage_model import InspectManageAssess
from config import D_UP_LOADS


class InspectSystemDownloadApi(Resource):
    def get(self, system_id):
        inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
        file_name = inspect_system.system_word
        if os.path.exists(file_name):
            ext_name = file_name.split('.')[1]
            system_name = inspect_system.system_name
            return send_file(file_name, mimetype="application/msword", as_attachment=True,
                             attachment_filename=system_name + '_' + inspect_system.system_no+ext_name)
        else:
            abort(404)

    def post(self, system_id):
        try:
            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            files = request.files
            if files and files.get('file'):
                f = files['file']
                # file_name = secure_filename(f.filename)
                file_name = f.filename
                file_name_list = file_name.split('.')
                word_file_name = file_name_list[0] + datetime.now().strftime('%Y%m%d%H%M%S') + \
                                 str(random.randint(0, 99)) + '.' + file_name_list[1]
                word_file_dir = os.path.join(D_UP_LOADS, word_file_name)
                f.save(word_file_dir)
                inspect_system.system_word = word_file_dir
                db.session.add(inspect_system)
                db.session.commit()
            else:
                return jsonify({"status": False, "desc": "无法获取上传的word附件"})

        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "等保系统word附件上传失败"})
        return jsonify({"status": True, "desc": "等保系统word附件上传成功"})


class InspectSystemApi(Resource):
    def get(self, id=None):
        try:
            if id:
                inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == id).first()
                return jsonify({"status": True, "inspect_system": inspect_system._to_dict()})
            page, per_page, offset, search_msg = get_page_items()
            query = db.session.query(InspectSystems)
            inspect_systems = query.limit(per_page).offset(offset).all()
            total = query.count()
            inspect_systems_list = [inspect_system._to_dict() for inspect_system in inspect_systems]
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取等保系统信息失败"})
        return jsonify({"status": True,  "page": page, "per_page": per_page,
                        "total": total, "inspect_systems": inspect_systems_list})

    def post(self):
        try:
            sys_dict = request.get_json()
            if sys_dict:
                system_no = sys_dict.get('system_no')
            if not sys_dict:
                sys_dict = dict(
                    system_name=request.values.get('system_name'),
                    system_no=request.values.get('system_no'),
                    system_data_json=request.values.get('system_data_json'),
                    describe=request.values.get('describe')
                )

            if db.session.query(InspectSystems).filter(InspectSystems.system_no == system_no).first():
                return jsonify({"status": False, "desc": "编号为：%s的等保系统已存在" % system_no})
            # files = request.files
            #
            # if files and files.get('file'):
            #     f = files['file']
            #     # file_name = secure_filename(f.filename)
            #     file_name = f.filename
            #     file_name_list = file_name.split('.')
            #     word_file_name = file_name_list[0] + datetime.now().strftime('%Y%m%d%H%M%S') + \
            #                      str(random.randint(0, 99)) + '.' + file_name_list[1]
            #     word_file_dir = os.path.join(D_UP_LOADS, word_file_name)
            #     f.save(word_file_dir)
            #     sys_dict['system_word'] = word_file_dir
            sys_dict['update_time'] = datetime.now()
            inspect_system = InspectSystems._from_dict(sys_dict)
            db.session.add(inspect_system)
            db.session.flush()
            system_id = inspect_system.id
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "等保系统创建失败"})
        return jsonify({"status": True, "desc": "等保系统创建成功", "system_id":system_id})

    def put(self, id):
        try:
            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == id).first()
            if not inspect_system:
                return jsonify({"status": False, "desc": "无法查询到该系统"})
            system_dict = request.get_json()
            inspect_system.system_name = system_dict.get('system_name'),
            inspect_system.system_no = system_dict.get('system_no'),
            inspect_system.system_data_json = json.dumps(system_dict.get('system_data_json')) if system_dict.get(
                'system_data_json') else json.dumps({}),
            # inspect_system.system_word = system_dict.get('system_word'),
            inspect_system.describe = system_dict.get('describe'),
            inspect_system.update_time = datetime.now()
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "等保自评系统修改失败"})
        return jsonify({"status": True, "desc": "等保自评系统修改成功"})

    def delete(self, id):
        try:
            db.session.query(InspectSystemsAssess).filter(InspectSystemsAssess.system_id == id).delete()
            db.session.commit()
            db.session.query(InspectTechAssess).filter(InspectTechAssess.system_id == id).delete()
            db.session.commit()
            db.session.query(InspectManageAssess).filter(InspectManageAssess.system_id == id).delete()
            db.session.commit()
            db.session.query(InspectSystems).filter(InspectSystems.id == id).delete()
            db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "等保自评系统删除失败"})
        return jsonify({"status": True, "desc": "等保自评系统删除成功"})


class InspectSystemsAssessApi(Resource):

    def get(self, system_id):
        try:
            system_assess_dict = {
                'system_id': system_id,
                'business_assess': {},
                'system_assess': {}
            }
            # object_levels = db.session.query(InspectObjectInjureLevel).all()
            # for object_level in object_levels:
            #     system_assess_dict['business_assess'][object_level.name] = False
            #     system_assess_dict['system_assess'][object_level.name] = False
            system_assess = db.session.query(InspectSystemsAssess).filter(
                InspectSystemsAssess.system_id == system_id).all()
            for assess in system_assess:
                system_assess_dict[assess.assess_type.name][assess.object_injure_level.name] \
                    = assess.assess_check
            b = json.dumps(system_assess_dict)
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取安全保护等级自评信息失败"})
        system_assess_dict['status'] = True
        return jsonify(system_assess_dict)

    def post(self, system_id):
        try:
            max_business_level = 0
            max_system_level = 0
            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            data_dict = request.get_json()

            business_dict = data_dict.get('business_assess')
            if business_dict:
                assess_type_id = InspectAssessType._get_id('business_assess')
                db.session.query(InspectSystemsAssess).filter(InspectSystemsAssess.system_id == system_id,
                                                              InspectSystemsAssess.assess_type_id ==
                                                              assess_type_id).delete()
                db.session.commit()
                for object_level_name in business_dict:
                    assess_check = business_dict.get(object_level_name)
                    object_level_id, level = InspectObjectInjureLevel._get_id(object_level_name)
                    if not object_level_id:
                        return jsonify({"status": False, "desc": "错误的%s导致安全保护等级自评信息提交失败" % object_level_name})
                    system_assess = InspectSystemsAssess(system_id, assess_type_id, object_level_id, assess_check)
                    db.session.add(system_assess)
                    db.session.commit()
                    if assess_check and (max_business_level < level):
                        max_business_level = level

                # update business_level
                inspect_system.business_level = max_business_level
                db.session.add(inspect_system)
                db.session.commit()

            system_dict = data_dict.get('system_assess')
            if system_dict:
                assess_type_id = InspectAssessType._get_id('system_assess')
                db.session.query(InspectSystemsAssess).filter(InspectSystemsAssess.system_id == system_id,
                                                              InspectSystemsAssess.assess_type_id ==
                                                              assess_type_id).delete()
                db.session.commit()
                for object_level_name in system_dict:
                    assess_check = system_dict.get(object_level_name)
                    object_level_id, level = InspectObjectInjureLevel._get_id(object_level_name)
                    if not object_level_id:
                        return jsonify({"status": False, "desc": "错误的%s导致安全保护等级自评信息提交失败" % object_level_name})
                    system_assess = InspectSystemsAssess(system_id, assess_type_id, object_level_id, assess_check)
                    db.session.add(system_assess)
                    db.session.commit()
                    if assess_check and (max_system_level < level):
                        max_system_level = level

                #  update system_level
                inspect_system.system_level = max_system_level
                db.session.add(inspect_system)
                db.session.commit()
            # update security_level
            inspect_system.security_level = max(max_business_level, max_system_level)
            db.session.add(inspect_system)
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
                'business_level': inspect_system.business_level,
                'system_level': inspect_system.system_level,
                'system_name': inspect_system.system_name,
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
            demands_assess_dict = request.get_json()

            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            if not inspect_system or inspect_system.security_level == 0:
                return jsonify({"status": False, "desc": "安全保护等级自评尚未完成"})
            db.session.query(InspectTechAssess).filter(InspectTechAssess.system_id == system_id).delete()
            db.session.commit()
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


api.add_resource(InspectSystemDownloadApi, '/insp/api/v1.0/systems/download/<int:system_id>',
                 methods=['GET'], endpoint='inspect_system_download')
api.add_resource(InspectSystemDownloadApi, '/insp/api/v1.0/systems/upload/<int:system_id>',
                 methods=['POST'], endpoint='inspect_system_upload')
api.add_resource(InspectSystemApi, '/insp/api/v1.0/systems', endpoint='inspect_system')
api.add_resource(InspectSystemApi, '/insp/api/v1.0/systems/<int:id>', methods=["DELETE", "PUT", "GET"],
                 endpoint='inspect_system_update')
api.add_resource(InspectSystemsAssessApi, '/insp/api/v1.0/systems/assess/<int:system_id>',
                 endpoint='inspect_system_assess')
api.add_resource(InspectTechAssessApi, '/insp/api/v1.0/tech/assess/<int:system_id>', endpoint='inspect_tech_assess')

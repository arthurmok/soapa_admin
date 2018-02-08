# --*-- coding: utf-8 --*--
import json

from flask import jsonify, request
from flask_restful import Resource
from insp import db, logger, api
from insp.models.insp_manage_model import InspectManageAssess, InspectManageDemands
from insp.models.inspect_model import InspectSystems


class InspectManageAssessApi(Resource):
    def get(self, system_id):
        try:
            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            if not inspect_system or inspect_system.security_level == 0:
                return jsonify({"status": False, "desc": "安全保护等级自评尚未完成"})

            manage_assess_dict = {
                'system_id': system_id,
                'security_level': inspect_system.security_level,
                'business_level': inspect_system.business_level,
                'system_level': inspect_system.system_level,
                'manage_assess': {}
            }
            # for manage_demand in db.session.query(InspectManageDemands).filter(
            #                 InspectManageDemands.level == inspect_system.security_level).all():
            #     manage_assess_dict['manage_assess'][manage_demand.name] = False
            for demand_assess in db.session.query(InspectManageAssess).filter(InspectManageAssess.system_id == system_id).all():

                manage_assess_dict['manage_assess'][demand_assess.manage_demand.name] = demand_assess.manage_demand_check
            # b = json.dumps(manage_assess_dict)
            # print b
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "获取安全保护等级技术细则自评信息失败"})
        manage_assess_dict["status"] = True
        return jsonify(manage_assess_dict)

    def post(self, system_id):
        try:
            demands_assess_dict = request.get_json()

            inspect_system = db.session.query(InspectSystems).filter(InspectSystems.id == system_id).first()
            if not inspect_system or inspect_system.security_level == 0:
                return jsonify({"status": False, "desc": "安全保护等级自评尚未完成"})
            db.session.query(InspectManageAssess).filter(InspectManageAssess.system_id == system_id).delete()
            db.session.commit()
            a_list = demands_assess_dict['manage_assess'].keys()
            b_list =[b.name for b in db.session.query(InspectManageDemands.name).filter(
                        InspectManageDemands.level == inspect_system.security_level).all()]
            print (set(a_list)-set(b_list))
            print (set(b_list) - set(a_list))
            for manage_demand in db.session.query(InspectManageDemands).filter(
                        InspectManageDemands.level == inspect_system.security_level).all():
                manage_demand_id = manage_demand.id
                manage_demand_check = demands_assess_dict['manage_assess'].get(manage_demand.name, False)
                manage_demand_assess = InspectManageAssess(system_id, manage_demand_id, manage_demand_check)
                db.session.add(manage_demand_assess)
                db.session.commit()
        except Exception, e:
            logger.error(e)
            return jsonify({"status": False, "desc": "安全保护等级技术细则自评失败"})
        return jsonify({"status": True, "desc": "安全保护等级技术细则自评成功"})


api.add_resource(InspectManageAssessApi, '/insp/api/v1.0/manage/assess/<int:system_id>', endpoint='inspect_manage_assess')

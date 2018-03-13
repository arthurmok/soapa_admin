# --*-- coding: utf-8 --*--

from flask import request, jsonify
from flask_restful import Resource
from admin import db, logger, api
from admin.models.user import Selector


class SelectorApi(Resource):
    def get(self):
        try:
            selectors = db.session.query(Selector).all()
            selectors_list = [selector._to_dict() for selector in selectors]
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取权限信息失败"})
        return jsonify({"status": True, "selectors": selectors_list})

    def post(self):
        try:
            selector_dict = request.get_json()
            selector = Selector._from_dict(selector_dict)
            db.session.add(selector)
            db.session.commit()

        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "权限创建失败"})
        return jsonify({"status": True, "desc": "权限创建成功"})

    def put(self, id):
        try:
            selector = db.session.query(Selector).filter(Selector.id == id).first()
            if not selector:
                raise Exception
            selector_dict = request.get_json()
            selector.name = selector_dict.get('name'),
            selector.cname = selector_dict.get('cname'),

            selector.kind = selector_dict.get('kind'),

            db.session.add(selector)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "权限修改失败"})
        return jsonify({"status": True, "desc": "权限修改成功"})

    def delete(self, id):
        try:
            db.session.query(Selector).filter(Selector.id == id).delete()
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "权限修改失败"})
        return jsonify({"status": True, "desc": "权限修改成功"})


api.add_resource(SelectorApi, '/selector/api/v1.0/selectors', methods=['GET', 'POST'], endpoint='selectors_api')
api.add_resource(SelectorApi, '/selector/api/v1.0/selectors/<int:id>', methods=['DELETE', 'PUT'], endpoint='selectors_api_id')
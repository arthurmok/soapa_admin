# --*-- coding: utf-8 --*--

from flask import request, jsonify
from flask_restful import Resource
from admin import db, logger, api
from admin.models.user import Group, Selector


class GroupApi(Resource):
    def get(self):
        try:
            groups = db.session.query(Group).all()
            groups_list = [group._to_dict() for group in groups]
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取用户组信息失败"})
        return jsonify({"status": True, "groups": groups_list})

    def post(self):
        try:
            group_dict = request.get_json()
            group = Group._from_dict(group_dict)
            db.session.add(group)
            db.session.commit()

        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "用户组创建失败"})
        return jsonify({"status": True, "desc": "用户组创建成功"})

    def put(self, id):
        try:
            group = db.session.query(Group).filter(Group.id == id).first()
            if not group:
                raise Exception
            group_dict = request.get_json()
            group.name = group_dict.get('name'),
            group.cname = group_dict.get('cname'),

            group.selectors = group_dict.get('selectors'),

            db.session.add(group)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "用户组修改失败"})
        return jsonify({"status": True, "desc": "用户组修改成功"})

    def delete(self, id):
        try:
            db.session.query(Group).filter(Group.id == id).delete()
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "用户组修改失败"})
        return jsonify({"status": True, "desc": "用户组修改成功"})


api.add_resource(GroupApi, '/group/api/v1.0/groups', methods=['GET', 'POST'], endpoint='groups_api')
api.add_resource(GroupApi, '/group/api/v1.0/groups/<int:id>', methods=['DELETE', 'PUT'], endpoint='groups_api_id')
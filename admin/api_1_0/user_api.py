# --*-- coding: utf-8 --*--

from flask import request, jsonify
from flask_restful import Resource
from admin import db, logger, api
from admin.models.user import User


class UserApi(Resource):
    def get(self):
        try:
            users = db.session.query(User).all()
            users_list = [user._to_dict() for user in users]
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "获取用户信息失败"})
        return jsonify({"status": True, "users": users_list})

    def post(self):
        try:
            user_dict = request.get_json()
            user = db.session.query(User).filter(User.name == user_dict.get('name')).first()
            if user:
                return jsonify(dict(status=False, desc='账号已存在'))
            user = User._from_dict(user_dict)
            db.session.add(user)
            db.session.commit()
            # 设置密码及scan_key
            user.password = user.gen_password_hash(user_dict.get('password'))
            user.scan_key = user.generate_auth_uuid()
            db.session.add(user)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "用户创建失败"})
        return jsonify({"status": True, "desc": "用户创建成功"})

    def put(self, id):
        try:
            user = db.session.query(User).filter(User.id == id).first()
            if not user:
                raise Exception
            user_dict = request.get_json()
            user.name = user_dict.get('name'),
            user.cname = user_dict.get('cname'),
            user.email = user_dict.get('email'),
            user.mobile = user_dict.get('mobile'),
            user.department = user_dict.get('department'),
            user.group_ids = user_dict.get('group_ids'),
            user.status = user_dict.get('status')
            db.session.add(user)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "用户修改失败"})
        return jsonify({"status": True, "desc": "用户修改成功"})

    def delete(self, id):
        try:
            db.session.query(User).filter(User.id == id).delete()
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "用户修改失败"})
        return jsonify({"status": True, "desc": "用户修改成功"})


class UserPasswordApi(Resource):
    def post(self):
        try:
            auth_dict = request.get_json()
            if not auth_dict:
                raise Exception
            username = auth_dict.get('username')
            password = auth_dict.get('password')
            new_password = auth_dict.get('new_password')
            user = db.session.query(User).filter(User.name == username, User.status==True).first()
            if not user:
                return jsonify({"status": False, "desc": "用户名或密码错误"})
            verify_res = user.check_password_hash(password)
            if not verify_res:
                return jsonify({"status": False, "desc": "用户名或密码错误"})
            user.password = user.gen_password_hash(new_password)
            db.session.add(user)
            db.session.commit()
        except Exception, e:
            logger.error(e)
            db.session.rollback()
            return jsonify({"status": False, "desc": "密码修改失败"})
        return jsonify({"status": True, "desc": "密码修改成功"})


api.add_resource(UserPasswordApi, '/user/api/v1.0/password', methods=['POST'], endpoint='user_password')
api.add_resource(UserApi, '/user/api/v1.0/users', methods=['GET', 'POST'], endpoint='users_api')
api.add_resource(UserApi, '/user/api/v1.0/users/<int:id>', methods=['DELETE', 'PUT'], endpoint='users_api_id')
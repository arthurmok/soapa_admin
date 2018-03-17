# --*-- coding: utf-8 --*--
from flask import jsonify
from flask_restful import Resource
from ops.models.ops_model import SecurityField
from ops import db, logger, api


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


api.add_resource(SecurityFieldApi, '/ops/api/v1.0/sec_fields', endpoint='sec_fields')

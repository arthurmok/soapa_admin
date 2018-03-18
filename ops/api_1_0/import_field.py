# coding: utf-8
import os
import xlrd
from flask import jsonify
from flask_restful import Resource
from config import D_UP_LOADS
from ops.models.ops_model import SecurityField, SecurityFieldType
from ops import db, api

file_name = os.path.join(D_UP_LOADS, "安全领域.xlsx")
f = open(file_name, 'rb')

data = xlrd.open_workbook(filename=None, file_contents=f.read())


class SaveFieldsApi(Resource):
    def post(self):
        try:
            _save_fields()
        except Exception, e:
            print e
            db.session.rollback()
            return jsonify({"status": False, "desc": "安全领域信息添加失败"})
        return jsonify({"status": True, "desc": "安全领域信息添加成功"})


def _save_fields():
    sheet_data = data.sheets()[0]
    table = sheet_data._cell_values
    for row in table:
        sec_type_name = row[0]
        sec_field_name = row[1]
        sec_field_type = db.session.query(SecurityFieldType).filter(
            SecurityFieldType.type_name == sec_type_name).first()
        if not sec_field_type:
            sec_field_type = SecurityFieldType(sec_type_name)
            db.session.add(sec_field_type)
            db.session.commit()
            db.session.flush()
            sec_type_id = sec_field_type.id

        else:

            sec_type_id = sec_field_type.id
        security_field = SecurityField(sec_field_name, sec_type_id)
        db.session.add(security_field)
        db.session.commit()


api.add_resource(SaveFieldsApi, '/ops/api/v1.0/save_fields')

if __name__ == '__main__':
    _save_fields()


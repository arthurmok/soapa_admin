# coding: utf-8
import os
import xlrd
from config import D_UP_LOADS
from ops.models.ops_model import SecurityField, SecurityFieldType
from ops import db

file_name = os.path.join(D_UP_LOADS, "安全领域.xlsx")
f = open(file_name, 'rb')

data = xlrd.open_workbook(filename=None, file_contents=f.read())


def _save_fields():
    sheet_data = data.sheets()[0]
    table = sheet_data._cell_values
    for row in table:
        sec_type_name = row[0]
        sec_field_name = row[1]
        if not db.session.query(SecurityFieldType).filter(SecurityFieldType.type_name == sec_type_name).first():
            sec_field_type = SecurityFieldType(sec_type_name)
            db.session.flush()
            sec_type_id = sec_field_type.id
            db.session.add(sec_field_type)
            db.session.commit()
        else:
            sec_field_type = db.session.query(SecurityFieldType).filter(SecurityFieldType.type_name == sec_type_name
                                                                    ).first()
            sec_type_id = sec_field_type.id
        security_field = SecurityField(sec_field_name, sec_type_id)
        db.session.add(security_field)
        db.session.commit()


if __name__ == '__main__':
    _save_fields()
#
# a = {
#     {"id": "1", "name": '安全', "provinces": [{"gx": "广西"}, {"gd": "广东"}]},
#     {"en": "美国", "pri":[]}
# }

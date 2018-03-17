# coding: utf-8
import os
import xlrd
from config import D_UP_LOADS
from ops.models.ops_model import SecurityField
from ops import db

file_name = os.path.join(D_UP_LOADS, "安全领域.xlsx")
f = open(file_name, 'rb')

data = xlrd.open_workbook(filename=None, file_contents=f.read())


def _save_fields():
    sheet_data = data.sheets()[0]
    table = sheet_data._cell_values
    for row in table:
        sec_type = row[0]
        sec_field = row[1]
        security_field = SecurityField(sec_field, sec_type)
        db.session.add(security_field)
        db.session.commit()


if __name__ == '__main__':
    _save_fields()

# coding: utf-8
import xlrd
import json

from config import D_UP_LOADS
import os
file_name = os.path.join(D_UP_LOADS, "细则自评.xlsx")
f = open(file_name, 'rb')

data = xlrd.open_workbook(filename=None, file_contents=f.read())
sheet_data = data.sheets()[0]
table = sheet_data._cell_values

table_json = json.dumps(table[1:])
print table_json


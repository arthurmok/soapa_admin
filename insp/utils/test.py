# coding: utf-8
import os
from config import D_UP_LOADS
from xlutils.copy import copy
import xlrd

file_name = os.path.join(D_UP_LOADS, "细则自评.xlsx")
workbook = xlrd.open_workbook(file_name)
new_workbook = copy(workbook)
new_file_name = os.path.join(D_UP_LOADS, "细则自评_new.xlsx")

new_workbook.get_sheet(0).write(0, 4, "foo")
new_workbook.save(new_file_name)

# --*-- coding: utf-8 --*--
import hashlib
import os
import xlrd
from flask_restful import Resource

from config import D_UP_LOADS
from insp import db, logger, api
from insp.models.inspect_model import InspectTechClassify, InspectTechTypes, InspectTechDemands
from insp.models.insp_manage_model import *
file_name = os.path.join(D_UP_LOADS, "细则自评.xlsx")
f = open(file_name, 'rb')

data = xlrd.open_workbook(filename=None, file_contents=f.read())


class ManageDemandsApi(Resource):
    def get(self):
        from xlutils.copy import copy
        file_name = os.path.join(D_UP_LOADS, "细则自评.xlsx")
        # workbook = xlrd.open_workbook(file_name)
        new_workbook = copy(data)
        new_file_name = os.path.join(D_UP_LOADS, "细则自评_new.xlsx")
        sheet_data = data.sheets()[1]
        table = sheet_data._cell_values
        row_id = 1
        for row in table[1:]:

            level = row[0]
            describe = row[3]
            manage_name = db.session.query(InspectManageDemands).filter\
                (InspectManageDemands.level == int(level), InspectManageDemands.describe == describe).first().name
            new_workbook.get_sheet(1).write(row_id, 4, manage_name)
            row_id += 1

        sheet_data_tech = data.sheets()[0]
        table_tech = sheet_data_tech._cell_values
        row_id_tech = 1
        for row in table_tech[1:]:
            level = row[0]
            describe = row[3]
            tech_name = db.session.query(InspectTechDemands).filter \
                (InspectTechDemands.level == int(level), InspectTechDemands.describe == describe).first().name
            new_workbook.get_sheet(0).write(row_id_tech, 4, tech_name)
            row_id_tech += 1
        new_workbook.save(new_file_name)

    def post(self):
        sheet_data = data.sheets()[1]
        table = sheet_data._cell_values
        for row in table[1:]:
            level = int(row[0])
            classify_name = row[1]
            type_name = row[2]
            demand_name = row[3]
            classify = db.session.query(InspectManageClassify).filter(InspectManageClassify.name == classify_name).first()
            if not classify:
                classify = InspectManageClassify(classify_name, classify_name)
                db.session.add(classify)
                db.session.flush()
                db.session.commit()
            classify_id = classify.id
            Manage_type = db.session.query(InspectManageTypes).filter(InspectManageTypes.name == type_name).first()
            if not Manage_type:
                Manage_type = InspectManageTypes(type_name, classify_id, type_name)
                db.session.add(Manage_type)
                db.session.flush()
                db.session.commit()
            Manage_type_id = Manage_type.id
            demand = db.session.query(InspectManageDemands).filter(InspectManageDemands.name == demand_name,
                                                                 InspectManageDemands.level == level).first()
            if demand:
                print demand.id, demand.name, demand.level
            else:
                demand = InspectManageDemands(demand_name, level, Manage_type_id, demand_name)
                db.session.add(demand)
                db.session.commit()


api.add_resource(ManageDemandsApi, '/insp/api/v1.0/manage/demands', endpoint='inspect_manage_demands')
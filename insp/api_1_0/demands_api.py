# --*-- coding: utf-8 --*--
import json
import os
import random
from datetime import datetime

import xlrd
from werkzeug.utils import secure_filename
from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.sql import func

from config import D_UP_LOADS
from insp import db, logger, api
from insp.models.inspect_model import InspectTechClassify, InspectTechTypes, InspectTechDemands

file_name = os.path.join(D_UP_LOADS, "细则自评.xlsx")
f = open(file_name, 'rb')

data = xlrd.open_workbook(filename=None, file_contents=f.read())


class TechDemandsApi(Resource):

    def post(self):
        sheet_data = data.sheets()[0]
        table = sheet_data._cell_values
        for row in table[1:]:
            level = int(row[0])
            classify_name = row[1]
            type_name = row[2]
            demand_name = row[3]
            classify = db.session.query(InspectTechClassify).filter(InspectTechClassify.name == classify_name).first()
            if not classify:
                classify = InspectTechClassify(classify_name, classify_name)
                db.session.add(classify)
                db.session.flush()
                db.session.commit()
            classify_id = classify.id
            tech_type = db.session.query(InspectTechTypes).filter(InspectTechTypes.name == type_name).first()
            if not tech_type:
                tech_type = InspectTechTypes(type_name, classify_id, type_name)
                db.session.add(tech_type)
                db.session.flush()
                db.session.commit()
            tech_type_id = tech_type.id
            demand = db.session.query(InspectTechDemands).filter(InspectTechDemands.name == demand_name,
                                                                 InspectTechDemands.level == level).first()
            if demand:
                print demand.id, demand.name, demand.level
            else:
                demand = InspectTechDemands(demand_name, level, tech_type_id, demand_name)
                db.session.add(demand)
                db.session.commit()


api.add_resource(TechDemandsApi, '/insp/api/v1.0/demands', endpoint='inspect_demands')
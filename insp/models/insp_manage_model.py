# --*-- coding: utf-8 --*--

from insp import db
from inspect_model import InspectSystems


class InspectManageClassify(db.Model):
    # 技术细节自评类型分类
    __tablename__ = "inspect_Manage_classify"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, describe=None):
        self.name = name
        self.describe = describe


class InspectManageTypes(db.Model):
    # 技术细节自评类型
    __tablename__ = "inspect_Manage_types"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    manage_classify_id = db.Column(db.Integer, db.ForeignKey(InspectManageClassify.__tablename__ + '.id'))
    manage_classify = db.relationship('InspectManageClassify')
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, manage_classify_id, describe=None):
        self.name = name
        self.manage_classify_id = manage_classify_id
        self.describe = describe


class InspectManageDemands(db.Model):
    # 技术细节自评细则要求(name, level)唯一
    __tablename__ = "inspect_Manage_demands"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    level = db.Column(db.Integer, nullable=False)  # level: 1-5
    manage_type_id = db.Column(db.Integer, db.ForeignKey(InspectManageTypes.__tablename__ + '.id'))
    manage_type = db.relationship('InspectManageTypes')
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, level, manage_type_id, describe=None):
        self.name = name
        self.level = level
        self.manage_type_id = manage_type_id
        self.describe = describe

    @staticmethod
    def gen_manage_demands_assess(system_level):
        manage_assess = {}
        for manage_demand in db.session.query(InspectManageDemands).filter(InspectManageDemands.level == system_level).all():
            classify_name = manage_demand.manage_type.manage_classify.name
            manage_type_name = manage_demand.manage_type.name
            if not manage_assess.get(classify_name):
                manage_assess[classify_name] = {}
            if not manage_assess[classify_name].get(manage_type_name):
                manage_assess[classify_name][manage_type_name] = {}
                manage_assess[classify_name][manage_type_name][manage_demand.name] = False
        return manage_assess


class InspectManageAssess(db.Model):
    # 技术细节自评
    __tablename__ = "inspect_Manage_assess"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    system_id = db.Column(db.Integer, db.ForeignKey(InspectSystems.__tablename__ + '.id'))
    manage_assess_system = db.relationship('InspectSystems')
    manage_demand_id = db.Column(db.Integer, db.ForeignKey(InspectManageDemands.__tablename__ + '.id'))
    manage_demand = db.relationship('InspectManageDemands')
    manage_demand_check = db.Column(db.Boolean, default=False)

    def __init__(self, system_id, manage_demand_id, manage_demand_check=False):

        self.system_id = system_id
        self.manage_demand_id = manage_demand_id
        self.manage_demand_check = manage_demand_check

    def _to_dict(self):
        # Manage_assess = {
        #     self.Manage_demand.Manage_type.Manage_classify.name: {
        #         self.Manage_demand.Manage_type.name: {
        #             self.Manage_demand.name: self.Manage_demand_check
        #         }
        #     }
        # }
        # Manage_assess_dict = {
        #     "system_id": self.system_id,
        #     "Manage_assess": Manage_assess
        # }
        return {
                    self.manage_demand.name: self.manage_demand_check
                }
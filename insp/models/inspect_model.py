# --*-- coding: utf-8 --*--
import json
from datetime import datetime

from flask import url_for
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from insp import db


class InspectSystems(db.Model):
    __tablename__ = "inspect_systems"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    system_name = db.Column(db.String(50), nullable=False)  # 系统名称
    system_no = db.Column(db.String(50), nullable=False)  # 系统编号
    system_data_json = db.Column(MEDIUMTEXT, nullable=True)  # 系统infomation
    system_word = db.Column(db.String(250), nullable=True)  # word文档路径
    business_level = db.Column(db.Integer, default=0)
    system_level = db.Column(db.Integer, default=0)
    security_level = db.Column(db.Integer, default=0)
    describe = db.Column(db.String(250), nullable=True)
    update_time = db.Column(db.DateTime)

    def __init__(self, system_name, system_no, system_data_json, system_word, describe=None, update_time=datetime.now()):
        self.system_name = system_name
        self.system_no = system_no
        self.system_data_json = system_data_json
        self.system_word = system_word
        self.describe = describe
        self.update_time = update_time

    def _to_dict(self):
        level_dict = {1: '第一级', 2: '第二级', 3: '第三级', 4: '第四级', 5: '第五级'}
        sys_dict = {col.name: getattr(self, col.name, None) for col in self.__table__.columns}
        sys_dict['system_data_json'] = json.loads(sys_dict.get('system_data_json')) if sys_dict.get('system_data_json') else {}
        sys_dict['system_word'] = '/insp/api/v1.0/systems/download/%d' % self.id
        sys_dict['security_level_name'] = level_dict.get(int(self.security_level))
        return sys_dict

    @staticmethod
    def _from_dict(sys_dict):
        return InspectSystems(system_name=sys_dict.get('system_name'),
                              system_no=sys_dict.get('system_no'),
                              system_data_json=json.dumps(sys_dict.get('system_data_json')) if sys_dict.get('system_data_json') else json.dumps({}),
                              system_word=sys_dict.get('system_word'),
                              describe=sys_dict.get('describe'),
                              update_time=sys_dict.get('update_time')
                              )


class InspectAssessType(db.Model):
    # 安全保护等级自评类型
    __tablename__ = "inspect_assess_type"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, describe=None):
        self.name = name
        self.describe = describe

    @staticmethod
    def _get_name(type_id):
        assess_type = db.session.query(InspectAssessType).filter(InspectAssessType.id==type_id).first()
        return assess_type.name

    @staticmethod
    def _get_id(type_name):
        assess_type = db.session.query(InspectAssessType).filter(InspectAssessType.name == type_name).first()
        return assess_type.id


class InspectObjectInjureLevel(db.Model):
    __tablename__ = "inspect_object_injure_level"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    object_name = db.Column(db.String(150), nullable=False)
    injure_level = db.Column(db.String(50), nullable=False)
    level_name = db.Column(db.String(50), nullable=True)
    level = db.Column(db.Integer, nullable=True)
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, object_name, injure_level, level_name, level, describe=None):
        self.name = name
        self.object_name = object_name
        self.injure_level = injure_level
        self.level_name = level_name
        self.level = level
        self.describe = describe

    @staticmethod
    def _get_id(name):
        object_level = db.session.query(InspectObjectInjureLevel).filter(InspectObjectInjureLevel.name == name).first()
        if object_level:
            return object_level.id, object_level.level
        else:
            return None, None


class InspectObject(db.Model):
    # 侵害的客体客体
    __tablename__ = "inspect_object"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, describe=None):
        self.name = name
        self.describe = describe

    @staticmethod
    def _get_id(object_name):
        insp_object = db.session.query(InspectObject).filter(InspectObject.name == object_name).first()
        return insp_object.id


class InspectInjureLevel(db.Model):
    # 客体的侵害程度
    __tablename__ = "inspect_injure_level"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, describe=None):
        self.name = name
        self.describe = describe

    @staticmethod
    def _get_id(level_name):
        level = db.session.query(InspectInjureLevel).filter(InspectInjureLevel.name == level_name).first()
        return level.id


class InspectObjectLevelRela(db.Model):
    __tablename__ = "inspect_object_level_rela"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    object_id = db.Column(db.Integer, db.ForeignKey(InspectObject.__tablename__+'.id'))
    inspect_object = db.relationship('InspectObject')
    injure_level_id = db.Column(db.Integer, db.ForeignKey(InspectInjureLevel.__tablename__+'.id'))
    injure_level = db.relationship('InspectInjureLevel')
    name = db.Column(db.String(50), nullable=True)
    level = db.Column(db.Integer, nullable=True)
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, object_id, injure_level_id, name, level, describe=None):
        self.object_id = object_id
        self.injure_level_id = injure_level_id
        self.name = name
        self.level = level
        self.describe = describe

    def _to_dict(self):
        return {'object_name': self.inspect_object.name, 'level_name': self.injure_level.name}

    @staticmethod
    def _get_id(object_id, level_id):
        object_level_rela = db.session.query(InspectObjectLevelRela).filter\
            (InspectObjectLevelRela.object_id == object_id, InspectObjectLevelRela.injure_level_id == level_id).first()
        return object_level_rela.id


class InspectSystemsAssess(db.Model):
    #  等级自评表
    __tablename__ = 'inspect_system_assess'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    system_id = db.Column(db.Integer, db.ForeignKey(InspectSystems.__tablename__+'.id'))
    assess_system = db.relationship('InspectSystems')
    assess_type_id = db.Column(db.Integer, db.ForeignKey(InspectAssessType.__tablename__+'.id'))
    assess_type = db.relationship('InspectAssessType')
    object_injure_level_id = db.Column(db.Integer, db.ForeignKey(InspectObjectInjureLevel.__tablename__+'.id'))
    object_injure_level = db.relationship('InspectObjectInjureLevel')
    assess_check = db.Column(db.Boolean, default=False)

    def __init__(self, system_id, assess_type_id, object_injure_level_id, assess_check):
        self.system_id = system_id
        self.assess_type_id = assess_type_id
        self.object_injure_level_id = object_injure_level_id
        self.assess_check = assess_check

    def _to_dict(self):
        return {
            'assess_type': self.assess_type.name,
            self.object_injure_level.name: self.assess_check
        }


class InspectTechClassify(db.Model):
    # 技术细节自评类型分类
    __tablename__ = "inspect_tech_classify"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, describe=None):
        self.name = name
        self.describe = describe


class InspectTechTypes(db.Model):
    # 技术细节自评类型
    __tablename__ = "inspect_tech_types"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    tech_classify_id = db.Column(db.Integer, db.ForeignKey(InspectTechClassify.__tablename__ + '.id'))
    tech_classify = db.relationship('InspectTechClassify')
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, tech_classify_id, describe=None):
        self.name = name
        self.tech_classify_id = tech_classify_id
        self.describe = describe


class InspectTechDemands(db.Model):
    # 技术细节自评细则要求(name, level)唯一
    __tablename__ = "inspect_tech_demands"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    level = db.Column(db.Integer, nullable=False)  # level: 1-5
    tech_type_id = db.Column(db.Integer, db.ForeignKey(InspectTechTypes.__tablename__ + '.id'))
    tech_type = db.relationship('InspectTechTypes')
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, level, tech_type_id, describe=None):
        self.name = name
        self.level = level
        self.tech_type_id = tech_type_id
        self.describe = describe

    @staticmethod
    def gen_tech_demands_assess(system_level):
        tech_assess = {}
        for tech_demand in db.session.query(InspectTechDemands).filter(InspectTechDemands.level == system_level).all():
            classify_name = tech_demand.tech_type.tech_classify.name
            tech_type_name = tech_demand.tech_type.name
            if not tech_assess.get(classify_name):
                tech_assess[classify_name] = {}
            if not tech_assess[classify_name].get(tech_type_name):
                tech_assess[classify_name][tech_type_name] = {}
            tech_assess[classify_name][tech_type_name][tech_demand.name] = False
        return tech_assess


class InspectTechAssess(db.Model):
    # 技术细节自评
    __tablename__ = "inspect_tech_assess"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    system_id = db.Column(db.Integer, db.ForeignKey(InspectSystems.__tablename__ + '.id'))
    tech_assess_system = db.relationship('InspectSystems')
    tech_demand_id = db.Column(db.Integer, db.ForeignKey(InspectTechDemands.__tablename__ + '.id'))
    tech_demand = db.relationship('InspectTechDemands')
    tech_demand_check = db.Column(db.Boolean, default=False)

    def __init__(self, system_id, tech_demand_id, tech_demand_check=False):

        self.system_id = system_id
        self.tech_demand_id = tech_demand_id
        self.tech_demand_check = tech_demand_check

    def _to_dict(self):
        # tech_assess = {
        #     self.tech_demand.tech_type.tech_classify.name: {
        #         self.tech_demand.tech_type.name: {
        #             self.tech_demand.name: self.tech_demand_check
        #         }
        #     }
        # }
        # tech_assess_dict = {
        #     "system_id": self.system_id,
        #     "tech_assess": tech_assess
        # }
        return {
                    self.tech_demand.name: self.tech_demand_check
                }

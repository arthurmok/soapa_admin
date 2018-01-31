# --*-- coding: utf-8 --*--
from datetime import datetime

from asset import db


class AssetType(db.Model, object):
    __tablename__ = 'asset_type'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)  # 资产类别
    type_assets = db.relationship('AssetAssets', backref='asset_type')
    describe = db.Column(db.String(250), nullable=True)

    def __init__(self, name, describe=None):
        self.name = name
        self.describe = describe

    def _to_dict(self):
        type_dict = {col.name: getattr(self, col.name, None) for col in self.__table__.columns}
        return type_dict

    @staticmethod
    def _get_type_id_by_name(name):
        asset_type = db.session.query(AssetType).filter(AssetType.name == name).first()
        return asset_type.id if asset_type else 0


class AssetAgentType(db.Model):
    __tablename__ = 'asset_agent_type'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)  # Agent/SYSlog/其他
    agent_type_assets = db.relationship('AssetAssets', backref='asset_agent_type')
    describe = db.Column(db.String(100), nullable=True)

    def __init__(self, name, describe=None):
        self.name = name
        self.describe = describe

    def _to_dict(self):
        agent_type_dict = {col.name: getattr(self, col.name, None) for col in self.__table__.columns}
        return agent_type_dict

    @staticmethod
    def _get_agent_type_id_by_name(name):
        agent_type = db.session.query(AssetAgentType).filter(AssetAgentType.name == name).first()
        return agent_type.id if agent_type else 0


class AssetAssets(db.Model):
    __tablename__ = 'asset_assets'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    serial_no = db.Column(db.String(50), nullable=False, unique=True)  # 资产编号
    name = db.Column(db.String(50), nullable=False)  # 资产名称
    location = db.Column(db.String(250), nullable=False)  # 地点
    owner = db.Column(db.String(50), nullable=False)  # 责任人
    owner_contact = db.Column(db.String(250), nullable=False)  # 责任人联系方式
    type_id = db.Column(db.Integer, db.ForeignKey(AssetType.__tablename__ + '.id'))
    ip = db.Column(db.String(50), nullable=False)  #
    port = db.Column(db.Integer, nullable=True)  # 资产类型为应用系统，必填;如果为其他，选填
    network = db.Column(db.String(50), nullable=True)  # 所属网络
    manufacturer = db.Column(db.String(50), nullable=True)  # 制造商
    agent_type_id = db.Column(db.Integer, db.ForeignKey(AssetAgentType.__tablename__ + '.id'))  #
    describe = db.Column(db.String(250), nullable=True)  # 备注
    alarm_count = db.Column(db.Integer, default=0)  # 告警信息
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, serial_no, name, location, owner, owner_contact, type_id, ip, agent_type_id,
                 port=None, network=None, manufacturer=None, describe=None):
        self.serial_no = serial_no
        self.name = name
        self.location = location
        self.owner = owner
        self.owner_contact = owner_contact
        self.type_id = type_id
        self.ip = ip
        self.agent_type_id = agent_type_id
        self.port = port
        self.network = network
        self.manufacturer = manufacturer
        self.describe = describe

    def _to_dict(self):
        asset_dict = {col.name: getattr(self, col.name, None) for col in self.__table__.columns}
        return asset_dict

    @staticmethod
    def _from_dict(asset_dict):
        return AssetAssets(serial_no=asset_dict['serial_no'], name=asset_dict['name'], location=
                           asset_dict['location'], owner=asset_dict['owner'], owner_contact=
                           asset_dict['owner_contact'], type_id=asset_dict['type_id'], ip=asset_dict['ip'],
                           agent_type_id=asset_dict['agent_type_id'],
                           port=asset_dict['port'], network=asset_dict['network'], manufacturer=
                           asset_dict['manufacturer'], describe=asset_dict['describe']
                           )

    @staticmethod
    def _from_excel_row(row):
        # ["资产编号", "资产名称", "地点", "责任人", "责任人联系方式", "资产类型",
        # "IP地址", "端口", "所属网络", "制造商", "Agent/SYSlog", "备注"]
        serial_no = row[0]
        name = row[1]
        location = row[2]
        owner = row[3]
        owner_contact = row[4]
        type_id = AssetType._get_type_id_by_name(row[5])
        ip = row[6]
        port = int(row[7]) if row[7] else None
        network = row[8]
        manufacturer = row[9]
        agent_type_id = AssetAgentType._get_agent_type_id_by_name(row[10])
        describe = row[11]
        return AssetAssets(serial_no=serial_no, name=name, location=location, owner=owner,
                           owner_contact=owner_contact, type_id=type_id, ip=ip,
                           agent_type_id=agent_type_id, port=port, network=network,
                           manufacturer=manufacturer, describe=describe
                           )

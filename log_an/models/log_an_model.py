# --*-- coding: utf-8 --*--
from datetime import datetime

from log_an import db


class LogLogs(db.Model):
    __tablename__ = 'log_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(100), nullable=False)
    city_name = db.Column(db.String(50), nullable=True)
    country_name = db.Column(db.String(50), nullable=True)
    url = db.Column(db.Text, nullable=True)
    attack_time = db.Column(db.DateTime, nullable=True)
    host = db.Column(db.String(50), nullable=True)
    rule_id = db.Column(db.String(50), nullable=True)
    source = db.Column(db.String(250), nullable=True)
    agent_id = db.Column(db.String(50), nullable=True)
    full_log = db.Column(db.Text, nullable=True)
    decoder_name = db.Column(db.String(50), nullable=True)
    srcip = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(50), nullable=True)
    dstip = db.Column(db.String(50), nullable=True)
    dstport = db.Column(db.Integer, nullable=True)
    level = db.Column(db.Integer, default=0)
    describe = db.Column(db.Text, nullable=True)
    hostname = db.Column(db.String(250), nullable=True)
    dealing = db.Column(db.Integer, default=1)  # 2应急处置、3安全处置、1未处置

    def __init__(self, log_id, city_name, country_name, url, attack_time, host, rule_id,
                 source, agent_id, full_log, decoder_name, srcip, location, dstip, dstport,
                 level=0, describe=None, hostname=None, dealing=1):
        self.log_id = log_id
        self.city_name = city_name
        self.country_name = country_name
        self.url = url
        self.attack_time = attack_time
        self.host = host
        self.rule_id = rule_id
        self.source = source
        self.agent_id = agent_id
        self.full_log = full_log
        self.decoder_name = decoder_name
        self.srcip = srcip
        self.location = location
        self.dstip = dstip
        self.dstport = dstport
        self.level = level
        self.describe = describe
        self.hostname = hostname
        self.dealing = dealing

    def _get_log_detail(self):
        log_detail = dict(
            srcip=self.srcip,
            full_log=self.full_log,
            city_name=self.city_name,
            country_name=self.country_name
        )
        solution = None
        if self.rule_id:
            rule = db.session.query(LogRules).filter(LogRules.rule_id == self.rule_id).first()
            if rule and rule.solution_id:
                solution = db.session.query().filter().first()

        log_detail['solution'] = solution if solution else None
        return log_detail

    def _to_dict(self):

        log_dict = dict(
            log_id=self.log_id,
            attack_time=str(self.attack_time),
            host=self.host,
            dstip=self.dstip,
            dealing=self.dealing,
            level=self.level,
            describe=self.describe,
            rule_id=self.rule_id
        )

        return log_dict


class LogRuleType(db.Model):
    __tablename__ = 'log_rule_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    rule_file = db.Column(db.String(250), nullable=True)
    describe = db.Column(db.Text, nullable=True)

    def __init__(self, type_name, rule_file=None, describe=None):
        self.type_name = type_name
        self.rule_file = rule_file
        self.describe = describe

    def _to_dict(self):
        rule_type_dict = {
            "id": self.id,
            "type_name": self.type_name,
            "rule_file": self.rule_file,
            "describe": self.describe
            }
        if rule_type_dict['rule_file']:
            rule_type_dict['rule_file'] = '/log_an/api/v1.0/rule/types/file/%d' % self.id
        return rule_type_dict

    @staticmethod
    def _from_dict(rule_type_dict):
        return LogRuleType(type_name=rule_type_dict['type_name'], describe=rule_type_dict['describe'])

    def _to_dict_for_ops(self):
        rule_type_dict = {
            "id": self.id,
            "type_name": self.type_name,
            "describe": self.describe,
            "rules": [rule._to_dict_for_ops() for rule in self.type_rules]
        }
        return rule_type_dict

class LogRules(db.Model):
    __tablename__ = 'log_rules'
    rule_id = db.Column(db.Integer, nullable=False, primary_key=True)
    level = db.Column(db.Integer, nullable=False, default=0)
    describe = db.Column(db.Text, nullable=True)
    rule_type_id = db.Column(db.Integer, db.ForeignKey(LogRuleType.__tablename__+'.id'))
    rule_type = db.relationship('LogRuleType', backref='type_rules')
    solution_id = db.Column(db.Integer, nullable=True)

    def __init__(self, rule_id, level, describe, rule_type_id, solution_id=None):
        self.rule_id = rule_id
        self.level = level
        self.describe = describe
        self.rule_type_id = rule_type_id
        self.solution_id = solution_id

    def _to_dict(self):
        rule_dict = {col.name: getattr(self, col.name, None) for col in self.__table__.columns}
        del(rule_dict['rule_type_id'])
        return rule_dict

    def _to_dict_for_ops(self):
        return {
            "rule_id": self.rule_id,
            "level": self.level,
            "describe": self.describe
        }
# --*-- coding: utf-8 --*--
from datetime import datetime

from log_an import db


class LogLogs(db.Model):
    __tablename__ = 'log_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(100), nullable=False)
    city_name = db.Column(db.String(50), nullable=True)
    country_name = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(250), nullable=True)
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

    def __init__(self, log_id, city_name, country_name, url, attack_time, host, rule_id,
                 source, agent_id, full_log, decoder_name, srcip, location, dstip, dstport):
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


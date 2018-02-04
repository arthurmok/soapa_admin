# --*-- coding: utf-8 --*--
from datetime import datetime

from log_an import db


class LogLogs(db.Model):
    __tablename__ = 'log_logs'

    log_id = db.Column(db.String(100), primary_key=True)

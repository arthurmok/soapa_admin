# coding: utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# database
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_DATABASE_URI = 'mysql://mysql_user:YgehieUEIO##@#(llsefeE@localhost/soapa_admin'
SQLALCHEMY_BINDS = {
    'soapa_admin': SQLALCHEMY_DATABASE_URI,
}

# log path
LOG_PATH = basedir + os.sep + 'log'


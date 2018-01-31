# coding: utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# database
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_DATABASE_URI = 'mysql://mysql_user:sEgeHe92Illse78klYex5s@localhost/soapa_admin'
SQLALCHEMY_BINDS = {
    'soapa_admin': SQLALCHEMY_DATABASE_URI,
}

# log path
LOG_PATH = basedir + os.sep + 'log'

# download & upload files
D_UP_LOADS = basedir + os.sep + 'd_up_loads'

SECRET_KEY = 'xgeESX@ghj67g487Gwj8j$^df'
SESSION_LIFETIME = 1000 * 24 * 60 * 60
# coding: utf-8
import os
from datetime import datetime, timedelta
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
ES_URL = '172.25.0.13:9200'
AGENT_URL = 'https://172.25.0.11:55000'
AGENT_USER = 'soapa'
AGENT_PWD = 'SF@yjxt17'

# Scheduler config
JOBS = [
    {
        'id': 'rsync_log_hour_job',
        'func': 'log_an.utils.rsync_log_job:_rsync_es_data_hour_job',
        'args': None,
        'trigger': 'interval',
        'seconds': 1800
    },
    {
        'id': '_count_assets_alarm',
        'func': 'log_an.utils.rsync_log_job:_count_assets_alarm',
        'args': None,
        'trigger': 'interval',
        'seconds': 1800
    },
    # {
    #     'id': 'createschuler_job',
    #     'func': 'log_an.utils.rsync_log_job:_rsync_es_data_job',
    #     'args': None,
    #     'trigger': 'date',
    #     'run_date': datetime.now()+timedelta(seconds=610)
    # },
    {
        'id': 'rsync_log_daily_job',
        'func': 'log_an.utils.rsync_log_job:_rsync_es_data_job',
        'args': None,
        'trigger': {'type': 'cron', 'day_of_week': '*', 'month': '*', 'day': '*', 'hour': '1',
                    'minute': '5', 'second': '5'}
    }
]
SCHEDULER_API_ENABLED = True

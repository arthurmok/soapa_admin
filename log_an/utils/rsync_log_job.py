# --*-- coding: utf-8 --*--
import os
from datetime import datetime, date, timedelta

from asset.models.assets import AssetAssets
from collect_es_data import _save_log

from log_an import logger, db


def _rsync_es_data_hour_job():
    try:
        run_day = str(date.today())
        print run_day, datetime.now()
        today_str = run_day.replace('-', '.')
        today_str = '2017.11.13'
        # with db.app.app_context():
        dstip_list = [asset[0] for asset in db.session.query(AssetAssets.ip).all()]
        print dstip_list
        dstip_list = ['172.25.0.101']
        _save_log(today_str, dstip_list)
    except Exception, e:
        logger.error(e)
        print e


def _rsync_es_data_job():
    try:
        run_day = str(date.today() - timedelta(1))
        print run_day
        # run_day = '2017-10-07'
        yesterday = run_day.replace('-', '.')
        yesterday = '2017.11.13'
        # with db.app.app_context():
        dstip_list = [asset[0] for asset in db.session.query(AssetAssets.ip).all()]
        print dstip_list
        dstip_list = ['172.25.0.101']
        _save_log(yesterday, dstip_list)
    except Exception, e:
        logger.error(e)
        print e


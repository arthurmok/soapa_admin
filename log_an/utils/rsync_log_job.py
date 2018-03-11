# --*-- coding: utf-8 --*--
import os
from datetime import datetime, date, timedelta

from sqlalchemy import func
from werkzeug.contrib.cache import MemcachedCache
from asset.models.assets import AssetAssets
from log_an.models.log_an_model import LogLogs
from collect_es_data import _save_log

from log_an import logger, db

mem_cache = MemcachedCache(['127.0.0.1:11211'])


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


def _count_assets_alarm():
    # print 11111111
    try:
        for asset in db.session.query(AssetAssets).all():
            alarm_count = _caculate_alarm(asset.ip, asset.port)
            mem_cache.set(str(asset.id), alarm_count, timeout=15*60)
    except Exception, e:
        logger.error(e)


def _caculate_alarm(dstip, dstport=None):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    if dstport:
        alarm_count = db.session.query(func.count(LogLogs.log_id)).filter(
            LogLogs.dstip == dstip, LogLogs.dstport == dstport, LogLogs.level > 8).filter(
            LogLogs.attack_time > thirty_days_ago).scalar()
    else:
        alarm_count = db.session.query(func.count(LogLogs.log_id)).filter(
            LogLogs.dstip == dstip, LogLogs.level > 8).filter(
            LogLogs.attack_time > thirty_days_ago).scalar()
    return alarm_count


def get_asset_alarm_by_cache(asset):
    rv = mem_cache.get(asset.id)
    if rv is None:
        rv = _caculate_alarm(asset.ip, asset.port)
        mem_cache.set(str(asset.id), rv, timeout=30 * 60)
    return rv

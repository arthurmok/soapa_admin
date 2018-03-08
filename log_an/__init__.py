from flask import Blueprint

from common.logger import Logger
from ext import db, api

log_an_app = Blueprint('log_an', __name__)
logger = Logger('log_an_')

from api_1_0 import log_an_api
# from utils import rsync_log_job
# from views import test







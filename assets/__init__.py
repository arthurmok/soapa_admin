from flask import Blueprint

from common.logger import Logger
from ext import db

sched_app = Blueprint('assets', __name__)
logger = Logger('sched_')





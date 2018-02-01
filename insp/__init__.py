from flask import Blueprint

from common.logger import Logger
from ext import db, api


inspect_app = Blueprint('insp', __name__)
logger = Logger('inspect_')

from api_1_0 import inspect_api, demands_api, manages_api, insp_manages_api


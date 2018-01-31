from flask import Blueprint

from common.logger import Logger
from ext import db, api

asset_app = Blueprint('asset', __name__)
logger = Logger('asset_')

from api_1_0 import assets







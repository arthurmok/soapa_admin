from flask import Blueprint

from common.logger import Logger
from ext import db, login_manager

admin_app = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
logger = Logger('admin_')

login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.do_login'

from views import user
from api_1_0 import user



from flask import Blueprint
sched_api_blue = Blueprint('sched_api_blue', __name__)

from . import sched_api

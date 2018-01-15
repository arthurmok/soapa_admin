from ext import app
from ext import db
from assets import sched_app
from assets.api_1_0 import sched_api_blue
# from tasks import tasks


def create_app():

    app.config.from_object('config')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    db.init_app(app)
    app.register_blueprint(sched_app, url_prefix='/assets')
    app.register_blueprint(sched_api_blue, url_prefix='/api/v1')
    return app

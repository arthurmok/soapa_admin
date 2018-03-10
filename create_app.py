import os
from ext import app, login_manager
from ext import db, scheduler
from asset import asset_app
# from asset.api_1_0 import asset_api_blue
from admin import admin_app
from insp import inspect_app
from log_an import log_an_app


def create_app():

    app.config.from_object('config')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    db.app = app
    db.init_app(app)
    if not scheduler.running:
        scheduler.init_app(app)
        scheduler.start()
    login_manager.init_app(app)

    app.register_blueprint(asset_app, url_prefix='/asset')
    app.register_blueprint(admin_app, url_prefix='')
    app.register_blueprint(inspect_app, url_prefix='/insp')
    app.register_blueprint(log_an_app, url_prefix='/log')
    # app.register_blueprint(asset_api_blue, url_prefix='/api/v1.0')


    return app

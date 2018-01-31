from ext import app, login_manager
from ext import db
from asset import asset_app
# from asset.api_1_0 import asset_api_blue
from admin import admin_app
from insp import inspect_app


def create_app():

    app.config.from_object('config')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(asset_app, url_prefix='/asset')
    app.register_blueprint(admin_app, url_prefix='')
    app.register_blueprint(inspect_app, url_prefix='/insp')
    # app.register_blueprint(asset_api_blue, url_prefix='/api/v1.0')
    return app

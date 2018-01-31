from flask import Flask, blueprints
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager

app = Flask(__name__, static_folder='admin/static')
db = SQLAlchemy()
api = Api(app)
login_manager = LoginManager()


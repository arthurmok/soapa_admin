from flask import Flask, blueprints
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__, static_folder='admin/static')
CORS(app, supports_credentials=True)
db = SQLAlchemy()
api = Api(app)
login_manager = LoginManager()


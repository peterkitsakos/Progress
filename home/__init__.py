from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from flask_login import LoginManager

home = Flask(__name__)
home.config.from_object(Config)
db = SQLAlchemy(home)
migrate = Migrate(home, db)
login = LoginManager(home)
login.login_view = 'login'

from home import routes, models

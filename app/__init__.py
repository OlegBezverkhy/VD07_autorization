from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config.Config')


db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models



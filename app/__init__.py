# purrfection/__init__.py
# app initializer

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('SECRET_CONFIG')
# app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from .users import signup, confirm, login, logout
from .models import Profile, Message
from .views import index
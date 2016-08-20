# purrfection/__init__.py
# app initializer

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
db = SQLAlchemy(app)

from .users import signup, confirm, login, logout
from .models import Profile, Message
from .views import index
# models.py

from . import db
from .users import User

class Profile(db.Model):
	__tablename__ = 'profile'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
	name = db.Column(db.String(128))
	about_me = db.Column(db.Text)

class Message(db.Model):
	__tablename__ = 'message'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender = db.Column(db.Integer, db.ForeignKey('user.id'))
	receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime)
	body = db.Column(db.Text)
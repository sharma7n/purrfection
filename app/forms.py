# forms.py

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from .models import Profile, Message

class ProfileForm(Form):
	name = StringField('Name', validators=[DataRequired()])
	about_me = TextAreaField('About Me', validators=[DataRequired()])

class MessageForm(Form):
	body = TextAreaField('', validators=[DataRequired()])
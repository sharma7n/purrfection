# utility functions used by multiple modules

from flask import flash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

from . import app


ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
mail = Mail(app)

def send_email(email, subject, html):
	''' Formats and sends an email.'''
	msg = Message(subject,
		sender=app.config['FROM_EMAIL'],
		recipients=[email])
	msg.html = html
	mail.send(msg)

def flash_errors(form):
	'''Flashes error messages on the UI.'''
	for field, errors in form.errors.items():
	    for error in errors:
	        flash(u"Error in the %s field - %s" % (
	            getattr(form, field).label.text,
	            error
	        ))
# users.py
# Generic users utility library for flask apps.

from flask import render_template, url_for, redirect, abort, flash
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import LoginManager, UserMixin, login_user, login_required, \
	logout_user
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_bcrypt import Bcrypt, generate_password_hash

from . import app, db
from .utils import ts, mail, send_email, flash_errors


# app config

bcrypt = Bcrypt(app)

# login manager init

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	'''Identifies a user object.'''
	return User.query.filter(User.id==user_id).first()

# model

class User(db.Model, UserMixin):
	'''Site user definition.'''
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(128), unique=True)
	_password = db.Column(db.String(128))

	def __repr__(self):
		return 'User(id={}, email={}, password={})'.format(
			self.id, self.email, self.password)

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def _set_password(self, plaintext):
		self._password = generate_password_hash(plaintext).decode('utf-8')

	def is_correct_password(self, plaintext):
		'''Checks that an entered password matches the user's password.'''
		return bcrypt.check_password_hash(self._password, plaintext)

# forms

class EmailPasswordForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class EmailForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
	password = PasswordField('Password', validators=[DataRequired()])

# views

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
	form = EmailPasswordForm()
	if form.validate_on_submit():
		user = User(
			email=form.email.data,
			password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Sign up successful.")
		subject = "Confirm your email"
		token = ts.dumps(form.email.data, salt='email-confirm-key')
		confirm_url = url_for(
			'confirm',
			token=token,
			_external=True)
		html = render_template(
			'activate.html', confirm_url=confirm_url)
		# send_email(user.email, subject, html)
		return redirect(url_for('index'))
	else:
		flash_errors(form)

	return render_template('signup.html', form=form)

@app.route("/confirm/<token>")
def confirm(token):
	try:
		email = ts.loads(token, salt='email-confirm-key', max_age=86400)
	except:
		abort(404)
	user = User.query.filter_by(email=email).first_or_404()
	user.email_confirmed = True
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('index'))

@app.route("/login/", methods=['GET', 'POST'])
def login():
	form = EmailPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first_or_404()
		if user.is_correct_password(form.password.data):
			flash("Logged in successfully.")
			print("login OK")
			login_user(user)
			return redirect(url_for('index'))
		else:
			flash_errors(form)
			print("login not OK")
			return redirect(url_for('login'))
	else:
		flash_errors(form)
	return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged out successfully.")
	return redirect(url_for('login'))

# tests
# purrfection
# A dating site for cats. Not cat owners... cats.

import os

from flask import Flask, render_template, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager, login_user, logout_user, login_required

# app init
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter(User.id==user_id).first()

# models

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), unique=True)
	_password = db.Column(db.String(128))

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def _set_password(self, plaintext):
		self._password = bcrypt.generate_password_hash(plaintext)

	def is_correct_password(self, plaintext):
		return bcrypt.check_password_hash(self._password, plaintext)

class Profile():
	None

class Message():
	None

# forms

class EmailPasswordForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class UsernamePasswordForm(Form):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class EmailForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
	password = PasswordField('Password', validators=[DataRequired()])

# views

@app.route("/accounts/create/", methods=['GET', 'POST'])
def create_account():
	form = EmailPasswordForm()
	if form.validate_on_submit():
		user = User(
			email=form.email.data,
			password=form.password.data,
		)
		db.session.add(user)
		db.session.commit()

		# send email confirmation link
		subject = "Confirm your email"

		token = ts.dumps(self.email, salt='email-confirm-key')

		confirm_url = url_for(
			'confirm_email',
			token=token,
			_external=True
		)

		html = render_template(
			'activate.html',
			title='Activate',
			confirm_url=confirm_url
		)

		send_email(user.email, subject, html)

		return redirect(url_for('index'))

	return render_template('create.html',
		title='Create account',
		form=form
	)

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
	form = EmailPasswordForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('signup.html',
		title="Sign up",
		form=form
	)

@app.route("/confirm/<token>")
def confirm_email(token):
	try:
		email = ts.loads(token, salt='email-confirm-key', max_age=86400)
	except:
		abort(404)

	user = User.query.filter_by(email=email).first_or_404()

	user.email_confirmed = True
	db.session.add(user)
	db.session.commit()

	return redirect(url_for('login'))

@app.route("/login/", methods=['GET', 'POST'])
def login():
	form = UsernamePasswordForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first_or_404()
		if user.is_correct_password(form.password.data):
			login_user(user)

			return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
	return render_template('login.html',
		title="Log in",
		form=form
	)

@app.route("/logout/")
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/reset/")
def reset():
	form = EmailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first_or_404()

		subject = "Password reset requested"

		token = ts.dumps(user.email, salt='recover-key')

		recover_url = url_for(
			'reset_with_token',
			token=token,
			_external=True)

		html = render_template(
			'recover.html',
			recover_url=recover_url)

		send_email(user.email, subject, html)

		return redirect(url_for('index'))
	return render_template('reset.html', form=form)

@app.route("/reset/<token>")
def reset_with_token(token):
	try:
		email = ts.loads(token, salt='recover-key', max_age=86400)
	except:
		abort(404)

	form = PasswordForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=email).first_or_404()

		user.password = form.password.data

		db.session.add(user)
		db.session.commit()

		return redirect(url_for('login'))

	return render_template('reset_with_token.html', form=form, token=token)
@app.route("/")
@login_required
def index():
	return "TODO: Make the index view."

@app.route("/profile/")
@login_required
def my_profile():
	return "TODO: Make the my profile view."

@app.route("/profile/<name>")
@login_required
def view_profile():
	return "TODO: Make the profile view."

@app.route("/messages/")
@login_required
def list_messages():
	return "TODO: Make the messages list view."

@app.route("/messages/<int:message_id>")
@login_required
def view_messages():
	return "TODO: Make the message single view."

# run the app
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
# views.py

from datetime import datetime

from flask import redirect, render_template, url_for, flash
from flask_login import current_user

from . import app, db
from .users import login_required
from .models import Profile, Message
from .forms import ProfileForm, MessageForm
from .utils import flash_errors


# TODO: Complete the Index view.
@app.route("/")
@login_required
def index():
	''' Shows a list of messages and profiles to a logged-in cat. Shows the 
	login form to an anonymous cat.'''
	profiles = Profile.query.filter(Profile.user != current_user.id)[:5]
	messages = Message.query.filter_by(receiver=current_user.id)[:5]
	return render_template('index.html', profiles=profiles, messages=messages)

@app.route("/profile/")
@login_required
def my_profile():
	'''Displays a cat's own profile in view mode.'''
	profile = Profile.query.filter_by(user=current_user.id).first()
	if not profile:
		return redirect(url_for('edit_profile'))
	else:
		return render_template('profile.html', profile=profile)

@app.route("/profile/edit/", methods=['GET', 'POST'])
@login_required
def edit_profile():
	'''Displays a cat's own profile in edit mode.'''
	form = ProfileForm()
	if form.validate_on_submit():
		profile = Profile(
			user=current_user.id,
			name=form.name.data,
			about_me=form.about_me.data)
		my_profile = Profile.query.filter_by(user=current_user.id).first()
		if not my_profile:
			db.session.add(profile)
		else:
			my_profile = profile
		db.session.commit()
		return redirect(url_for('index'))
	else:
		flash_errors(form)
	return render_template('edit_profile.html', form=form)

@app.route("/profile/<name>", methods=['GET', 'POST'])
def view_profile(name):
	'''View another cat's profile.'''

	profile = Profile.query.filter_by(name=name).first()

	# build the message form.
	form = MessageForm()
	if form.validate_on_submit():
		message = Message(
			sender=current_user.id,
			receiver=profile.user,
			timestamp=datetime.now(),
			body=form.body.data)
		db.session.add(message)
		db.session.commit()
		flash("Success! Your meowssage was sent!")
		return redirect(url_for('view_profile', name=name))

	if not profile:
		return render_template('view_profile.html', profile=None, form=form)
	elif profile.user == current_user.id:
		return redirect(url_for('my_profile'))
	else:
		return render_template('view_profile.html', profile=profile,
				form=form)

@app.route("/messages/")
@login_required
def messages():
	messages = Message.query.filter_by(receiver=current_user.id)[:5]
	return render_template('list_messages.html', messages=messages)

@app.route("/messages/<int:message_id>")
@login_required
def message(message_id):
	message = Message.query.filter_by(receiver=current_user.id).filter_by(id=message_id).first()
	if message:
		return render_template('view_message.html', message=message)
	else:
		flash("Meowssage not found.")
		return redirect(url_for('messages'))
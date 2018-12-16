from home import home
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from home import db
from home.forms import LoginForm, RegistrationForm, HobbyForm
from home.day import Day
from home.models import User, Hobby

from calendar import monthrange
from datetime import date

import sys

@home.route("/", methods = ['GET', 'POST'])
@home.route("/index", methods = ['GET', 'POST'])
@login_required
def index():
	hobbies = ["Photography","Programming"]

	calendarDays = []
	month = monthrange(date.today().year,date.today().month)
	dayOfWeek = month[0] + 1
	if(dayOfWeek == 7):
		dayOfWeek = 0

	last_week = month[1] % 7
	last_day = ((month[0] + last_week) % 7) + 1

	for blanks in range(dayOfWeek):
		calendarDays.append(Day(0,False,"",True))
	for days in range(month[1]):
		if(days < date.today().day):
			day = Day(days + 1, False, "", True)
		else:
			day = Day(days + 1, False, "", False)
		calendarDays.append(day)
	for blanks in range(last_day, 7):
		calendarDays.append(Day(0,False,"",False))

	return render_template('home.html', hobbies=hobbies, calendarDays=calendarDays)

@home.route("/login", methods = ['GET', 'POST'])
def login():
	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		
		if user is None or not user.get_password(form.password.data):
			print("invalid username or password", file=sys.stdout)
			flash("Invalid Username or Password")
			return redirect(url_for('login'))

		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)

	return render_template('login.html', form=form, title='Login')

@home.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@home.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Registration Succesful!')
		return redirect(url_for('login'))

	return render_template('register.html', form=form, title='Register')

@home.route('/hobbies/<username>', methods=['GET','POST'])
@login_required
def hobbies(username):
	user = User.query.filter_by(username=username).first_or_404()
	hobbies = Hobby.query.filter_by(user=current_user.username).all()
	for x in hobbies:
		print(x)
	return render_template('hobbies.html', user=user, title=username, hobbies=hobbies)

@home.route('/new_hobby', methods=['GET','POST'])
@login_required
def newHobby():
	user = User.query.filter_by(username=current_user.username).first_or_404()

	form = HobbyForm()
	if form.validate_on_submit():
		hobby = Hobby(name=form.name.data, notes=form.notes.data, frequency=form.frequency.data, duration=form.duration.data, goals=form.goals.data, user=current_user.username)
		print("Hobby created")
		db.session.add(hobby)
		print("Added to session")
		db.session.commit()
		print("Commited")
		return redirect(url_for('hobbies', username=current_user.username))
		
	return render_template('newHobby.html', title="New Hobby", form=form)

@home.route('/hobbies/<username>/<hobbyName>', methods=['GET','POST'])
@login_required
def hobbyView(username, hobbyName):
	user = User.query.filter_by(username=username).first_or_404()
	hobby = Hobby.query.filter_by(name=hobbyName).first_or_404()
	hobbies = Hobby.query.filter_by(user=current_user.username).all()
	form = HobbyForm(obj=hobby)

	if form.validate_on_submit():
		hobby.name = form.name.data
		hobby.notes = form.notes.data
		hobby.frequency = form.frequency.data
		hobby.duration = form.duration.data
		hobby.goals = form.goals.data
		db.session.commit()
		print("Updated Entry")
	return render_template('hobbyView.html', hobbies=hobbies, hobby=hobby, form=form)






















	
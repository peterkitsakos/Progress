from home import home
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from home import db
from home.forms import LoginForm, RegistrationForm, HobbyForm
from home.models import User, Hobby, Day, DevBlogPosts

from calendar import monthrange, day_name
from datetime import date, datetime

import sys

@home.route("/", methods = ['GET', 'POST'])
@home.route("/index", methods = ['GET', 'POST'])
@login_required
def index():
	user = User.query.filter_by(username=current_user.username).first_or_404()
	hobbies = user.hobbies

	#Setup calendar days, days of week, month, etc.
	calendarDays = []
	todays_hobbies = []
	month_range = monthrange(date.today().year,date.today().month)
	month = date.today().month

	#Set month to previous for appropriate date in previous months days object
	if month > 1:
		month -= 1
	else:
		month = 12
	year = date.today().year
	
	# If month is not january, decrement to get previousmonth else previous month is december
	if(date.today().month > 1):
		previousMonth = monthrange(date.today().year, date.today().month-1)
	else:
		previousMonth = monthrange(date.today().year - 1, 12);

	dayOfWeek = month_range[0] + 1
	if(dayOfWeek == 7):
		dayOfWeek = 0

	#last_week = number of days in last week of month
	last_week = month_range[1] % 7
	#last_day = number of last day of month
	last_day = ((month_range[0] + last_week) % 7) + 1

	def switch(dayNum):
		switchList = []
		
		for hobby in hobbies:
			if hobby.sunday and dayNum == 2:
				switchList.append(hobby)
			if hobby.monday and dayNum == 3:
				switchList.append(hobby)
			if hobby.tuesday and dayNum == 4:
				switchList.append(hobby)
			if hobby.wednesday and dayNum == 5:
				switchList.append(hobby)
			if hobby.thursday and dayNum == 6:
				switchList.append(hobby)
			if hobby.friday and dayNum == 0:
				switchList.append(hobby)
			if hobby.saturday and dayNum == 1:
				switchList.append(hobby)

		return switchList

	#month is already set to previous
	for prev in range(dayOfWeek,0,-1):#All days remaining from last month
		calendarDays.append(Day(date=(-1*prev)+previousMonth[1]+1, month=month, year=year, past=True, curr=False, _hobbies=todays_hobbies))

	#increment month to get correct one
	if month < 12:
		month += 1
	else:
		month = 1

	for days in range(month_range[1]): #All days from current month
		todays_hobbies = switch(days % 7)

		#If this date has already past
		if(days < date.today().day-1):
			dayObj = Day(date=days + 1, month=month, year=year, past=True, curr=True, _hobbies=todays_hobbies)
		else:
			dayObj = Day(date=days + 1, month=month, year=year, past=False, curr=True, _hobbies=todays_hobbies)
		
		#If day object does not exist in db add it
		if Day.query.filter_by(date=days+1, month=month, year=year).all() == []:
			db.session.add(dayObj)
			db.session.commit()

		dbDay = Day.query.filter_by(date=days+1, month=month, year=year).first()
		calendarDays.append(dbDay)

	#increment month to get correct one
	if month < 12:
		month += 1
	else:
		month = 1

	for future in range(last_day, 7):#All days from next month
		dayObj = Day(date=future - last_day + 1, month=month, year=year, past=True, curr=False, _hobbies=todays_hobbies)
		
		# If day object does not exist in db, add it
		if Day.query.filter_by(date=future - last_day + 1, month=month, year=year).all() == []:
			db.session.add(dayObj)
			db.session.commit()

		dbDay = Day.query.filter_by(date=future - last_day + 1, month=month, year=year).all()
		calendarDays.append(dbDay)


	return render_template('home.html', hobbies=hobbies, calendarDays=calendarDays, year=year)

@home.route("/login", methods = ['GET', 'POST'])
def login():
	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		
		if user is None or not user.get_password(form.password.data):
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

@home.route('/<username>/hobbies', methods=['GET','POST'])
@login_required
def hobbies(username):
	user = User.query.filter_by(username=username).first_or_404()
	hobbies = user.hobbies

	if len(hobbies) < 1:
		return redirect(url_for('newHobby'))
	else:
		hobby = hobbies[0];
		form = HobbyForm(obj=hobby)
		return redirect(url_for('hobbyView', username=current_user.username, hobbyName=hobby.name))

@home.route('/new_hobby', methods=['GET','POST'])
@login_required
def newHobby():
	user = User.query.filter_by(username=current_user.username).first_or_404()

	form = HobbyForm()
	if form.validate_on_submit():
		hobby = Hobby(name=form.name.data, notes=form.notes.data, sunday=form.frequencySun.data, monday=form.frequencyMon.data, tuesday=form.frequencyTue.data, wednesday=form.frequencyWed.data, thursday=form.frequencyThu.data, friday=form.frequencyFri.data, saturday=form.frequencySat.data, color=form.color.data, duration=form.duration.data, goals=form.goals.data, user=user)
		hobby.user = user
		print("Hobby created")
		db.session.add(hobby)
		print("Added to session")
		db.session.commit()
		print("Commited")
		return redirect(url_for('hobbies', username=current_user.username))
		
	return render_template('newHobby.html', title="New Hobby", form=form)

@home.route('/<username>/hobbies/<hobbyName>', methods=['GET','POST'])
@login_required
def hobbyView(username, hobbyName):
	user = User.query.filter_by(username=username).first_or_404()
	hobbies = user.hobbies
	for h in hobbies:
		if h.name == hobbyName:
			hobby = h
	form = HobbyForm(obj=hobby)
	form.color.default = hobby.color

	if form.validate_on_submit():
		if form.save.data:
			hobby.name = form.name.data
			hobby.notes = form.notes.data
			hobby.duration = form.duration.data
			hobby.goals = form.goals.data
			hobby.sunday = form.frequencySun.data
			hobby.monday = form.frequencyMon.data
			hobby.tuesday = form.frequencyTue.data
			hobby.wednesday = form.frequencyWed.data
			hobby.thursday = form.frequencyThu.data
			hobby.friday = form.frequencyFri.data
			hobby.saturday = form.frequencySat.data
			hobby.color = form.color.data;
			db.session.commit()
			print("Updated Entry")
			return redirect(url_for('hobbyView', username=username, hobbyName=form.name.data))
		elif form.delete.data:
			db.session.delete(hobby)
			db.session.commit()
			return redirect(url_for('hobbies', username=username))
	return render_template('hobbyView.html', hobbies=hobbies, hobby=hobby, form=form)

@home.route('/<username>/achievements', methods=['GET','POST'])
@login_required
def achievements(username):
	achievementList = [
	'perfWeekOneHobbyAch',
	'perfWeekAllHobbiesAch',
	'perfMonthOneHobbyAch',
	'perfMonthAllHobbiesAch'
	]


	user = User.query.filter_by(username=username).first_or_404()
	return render_template('achievements.html', username=current_user.username, achievementList=achievementList)

@home.route('/<username>/day/<dayid>', methods=['GET','POST'])
@login_required
def dayView(username, dayid):
	# Get Day object from db using id
	day = db.session.query(Day).get(dayid)
	
	monthConvert = ["January","February","March","April","May","June","July","August","September","October", "November", "December"]
	dtWeekday = datetime(day.year,day.month,day.date).weekday()
	weekday = day_name[dtWeekday]

	return render_template('dayView.html', day=day, month=monthConvert[day.month - 1], weekday=weekday)

@home.route('/devblog/', methods=['GET','POST'])
@login_required
def devBlog():
	username = current_user.username

	posts = []
	for post in DevBlogPosts.query.all():
		posts.append(post)

	return render_template('devBlog.html', username=username, posts=posts)











	
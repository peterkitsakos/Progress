from home import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from home import login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), index=True, unique=True, nullable=False)
	email = db.Column(db.String(128), index=True, unique=True, nullable=False)
	password_hash = db.Column(db.String(128))
	hobbies = db.relationship('Hobby', backref='user', lazy=True)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def get_password(self, password):
		return check_password_hash(self.password_hash, password)


days = db.Table('days',
	db.Column('day_id', db.Integer, db.ForeignKey('day.id'), primary_key=True),
	db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id'), primary_key=True)
)

class Hobby(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, server_default="")

	name = db.Column(db.String(32), index=True, nullable=False)
	sunday = db.Column(db.Boolean, default=False)
	monday = db.Column(db.Boolean, default=False)
	tuesday = db.Column(db.Boolean, default=False)
	wednesday = db.Column(db.Boolean, default=False)
	thursday = db.Column(db.Boolean, default=False)
	friday = db.Column(db.Boolean, default=False)
	saturday = db.Column(db.Boolean, default=False)
	color = db.Column(db.String(3), default="Red"); #Need to check for null when displaying
	duration = db.Column(db.String(2), nullable=False)
	notes = db.Column(db.Text)
	goals = db.Column(db.Text)

	dates = db.relationship('Day', secondary=days, backref='hobbies', lazy=True)

	def __repr__(self):
		return '<Hobby {}, Notes {}>'.format(self.name, self.notes)

class Day(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	date = db.Column(db.Integer)
	month = db.Column(db.Integer)
	year = db.Column(db.Integer) 
	#Has this date already past
	past = db.Column(db.Boolean)
	#Is date in current month
	curr = db.Column(db.Boolean)

	_hobbies = db.relationship('Hobby', secondary=days)

class DevBlogPosts(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	title = db.Column(db.Text)
	content = db.Column(db.Text)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
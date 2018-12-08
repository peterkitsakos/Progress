from home import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from home import login

class User(UserMixin, db.Model):
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String(32), index=True, unique=True)
		email = db.Column(db.String(128), index=True, unique=True)
		password_hash = db.Column(db.String(128))

		def __repr__(self):
			return '<User {}>'.format(self.username)

		def set_password(self, password):
			self.password_hash = generate_password_hash(password)

		def get_password(self, password):
			return check_password_hash(self.password_hash, password)

class Hobby(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String(32), index=True)
		frequency = db.Column(db.String(1))
		duration = db.Column(db.String(2))
		notes = db.Column(db.Text)
		goals = db.Column(db.Text)
		user = db.Column(db.Integer)
		link = db.Column(db.String(32))

		def __repr__(self):
			return '<Hobby {}, Notes {}>'.format(self.name, self.notes)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms.widgets import TextArea
from home.models import User

class LoginForm(FlaskForm):
		username = StringField('Username', validators=[DataRequired()])
		password = PasswordField('Password', validators=[DataRequired()])
		remember_me = BooleanField('Remember Me')
		submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
		username = StringField('Username', validators=[DataRequired()])
		email = StringField('Email', validators=[DataRequired(), Email()])
		password = PasswordField('Password', validators=[DataRequired()])
		password_2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
		submit = SubmitField('Register')

		def validate_user(self, username):
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError("Username is taken")

		def validate_email(self, email):
			user = User.query.filter_by(email=email.data).first()
			if user is not None:
				raise ValidationError("Email has already been registered")

class HobbyForm(FlaskForm):
		days = []
		hours = []
		for i in range(1,8):
			days.append((i,str(i)))
		for j in range(1,25):
			hours.append((j,str(j)))

		name = StringField('Hobby Name', validators=[DataRequired()])
		frequencySun = BooleanField()
		frequencyMon = BooleanField()
		frequencyTue = BooleanField()
		frequencyWed = BooleanField()
		frequencyThu = BooleanField()
		frequencyFri = BooleanField()
		frequencySat = BooleanField()
		duration = IntegerField('Duration (Hours per day)', validators=[DataRequired()])
		color = RadioField('Label Color', choices=[('Red',''),('Ora',''),('Yel',''),('Gre',''),('Blu',''),('Pur','')])
		notes = TextAreaField('Notes')
		goals = TextAreaField('Goals')
		submit = SubmitField('Add Hobby')
		save = SubmitField('Save Changes')
		delete = SubmitField('Delete')

class DevBlogForm(FlaskForm):
		title = StringField('Post Title', validators=[DataRequired()])
		content = TextAreaField('Post Content', validators=[DataRequired()])
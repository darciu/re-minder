# application forms
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from src.models import User


class RegistrationForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])

	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max = 100)])

	password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)])

	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

	

	submit = SubmitField('Sign Up')

	# validate with database content

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is already taken. Please choose a different one!')


	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is already taken. Please choose a different one!')




class LoginForm(FlaskForm):


	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember Me')

	submit = SubmitField('Sign Up')


class UpdateUserForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=50)])

	submit = SubmitField('Update')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data)
			if user:
				raise ValidationError('That email is already taken. Please choose a different one!')


class AddLessonForm(FlaskForm):

	title = StringField('Title',validators=[DataRequired(), Length(min=1, max = 20)])

	domain = StringField('Domain',validators=[DataRequired(), Length(min=1, max = 30)])

	picture = FileField('Upload picture', validators=[FileAllowed(['jpg','png'])])

	short_description = StringField('Short Description',validators=[DataRequired(), Length(min=1, max = 50)])

	content = TextAreaField('Content', validators=[DataRequired()])

	submit = SubmitField('Add Lesson')







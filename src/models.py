# database models

from src import db, login_manager
import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))



class User(db.Model, UserMixin):
	"""User table model"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable = False)
	email = db.Column(db.String(100), unique=True, nullable = False)
	password = db.Column(db.String(30), nullable = False)
	lessons = db.relationship('Lesson', backref='author', lazy=True)



class Lesson(db.Model):
	"""Lesson table model"""
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	domain = db.Column(db.String(50), nullable=False)
	short_description = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text,nullable=False)
	creation_date = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow)
	last_pass_date = db.Column(db.Date)
	next_pass_date = db.Column(db.Date)
	image_path = db.Column(db.String(20))
	pass_count = db.Column(db.Integer, nullable=False, default=0)
	archived = db.Column(db.Boolean, nullable=False, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)










db.create_all()
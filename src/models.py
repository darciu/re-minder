# database models

from src import db
import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable = False)
	email = db.Column(db.String(100), unique=True, nullable = False)
	password = db.Column(db.String(30), nullable = False)
	tasks = db.relationship('Tasks', backref='user', lazy=True)


class Tasks(db.Model):
	task_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	domain = db.Column(db.String(50), nullable=False)
	short_description = db.Column(db.String(100), nullable=False)
	text = db.Column(db.String(2000),nullable=False)
	creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
	last_pass_date = db.Column(db.DateTime, nullable=False, default='')
	next_pass_date = db.Column(db.DateTime, nullable=False, default='')
	pass_count = db.Column(db.Integer, nullable=False, default=0)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)





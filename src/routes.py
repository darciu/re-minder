# routing in application

from flask import render_template, url_for, flash, redirect
from src.forms import RegistrationForm, LoginForm
from src.models import User, Tasks
from src import app



@app.route('/')
def home():
    return render_template('home.html', title='Re-minder')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')


@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash('Account has been created successfully!','success_field')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)








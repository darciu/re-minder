# routing in application
import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from src.forms import RegistrationForm, LoginForm, UpdateUserForm, AddLessonForm
from src.models import User, Lesson
from src import app, db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Re-minder')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')





@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hashowane hasło
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account has been created successfully!','success_field')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page= request.args.get('next')
			
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Email or password are not valid!','unsuccess_field')
		
	return render_template('login.html', title='Login', form=form)



@app.route('/account')
@login_required
def account():
	form = UpdateUserForm()
	if form.validate_on_submit():
		current_user.email = form.email.data
		db.session.commit()
		flash('Email address has been changed!','success_field')
	elif request.method == 'GET':
		form.email.data = current_user.email
	return render_template('account.html', title='Your accoount', form = form)



@app.route('/app')
@login_required
def application():
	
	lessons = Lesson.query.filter_by(archived=False, author=current_user)
	return render_template('application.html', title='Run Application', lessons=lessons)


@app.route('/archived')
@login_required
def archived():
	lessons = Lesson.query.filter_by(archived=True, author=current_user)
	return render_template('archived.html', title='Archived Lessons', lessons=lessons)




def save_picture(image_from_form):
	"""Save picture in static/lesson_pics folder and return filename"""
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(image_from_form.filename)
	picture_filename = random_hex+f_ext
	picture_path = os.path.join(app.root_path, 'static/lesson_pics', picture_filename) 
	image_from_form.save(picture_path)
	return picture_filename


@app.route('/lesson_add', methods=['GET','POST'])
@login_required
def lesson_add():
	form = AddLessonForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_filename = save_picture(form.picture.data)
		else:
			picture_filename = None

		lesson = Lesson(title=form.title.data, domain=form.domain.data, short_description=form.short_description.data, content = form.content.data, 
			author=current_user, image_path=picture_filename)
		db.session.add(lesson)
		db.session.commit()
		flash('Lesson added!','success_field')
		return redirect(url_for('application'))
	return render_template('lesson_add.html',title='New Lesson', form = form)


@app.route('/lesson_play/<int:lesson_id>/<string:show>', methods=['GET'])
@login_required
def lesson_play(lesson_id, show):
	lesson = Lesson.query.get_or_404(lesson_id)
	
	return render_template('lesson_play.html', title='Play Lesson', lesson=lesson, show=show)


@app.route('/lesson_archive/<int:lesson_id>', methods=['GET','POST'])
@login_required
def lesson_archive(lesson_id):
	lesson = Lesson.query.get_or_404(lesson_id)
	if lesson.author != current_user:
		abort(403)
	lesson.archived = True
	db.session.commit()

	flash(f'Lesson with id {lesson_id} has been archived!','success_field')
	return redirect(url_for('application'))

def delete_picture(filename):
	
	try:
		os.remove(f'{app.root_path}/static/lesson_pics/{filename}')
	except:
		pass



@app.route('/lesson_delete/<int:lesson_id>')
@login_required
def lesson_delete(lesson_id, methods=['GET','POST']):
	lesson = Lesson.query.get_or_404(lesson_id)
	if lesson.author != current_user:
		abort(403)
	delete_picture(lesson.image_path)
	db.session.delete(lesson)
	db.session.commit()
	flash(f'Lesson with id {lesson_id} has been deleted!','success_field')
	return redirect(url_for('application'))



@app.route('/lesson_activate/<int:lesson_id>')
@login_required
def lesson_activate(lesson_id):
	lesson = Lesson.query.get_or_404(lesson_id)
	if lesson.author != current_user:
		abort(403)
	lesson.archived = False
	db.session.commit()

	flash(f'Lesson with id {lesson_id} has been activated!','success_field')
	return redirect(url_for('application'))




@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))



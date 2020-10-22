from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY'] = '09995165446f21c6d5487af318d03ead'

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









if __name__ == '__main__':
	app.run(host= '0.0.0.0',port=5000,threaded=False,processes=5)
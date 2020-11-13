# initialize application

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

from flask_login import LoginManager



app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY'] = '09995165446f21c6d5487af318d03ead'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # dajemy znać dodatkowi gdzie zlokalizowany jest login



from src import routes
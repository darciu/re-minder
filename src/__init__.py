# initialize application

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug=True

app.config['SECRET_KEY'] = '09995165446f21c6d5487af318d03ead'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from src import routes
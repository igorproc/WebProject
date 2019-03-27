from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controller import init_route
from DataBase import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_route(app, db)

app.run(port=8001, host='127.0.0.1')

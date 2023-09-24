from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///' + os.path.join(os.getcwd(),'site.db')
app.config['SECRET_KEY'] = "5a4ca6e00b1098343fb1965ac8f43f"

db = SQLAlchemy(app)
from app import routes
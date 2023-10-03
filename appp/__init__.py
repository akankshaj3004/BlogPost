from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///' + os.path.join(os.getcwd(),'site.db')
app.config['SECRET_KEY'] = "5a4ca6e00b1098343fb1965ac8f43f"
bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # function name of login route
login_manager.login_message_category = 'info'
db = SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'akankshajagtap8469@gmail.com'
app.config['MAIL_PASSWORD'] = 'wwytejjlvxhyanev'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from appp import routes
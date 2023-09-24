from datetime import datetime
from flask import Flask,render_template,url_for,flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///' + os.path.join(os.getcwd(),'site.db')
app.config['SECRET_KEY'] = "5a4ca6e00b1098343fb1965ac8f43f"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password= db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref="author" , lazy= True)

    def __repr__(self) :
        return f"User('{self.username}','{self.email}','{self.image})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(20), nullable=False)
    date_posted= db.Column(db.DateTime, nullable=False, default = datetime.utcnow )
    content = db.Column(db.Text(20), nullable=False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'),nullable=False)

    def __repr__(self) :
        return f"Post('{self.title}','{self.date_posted}')"

posts= [
    {
        "author": "Akanksha Jagtap",
        "title" : "My first Post",
        "content" : "This is my first Post",
        "date_posted" : "April 30 2023"
    },
    {
        "author": "Akanksha Jagtap",
        "title" : "My second Post",
        "content" : "This is my second Post",
        "date_posted" : "April 30 2024"
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/register", methods=["GET" ,"POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods=["GET" ,"POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data =="admin@gmail.com" and form.password.data == "password":
            flash(f"Login Successful!", 'success')
            return redirect(url_for('home'))
        else:
            flash(f"Login Failed. Please check username and password!", 'danger')
    return render_template("login.html", title = "Login", form = form)


if __name__ == "__main__":
    app.run(debug=True)
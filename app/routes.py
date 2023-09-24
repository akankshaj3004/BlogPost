from flask import Flask,render_template,url_for,flash, redirect
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm
from app import app

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

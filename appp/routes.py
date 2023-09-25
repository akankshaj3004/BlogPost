from flask import Flask,render_template,url_for,flash, redirect, request
from appp.models import User, Post
from appp.forms import RegistrationForm, LoginForm
from appp import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required

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
    if current_user.is_authenticated:
        return  redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username =form.username.data, email=form.email.data, password= hashed_password )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You can now successfully log in ','success')
        return redirect(url_for('login'))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods=["GET" ,"POST"])
def login():
    if current_user.is_authenticated:
        return  redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember= form.remember.data)
            next_page= request.args.get('next')
            print (next_page)
            return redirect(url_for('account')) if next_page else redirect(url_for('home'))
        else:
            flash(f"Login Failed. Please check email and password!", 'danger')
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title = "Account ")

    


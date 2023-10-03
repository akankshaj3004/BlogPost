import secrets
from PIL import Image
import os
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from appp.models import User, Post
from appp.forms import RegistrationForm, LoginForm, UpdateAccountForm,PostForm, RequestResetform, ResetPasswordForm
from appp import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page  = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page =5)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Your account has been created. You can now successfully log in ",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            print(next_page)
            return (
                redirect(url_for("account")) if next_page else redirect(url_for("home"))
            )
        else:
            flash(f"Login Failed. Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics' , picture_fn)
    output_size = (125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if(form.picture.data):
             picture_file = save_picture(form.picture.data)
             current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", category="success")
        return redirect(url_for("account"))
    elif request.method== 'GET':
        form.username.data= current_user.username
        form.email.data= current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account ", image_file=image_file, form=form
    )

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title= form.title.data , content = form.content.data,author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created!", category='success')
        return redirect(url_for('home'))
    return render_template("create_post.html", title="New Post", form= form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post=post, legend = "Update Post")

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content
    if(form.validate_on_submit()):
        post.title =  form.title.data
        post.content = form.content.data
        db.session.commit()
        flash ("Your post has been updated", 'success')
        return redirect (url_for('post', post_id = post.id))
    return render_template("create_post.html", title="Update Post", legend = "Update Post" , form= form)

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash ("Your post has been deleted", 'success')
    return redirect (url_for('home'))

@app.route("/user/<string:username>")
def user_post(username):
    page  = request.args.get('page', 1, type = int)
    user  = User.query.filter_by(username = username).first_or_404()
    # the \ is just used to get the whole code in different line
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page, per_page =5)
    return render_template("user_post.html", posts=posts, user = user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg= Message("Password Reset Request", sender = 'noreply@flaskblog.com', recipients= [user.email])
    msg.body = f''' To reset your password, visti the following link:
{url_for('reset_token', token = token, _external= True)}

If ypu did not make this reqest then ignore this email.
'''

    mail.send(msg)
    pass

@app.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", 'info')
        return redirect(url_for('login'))
    return render_template("reset_request.html" , title="Reset Password", form = form)

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash ('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_redirect'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(
            f"Your password has been updated. You can now login",
            "success",
        )
        return redirect(url_for("login"))
    return render_template('reset_token.html',title="Reset Password", form = form )

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html', err="404")

@app.errorhandler(403)
def error_403(error):
    return render_template('error.html', err="403")

@app.errorhandler(500)
def error_500(error):
    return render_template('error.html', err = "500")

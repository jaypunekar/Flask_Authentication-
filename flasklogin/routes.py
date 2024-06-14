from flask import render_template, url_for, flash, redirect
from flasklogin import app, db, bcrypt, mail
from flasklogin.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from flasklogin.models import User
from flask_login import login_user, current_user, logout_user
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    with app.app_context():
        posts = list(User.query.all())
    return render_template("home.html", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hashed the password and stored it in MySQL Database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash(f"Your account has been created successfully! {form.username.data}!", category="success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You are logged in!", category="success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password", category="danger")
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[user.email])

    msg.body = f'''To reset you password visit following link:
{url_for("reset_token", token=token, _external=True)} 
If you did not make this request then ignore.
    '''
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been send with instruction to reset password", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        with app.app_context():
            user.password = hashed_password
            db.session.add(user)
            db.session.commit()
        flash(f"You password has been changed!", category="success")
        return redirect(url_for("home"))
    return render_template("reset_token.html", title="Reset Password", form=form)

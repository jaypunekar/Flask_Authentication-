from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasklogin.models import User
from flasklogin import app


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    # This 2 methods automatically execute because unique=True in models.py file for User
    # The original error was given by SQLAlchemy and is handled by this
    # The function names have to "validate_field" where field is the name we want to validate
    # It is a template!!!

    def validate_username(self, username):
        with app.app_context():
            user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken")

    def validate_email(self, email):
        with app.app_context():
            user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already taken")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=20)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        with app.app_context():
            user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is not account with this email. Register first.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")

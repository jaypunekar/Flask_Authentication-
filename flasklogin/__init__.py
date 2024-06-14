import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

username = 'root'
password = 'Root@12345'
host = 'localhost'
port = '3306'
database = 'student'

encoded_password = quote_plus(password)

db_url = f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}?charset=utf8mb4"

app = Flask(__name__)
app.config["SECRET_KEY"] = "4d42cdd9c3c4dfe1d489ea71bd6b31e6"
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "jaypunekar01@gmail.com"
app.config["MAIL_PASSWORD"] = "lktd bppq pzdm cqfp"
mail = Mail(app)

from flasklogin import routes

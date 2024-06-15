## Demo Video [Click Here](https://youtu.be/AVQxj_St0AY)

This repository contains the implementation of a login system using Flask, MySQL, SQLAlchemy as the ORM, and HTML/CSS for the frontend. The system includes functionalities for user registration, login, and password reset through email.

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine using Git.

```bash
git clone https://github.com/jaypunekar/flask_authentication.git
cd flask_authentication
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies. Create and activate a virtual environment using the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate
```

### 3. Install Dependencies
With the virtual environment activated, install the required dependencies using the requirements.txt file:

```bash
pip install -r requirements.txt
```
### 4. Setup MySQL Database
Install MySQL
If you do not have MySQL installed, download and install it from the official MySQL website.

I have given my MySQL configuration on localhost you can do the same.

### 5. Configure the Application
Open the __init__.py file in the repository and update the database connection string with your MySQL username, password, and database name. It should look something like this:

```bash
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# Database credentials
username = 'root'
password = 'Root@12345'
host = 'localhost'
port = '3306'
database = 'student'

# Encode the password for the database URL
encoded_password = quote_plus(password)

# Create the database URL
db_url = f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}?charset=utf8mb4"

# Initialize the Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Mail server configuration
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_email_password"
mail = Mail(app)

# Import routes to register them with the app
from flasklogin import routes
```

### 6. Run the Application
Run the following command to start the Flask server:

```bash
python app.py
```

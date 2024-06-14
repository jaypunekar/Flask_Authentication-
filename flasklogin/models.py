from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flasklogin import db, login_manager, app
from flask_login import UserMixin


# This functionality is for Login
@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        with app.app_context():
            usr = User.query.get(user_id)
        return usr

    def __repr__(self):
        return f"User('{self.username}', {self.email})"

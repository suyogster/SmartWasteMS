from datetime import datetime
from swms import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False,
                           nullable=True, default='default.jpg')
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120),nullable=False,default='user')
    created_by = db.Column(db.String(120), nullable=True, default='admin')
    dustbins = db.relationship('Dustbin', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}','{self.image_file}', '{self.role}','{self.created_by}')"


class Dustbin(db.Model):
    __tablename__ = 'dustbin'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

from typing import DefaultDict
from app import db
from datetime import datetime, date, timedelta
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Create a table of users and user roles
roles_users_table = db.Table('roles_users',
                            db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                            db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    ph_no = db.Column(db.BigInteger , nullable=True)
    password = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(120), nullable=True)
    activation_code = db.Column(db.Integer)
    code_limit = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    roles = db.relationship('Roles', secondary=roles_users_table, backref=db.backref('users'), lazy='dynamic')
    posts = db.relationship('Posts', backref='poster')
    def is_user_active(self):
        return self.active

    def __repr__(self):
        return '<%r>' % self.name

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
    slug = db.Column(db.String(200))
    img = db.Column(db.String(120), nullable=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Define models for the users and user roles
class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))



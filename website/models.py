from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_subjects = db.relationship('UserSubjects', back_populates='user')

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    class_name = db.Column(db.String(150))
    code = db.Column(db.String(7), unique=True)
    subject_users = db.relationship('UserSubjects', back_populates='subject')

class UserSubjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    is_teacher = db.Column(db.Boolean)
    user = db.relationship('User', back_populates='user_subjects')
    subject = db.relationship('Subjects', back_populates='subject_users')




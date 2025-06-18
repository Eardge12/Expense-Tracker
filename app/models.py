from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable =False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password_hash = db.Column(db.String(200),nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Float,nullable=False)
    category = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(200),nullable=True)
    date= db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',backref=db.backref('expenses',lazy = True))

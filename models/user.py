from database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
  # Structure of table for adding a new user with username and password
  id = db.Column(db.Integer,primary_key=True)
  username = db.Column(db.String(80),nullable=False,unique=True)
  password = db.Column(db.String(80),nullable=False)
  role = db.Column(db.String(80),nullable=False, default='user')
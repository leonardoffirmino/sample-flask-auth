from app import db


class User(db.Model):
  # Structure of table for adding a new user with username and password
  id = db.Column(db.Integer,primary_key=True)
  username = db.Column(db.String(80),nullable=False,unique=True)
  password = db.Column(db.String(80),nullable=False)
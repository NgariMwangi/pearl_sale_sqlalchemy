from main import db
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(80), unique=True, nullable=False)
    username=db.Column(db.String(80))
    password = db.Column(db.String(80))
    confirm_password = db.Column(db.String(120))
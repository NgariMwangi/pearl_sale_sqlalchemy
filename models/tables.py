from flask.scaffold import F
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from main import db
class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),  nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    rel=db.relationship('Sales', backref='product')
    re=db.relationship('Restocking_update', backref="product")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(80), unique=True, nullable=False)
    username=db.Column(db.String(80))
    password = db.Column(db.String(80))
    confirm_password = db.Column(db.String(120))

class Stocks(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80))
    buying_price = db.Column(db.Integer)
    selling_price = db.Column(db.Integer)
    stock_quantity = db.Column(db.Integer)

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    created_at=db.Column(db.DateTime(timezone=True),server_default=func.now())

class Restocking_update(db.Model):
    __tablename__ = 'restocking_update'
    id = db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('products.id'))
    stockchanged=db.Column(db.Integer)
    changed_sp =db.Column(db.Integer)
    changed_bp=db.Column(db.Integer)
    change_time=db.Column(db.DateTime(timezone=True),server_default=func.now())






from main import db
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
class Stocks(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('products.id'))
    stock_quantity = db.Column(db.Integer)
    re=db.relationship('Restocking_update', backref="product")
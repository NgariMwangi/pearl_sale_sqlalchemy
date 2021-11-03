from sqlalchemy.orm import backref
from main import db

class Products(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),  nullable=False)
    buying_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

    rel=db.relationship('Sales', backref='product')    
    r=db.relationship('Stocks', backref="stocks")
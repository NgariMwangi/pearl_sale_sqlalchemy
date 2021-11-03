from main import db
from sqlalchemy.orm import backref
from sqlalchemy.sql import func
class Restocking_update(db.Model):
    __tablename__ = 'restocking_update'
    id = db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('stocks.pid'))
    stockchanged=db.Column(db.Integer)
    newstock=db.Column(db.Integer)
    change_time=db.Column(db.DateTime(timezone=True),server_default=func.now())
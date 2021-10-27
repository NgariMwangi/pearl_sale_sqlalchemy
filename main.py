from werkzeug.utils import escape
from kra import Payroll
import psycopg2
from flask import Flask, request, render_template, Request, redirect, url_for, flash,session
from datetime import date
import json, ast

from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from mai import sales

app = Flask(__name__)
app.config["SECRET_KEY"] = "#deno0707@mwangi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:deno0707@localhost:5432/orm'
db = SQLAlchemy(app)

from models.tables import Products,User,Sales,Stocks,Restocking_update
db.create_all()



@app.route('/')
def hello_world():
    return render_template('index.html')



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')
            return redirect(url_for('log', next = request.url))
    return wrap

@app.route('/signup',methods=["POST","GET"])
def sign():
     if request.method=="POST":
          email=request.form["email"]
          password=request.form["password"]
          password2=request.form["password2"]
          username=request.form["username"]
          emails=User.query.all()
          ema=[]
          for users in emails:
               ema.append(users.email)
          print(ema)
          for e  in ema:
               if email==e:
                    return redirect('/signup')
          if password == password2:
               new_user=User(email=email,password=password,confirm_password=password2,username=username)
               db.session.add(new_user)
               db.session.commit()
               return redirect('/')
          else:
               return redirect('/signup')
     else:
          return render_template("signup.html")
     
@app.route('/login', methods=["POST", "GET"])
def log():
     if request.method=="POST":

          email=request.form["email"]
          
          password=request.form["password"]   
          emails=User.query.all()
          for e in emails:
               if e.email == email:
                    if e.password == password:
                         session["email"]=email
                         #logged_in =session['logged_in']
                         return redirect('/')

          return redirect('/signup')    
     else:
          return render_template("signup.html")     

@app.route('/products', methods=["POST", "get"])
#@login_required
def product():
     if request.method == "POST":
        product_name = request.form["name"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling"]
        stock_quantity = request.form["stock"]  
        new_product = Products(name =product_name ,buying_price=buying_price,selling_price=selling_price, stock_quantity = stock_quantity)
        db.session.add(new_product)
        db.session.commit()  
        return redirect("/products")
     else:
          all_products=Products.query.all()
          return render_template('products.html',  all_products= all_products)

@app.route('/sales', methods=["POST", "GET"])
#@login_required
def sale():

     if request.method == "POST":


          pid = request.form["Item-id"]
          sale_quantity = request.form["item-quantity"]
          x = int(sale_quantity)
          st=Products.query.filter_by(id=pid).all()
          y=st[0].stock_quantity

          rem=y-x
          print(rem)
          if rem < 0:
               flash('Quantity ordered is higher that stock available')
               return redirect(url_for("product"))
          else:
               updated=Products.query.filter_by(id=pid).update({Products.stock_quantity:rem})
               db.session.commit()
               new_sale=Sales(pid=pid,quantity=sale_quantity)
               db.session.add(new_sale)
               db.session.commit()
               return redirect('/sales')
     else:
          sale=Sales.query.all()
          # print(sale)
          lst4=sale
          # print(sale[0].product.id)
          #sale= Sales.query.filter_by(product.__name__).all()
          # print(sale)
     
          
          lst4=sale
          return render_template('sales.html', lst4=lst4)
          
@app.route('/edit',methods=["POST", "GET"])
def edit():
    if request.method == "POST":
          id=request.form["Item-id"]
          name= request.form["name"]
          bp = request.form["buyingprice"]
          sp= request.form["sellingprice"]
          st= request.form["stockquantity"]
          print(st)
          stock=Stocks.query.filter_by(id=id).all()
          sbp=stock[0].buying_price
          ssp=stock[0].selling_price
          sst=stock[0].stock_quantity
          print(sst)
          bp=int(bp)
          sp=int(sp)
          st=int(st)
          sbp=bp-sbp
          ssp=sp-ssp
          sst=st-sst
          print(sst)
          change=Restocking_update(pid=id,stockchanged=sst,changed_sp=ssp,changed_bp=sbp)
          db.session.add(change)
          db.session.commit()  
          update=Stocks.query.filter_by(id=id).update({Stocks.name:name,Stocks.buying_price:bp,Stocks.selling_price:sp,Stocks.stock_quantity:st})
          db.session.commit()
          updated=Products.query.filter_by(id=id).update({Products.name:name,Products.buying_price:bp,Products.selling_price:sp,Products.stock_quantity:st})
          db.session.commit()
          
          return redirect("/products")

@app.route('/stock',methods=["POST", "GET"])
# @login_required
def stock():
     if request.method == "POST": 
          name = request.form["name"]
          buying_price = request.form["buying_price"]
          selling = request.form["selling"]
          stock = request.form["stock"]
          new_product = Stocks(name =name ,buying_price=buying_price,selling_price=selling, stock_quantity = stock)
          db.session.add(new_product)
          db.session.commit()
          new_product = Products(name =name ,buying_price=buying_price,selling_price=selling, stock_quantity = stock)
          db.session.add(new_product)
          db.session.commit()
          return redirect("/stock")
     else:
          all_products=Stocks.query.all()
          list1=all_products
          return render_template('stock.html', list1=list1)


     





     
     
        
          









if __name__ == '__main__':
     app.run(debug=True)
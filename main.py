from flask import Flask, request, render_template, redirect, url_for, flash,session
from werkzeug.utils import escape
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:deno0707@localhost:5432/orm'
app.config["SECRET_KEY"] = "#deno0707@mwangi"

db = SQLAlchemy(app)

from models.products import Products
from models.restocking_update import Restocking_update
from models.sales import Sales
from models.stocks import Stocks
from models.user import User

@app.before_first_request()
def create_table():
     db.drop_all()
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
        id=Products.query.filter_by(product_name=product_name).all()
        pid=id.id
        newstock=Stocks(pid=pid,stock_quantity=stock_quantity)
        db.session.add(newstock)
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
          stock=Stocks.query.filter_by(id=id).all()
          sbp=stock[0].buying_price
          ssp=stock[0].selling_price
          
          
          bp=int(bp)
          sp=int(sp)
          sbp=bp-sbp
          ssp=sp-ssp
          updated=Products.query.filter_by(id=id).update({Products.name:name,Products.buying_price:bp,Products.selling_price:sp})
          db.session.commit()
          
          return redirect("/products")

@app.route('/stock',methods=["POST", "GET"])
# @login_required
def stock():
     if request.method == "POST": 
          
          pid = request.form["Item-id"]
          
          
          stock_added = request.form["stock"]
          stock=Stocks.query.filter_by(pid=pid).all()
          sst=stock[0].stock_quantity
          s=int(stock_added)
          newstock=sst+s
          update=Stocks.query.filter_by(pid=pid).update({Stocks.stock_quantity:newstock})
          db.session.commit()
          change=Restocking_update(pid=pid,stockchanged=stock_added,newstock=newstock)
          db.session.add(change)
          db.session.commit()  
         
          db.session.commit()
          return redirect("/stock")
     else:
          all_products=Stocks.query.all()
          list1=all_products
          return render_template('stock.html', list1=list1)



# if __name__ == '__main__':
#      app.run(debug=True)
from kra import Payroll
import psycopg2
from flask import Flask, request, render_template, Request, redirect, url_for, flash,session
from datetime import date
import json, ast
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SECRET_KEY"] = "#deno0707@mwangi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/orm'
db = SQLAlchemy(app)

#app.config["SECRET_KEY"] = "36d44b1536a758b6cfb4ab06430c574cecf024ad288c0bf0de2cb3a5f1cc63e8"
conn = psycopg2.connect(user="postgres", password="deno0707",host="127.0.0.1", port="5432", database="myduka")
#conn = psycopg2.connect(database="d66n9lkjhpv4d2", host="ec2-54-155-61-133.eu-west-1.compute.amazonaws.com", user="skfkvatvfaigmx", port=5432, password="36d44b1536a758b6cfb4ab06430c574cecf024ad288c0bf0de2cb3a5f1cc63e8")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS product1 (id serial PRIMARY KEY,name VARCHAR(100),buying_price INT,selling_price INT,stock_quantity INT);")
cur.execute("CREATE TABLE IF NOT EXISTS sale (id serial PRIMARY KEY,pid INT, quantity INT, created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW() );")
cur.execute("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY,username VARCHAR(100), email VARCHAR(100),password VARCHAR(100),password2 VARCHAR(100) );")
cur.execute("CREATE TABLE IF NOT EXISTS stocks (id serial PRIMARY KEY,name VARCHAR(100),buying_price INT,selling_price INT,stock_quantity INT);")
cur.execute("CREATE TABLE IF NOT EXISTS restocking_update (id serial PRIMARY KEY, pid INT,stockchanged INT,changed_sp INT,changed_bp INT,change_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW());")
conn.commit()

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
        cur=conn.cursor()
        email=request.form["email"]
        password=request.form["password"]
        password2=request.form["password2"]
        username=request.form["username"]
        cur.execute('select email from users')
        emails=cur.fetchall()
        q=[]
        for y in emails:
            q.append(y[0])

        
        if password==password2:
                for t in q:
                    if email !=t:
                        cur.execute("""INSERT INTO users(username,email,password,password2) VALUES ( %(username)s,%(email)s,%(password)s,%(password2)s)""", {
                            "username":username, "email": email, "password":password, "password2": password2, })              
                        return redirect("/products")
                
                    else:
                        flash('email already exist')
                        return redirect("/signup")
                
               
        else:
            flash('password can not be confirmed')          
            return redirect("/signup")

    else:
        return render_template("signup.html")

@app.route('/login', methods=["POST", "GET"])
def log():
    if request.method=="POST":
        cur=conn.cursor()
        email=request.form["email"]
        logged_in =session['logged_in']
        password=request.form["password"]
        cur.execute("select count(id) from users where email= %(email)s and password=%(password)s", {"email":email,"password":password})
        count=cur.fetchone()
        for i in count:
            if i[0]==1:
                session["email"]=email
                
                
                
                return redirect("/products")
            else:
                flash('incorrect details')
                return redirect("/login")

    
       
        
        # for b in f:
        #     if b[2]==h:
        #         if b[3]==j:
        #             return redirect("/products")
        #         else:
        #             flash('incorrect password')
        #     else:
        #         flash('invalid Email')
    else:
        return render_template("signup.html")
    


@app.route('/dashboard')
@login_required
def dash():
    cur=conn.cursor()
    cur.execute("select count(id) from product1")
    t_products=cur.fetchall()
    t_products=t_products[0] 
    cur.execute("select count(id) from sale")
    sale_count=cur.fetchall()
    sale_count=sale_count[0]
    cur.execute("""select sum((product1.selling_price-product1.buying_price)*sale.quantity) as profit, product1.name from sale 
        join product1 on product1.id=sale.pid
        GROUP BY product1.name""")
    graph=cur.fetchall()
    
    product_name=[]
    profit=[]
    for i in graph:
        product_name.append(i[1])
        profit.append(i[0])
        
    cur.execute(""" select to_char("created_at", 'mm-dd-yyyy'),sum((product1.selling_price-product1.buying_price)*sale.quantity) as profit
from sale join product1 on product1.id=sale.pid
        GROUP BY sale.created_at""")
    line=cur.fetchall()
    # print(line)
    date=[]
    profit=[]
    for u in line:
        date.append(u[0])
        profit.append(u[1])    
    return render_template("dashboard.html", t_products=t_products,sale_counts=sale_count,product_name=product_name,graph=graph,date=date,profit=profit)
    

@app.route('/')
def hello_world():
    cur = conn.cursor()
    

    return render_template('index.html')


@app.route('/change')
def products():
    return render_template('change.html')


@app.route('/products', methods=["POST", "get"])
@login_required
def product():

    if request.method == "POST":
        cur = conn.cursor()
        product_name = request.form["name"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling"]
        stock_quantity = request.form["stock"]        
        cur.execute("""INSERT INTO product1(name,buying_price,selling_price,stock_quantity) VALUES ( %(n)s,%(bp)s,%(sp)s,%(st)s)""", {
                    "n": product_name, "bp": buying_price, "sp": selling_price, "st": stock_quantity, })
        conn.commit()
        return redirect("/products")
    else:
        cur = conn.cursor()
        cur.execute("select * from product1")
        products = cur.fetchall()
        return render_template('products.html',  products= products)


@app.route('/sales/<int:id>')
@login_required
def sales(id):
    cur = conn.cursor()
    cur.execute("""select sale.id, product1.name, product1.stock_quantity,(product1.selling_price-product1.buying_price)*sale.quantity as profit from product1
    join sale on sale.pid=product1.id where  pid= %(id)s""", {"id": id})
    sales = cur.fetchall()
    
    return render_template('sales.html', sales=sales)


@app.route('/sales', methods=["POST", "GET"])
@login_required
def sale():
    if request.method == "POST":
        pid = request.form["Item-id"]
        sale_quantity = request.form["item-quantity"]
        x = (int(sale_quantity))

        cur = conn.cursor()
        cur.execute(
            """select stock_quantity from product1 where id=%(pid)s""", {"pid": pid})
        st = cur.fetchone()
        y = list(st)
        z = y[0]-x
        print(y[0])
        if z <= 0:
            flash('Quantity ordered is higher that stock available')
            return redirect(url_for("product"))
        else:
            cur.execute("""update product1 set stock_quantity=%(z)s where id=%(pid)s""", {
                        "pid": pid, "z": z})
            cur.execute("""update stocks set stock_quantity=%(z)s where id=%(pid)s""", {
                        "pid": pid, "z": z})
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO sale (pid,quantity) VALUES (%s,%s)", (pid, sale_quantity))
            conn.commit()
            return redirect(url_for("sa"))


@app.route('/sal')
def sa():
    cur = conn.cursor()
    cur.execute("""select sale.id, product1.name, product1.stock_quantity,(product1.selling_price-product1.buying_price)*sale.quantity as profit from product1
    join sale on sale.pid=product1.id """,)
    sale = cur.fetchall()
    lst4 = sale

    return render_template('sales.html', lst4=lst4)
@app.route('/edit',methods=["POST", "GET"])
def edit():
    if request.method == "POST":
    
        e=request.form["Item-id"]
        a = request.form["name"]
        b = request.form["buyingprice"]
        c= request.form["sellingprice"]
        d = request.form["stockquantity"]
        cur.execute("""select * from stocks where id=%(e)s""",{"e": e})
        ch=cur.fetchone()
        cur.execute("""update product1 set name=%(a)s,buying_price=%(b)s,selling_price=%(c)s,stock_quantity=%(d)s where id=%(e)s""", {
                        "e": e, "a": a,"b":b,"c":c,"d":d})
        cur.execute("""update stocks set name=%(a)s,buying_price=%(b)s,selling_price=%(c)s,stock_quantity=%(d)s where id=%(e)s""", {
                        "e": e, "a": a,"b":b,"c":c,"d":d})
        
        b=(int(b))
        c=(int(c))
        d=(int(d))
        bp=b-ch[2]
        sp=c-ch[3]
        st=d-ch[4]
        cur.execute( """INSERT INTO restocking_update (pid,stockchanged,changed_sp,changed_bp) VALUES (%(e)s,%(st)s,%(bp)s,%(sp)s)""", {"e":e,"st":st,"bp":bp,"sp":sp})

        conn.commit()
        return redirect("/products")






@app.route('/stock',methods=["POST", "GET"])
@login_required
def stock():
    if request.method == "POST":
        cur = conn.cursor()
        product_name = request.form["name"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling"]
        stock_quantity = request.form["stock"]
        print(product_name)
        
        cur.execute("""INSERT INTO stocks(name,buying_price,selling_price,stock_quantity) VALUES ( %(n)s,%(bp)s,%(sp)s,%(st)s)""", {
                    "n": product_name, "bp": buying_price, "sp": selling_price, "st": stock_quantity, })
        cur.execute("""INSERT INTO product1(name,buying_price,selling_price,stock_quantity) VALUES ( %(n)s,%(bp)s,%(sp)s,%(st)s)""", {
                    "n": product_name, "bp": buying_price, "sp": selling_price, "st": stock_quantity, })
        conn.commit()
        return redirect("/stocks")
    else:
        cur = conn.cursor()
        cur.execute("select * from stocks")
        record = cur.fetchall()
        list1 = record
        record = cur.fetchall()
        return render_template('stock.html', list1=list1)

if __name__ == "__main__":
    app.run(debug=True)

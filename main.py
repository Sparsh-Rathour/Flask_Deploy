# from flask import Flask,redirect,render_template,request,url_for,flash
# import json
# from flask_sqlalchemy import SQLAlchemy
# import pypyodbc as odbc
from flask_mail import Mail, Message
from flask import Flask,redirect,render_template,request,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import pyodbc
app = Flask(__name__)
app.secret_key="^%$^$^^*&&FGGY9178"
 
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://tap2023:tap2023@APINP-ELPTYIXVW\SQLEXPRESS/crudApp?driver=SQL Server'
db = SQLAlchemy(app)
# DRIVER_NAME='SQL SERVER'
# SERVER_NAME='APINP-ELPTTQSW3\SQLEXPRESS'
# DATABASE_NAME='crudApp'
 
 
# connnection_string=connection_string = (
#     'DRIVER={SQL Server};'
#     'SERVER=APINP-ELPTTQSW3\SQLEXPRESS;'
#     'DATABASE=crudApp;'
#     'UID=tap2023;'
#     'PWD=tap2023;'
# )
# conn=odbc.connect(connnection_string)
# print(conn)
 
 
 
# local_server= True
# app=Flask(__name__)
# app.secret_key="^%$^$^^*&&FGGY9178"
 
 
# database configuration
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/flaskcrudapp'
# db=SQLAlchemy(app)
 
 

 
 
# configuration of database tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(15))
 
class Products(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    productName=db.Column(db.String(50))
    productDescription=db.Column(db.String(100))
    rating=db.Column(db.Integer)
    stocks=db.Column(db.Integer)
    price=db.Column(db.Integer)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))

@app.route("/test/")
def test():
    try:
        # query=Test.query.all()
        # print(query)
        sql_query="Select * from test"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(sql_query).all()
            print(response)
        return f"Database is connected"
 
    except Exception as e:
        return f"Database is not connected {e} "
 
 
@app.route("/")
def home():
    products=Products.query.all()
    return render_template("index.html",products=products)
 
# create operation
@app.route("/create",methods=['GET','POST'])
def create():
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"INSERT INTO [products] ([productName], [productDescription], [rating], [stocks], [price]) VALUES ('{pName}', '{pDesc}', '{pRating}', '{pStocks}', '{pPrice}')"
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Added Successfully","success")
            return redirect(url_for('home'))
       
 
 
    return render_template("index.html")
 
# update operation
@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    product=Products.query.filter_by(pid=id).first()
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"UPDATE [products] SET [productName]='{pName}',[productDescription]='{pDesc}',[rating]='{pRating}',[stocks]='{pStocks}',[price]='{pPrice}' WHERE [pid]='{id}'"
       
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Updated Successfully","primary")
            return redirect(url_for('home'))
 
 
    return render_template("edit.html",product=product)
 
 
 
# delete operation
@app.route("/delete/<int:id>",methods=['GET'])
def delete(id):
    # print(id)
    query=f"DELETE FROM [products] WHERE [pid]={id}"
    with db.engine.begin() as conn:
        conn.exec_driver_sql(query)
        flash("Product Deleted Successfully","danger")
        return redirect(url_for('home'))
   
@app.route("/search", methods=['POST'])
def search():
    search = request.form.get('search')
    # check if the input string can be converted to an integer
    if search.isdigit():
        products = Products.query.filter_by(pid=int(search)).all()
    else:
        products = Products.query.filter(Products.productName.like("%"+search+"%")).all()
 
    return render_template("index.html", products=products)

@app.route("/save_contact", methods=["POST"])
def save_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    contact = Contacts(name=name, email=email)
    db.session.add(contact)
    db.session.commit()
    flash("Contact information successfully stored", "success")
    return redirect(url_for('contact'))

@app.route("/display_contacts")
def display_contacts():
    contacts = Contacts.query.all()
    return render_template("contacts.html", contacts=contacts)

@app.route("/contact")
def contact():
    return render_template("contact.html")
   
 
   
   
   
 
   
 
 
 
app.run(debug=True)
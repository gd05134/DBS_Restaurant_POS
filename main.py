#Import Libraries
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#global variables if needed

#Create Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///restaurant_pos.db'
db = SQLAlchemy(app)

#Initialize Relationship Schema
#Order Schema
class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)                                #Add Auto Increment
    cust_id = db.Column(db.Integer, db.ForeignKey("customer.cust_id"))               
    table_id = db.Column(db.Integer, db.ForeignKey("table.table_id"))                                                  
    order_time = db.Column(db.DateTime, default = datetime.today(), nullable=False)   #idk if this is the right datetime function, will change later
    total_cost = db.Column(db.Integer, nullable=False)                                #add logic for incrementing later, change to decimal

    def __init__(self, order_id, cust_id, table_id, order_time, total_cost):
        self.order_id = order_id
        self.cust_id = cust_id
        self.table_id = table_id
        self.order_time = order_time
        self.total_cost = total_cost

#Customer Schema
class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)                                 #Add Auto Increment
    cust_first_name = db.Column(db.String(50), nullable=False)                  
    cust_last_name = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(10), unique=True, nullable=False)                               
    email = db.Column(db.String(60), unique=True, nullable=False)                                
    pref_table = db.Column(db.Integer, db.ForeignKey("table.table_id"))               

    def __init__(self, cust_id, cust_first_name, cust_last_name, phone_no, email, pref_table):
        self.cust_id = cust_id
        self.cust_first_name = cust_first_name
        self.cust_last_name = cust_last_name
        self.phone_no = phone_no
        self.email = email
        self.pref_table = pref_table

#Table Schema
class Table(db.Model):
    table_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)                                  
    capacity = db.Column(db.Integer, unique=True, nullable=False)                                 
    loc = db.Column(db.String(20))
    
    def __init__(self, table_id, capacity, loc):
        self.table_id = table_id
        self.capacity = capacity
        self.loc = loc

#Reservation Schema
class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)                          #Add auto increment
    cust_id = db.Column(db.Integer, db.ForeignKey("customer.cust_id"), nullable=False)                        
    date_created = db.Column(db.DateTime, default = datetime.today(), nullable=False) #idk if this is the right datetime function, will change later
    date_reserved = db.Column(db.DateTime, default = datetime.today(), nullable=False)#pulls current time, find function to pull select time

    def __init__(self, reservation_id, cust_id, date_created, date_reserved):
        self.reservation_id = reservation_id
        self.cust_id = cust_id
        self.date_created = date_created
        self.date_reserved = date_reserved

#Payment Schema
class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, nullable=False)              #Add auto increment
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)                                 
    amount = db.Column(db.Integer, nullable=False)                                    #Change to decimal
    payment_method = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default = datetime.today(), nullable=False)

    def __init__(self, payment_id, order_id, amount, payment_method, payment_date):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_date = payment_date

#MenuCategory Schema
class MenuCat(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, nullable=False)                               #increments
    name = db.Column(db.String(30), unique=True, nullable=False)                                  

    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

#MenuItem Schema
class MenuItem(db.Model):
    menu_item_id = db.Column(db.Integer, primary_key=True, nullable=False)                              #Increments
    category_id = db.Column(db.Integer, db.ForeignKey("menu_cat.category_id"), nullable=False)                               
    name = db.Column(db.String(50), unique=True, nullable=False)                                  
    desc = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)                                     #Change to decimal

    def __init__(self, menu_item_id, category_id, name, desc, price):
        self.menu_item_id = menu_item_id
        self.category_id = category_id
        self.name = name
        self.desc = desc
        self.price = price
        
#OrderItem Schema
class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True)                                            #Increments
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)                              
    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_item.menu_item_id"), nullable=False)                         
    quantity = db.Column(db.Integer, nullable=False)
    special_instructions = db.Column(db.String(100))

    def __init__(self, order_item_id, order_id, menu_item_id, quantity, special_instructions):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.special_instructions = special_instructions

#Main Restaurant Layout
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            
            db.session.commit()
            return redirect(url_for('order'))
        except:
               return 'There was an issue opening the order'
    else:
        return render_template('index.html')

#To enter Order state
@app.route('/order/<table_id>', methods=['GET','POST'])
def order(table_id):
     table = Table.query.get_or_404(table_id)
     if request.method == 'POST':
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
               return 'There was an issue opening the layout'
     else:
        return render_template('order.html', table = table)

#For Customers
customer_id = 0
@app.route('/customer', methods=['GET','POST'])
def add_customer():
    if request.method == 'POST':
        first_name = request.form['First Name']
        last_name = request.form['Last Name']
        phone_no = request.form['Phone No.']
        email = request.form['Email']
        pref_table = request.form.get('Preferred Table')
        try:
            db.session.add(Customer(cust_id=customer_id, first_name=first_name, last_name=last_name, phone_no=phone_no, email=email, pref_table=pref_table))
            customer_id += 1
            db.session.commit()
            return redirect(url_for('index'))
        except:
               return 'There was an issue entering your information'
    else:
        return render_template('customer.html')

#For reservations
@app.route('/reservation', methods=['GET','POST'])
def add_reservation():
    if request.method == 'POST':
      
        try:
            db.session.commit()
            return redirect(url_for('/'))
        except:
               return 'There was an issue reserving your table'
    else:
        return render_template('reservation.html')

if __name__ == '__main__':
     app.run(debug=True)
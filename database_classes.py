#Import Libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///restaurant_pos.db'
db = SQLAlchemy(app)
app.secret_key ='key'

#Initialize Relationship Schema
#Order Schema
class Order(db.Model):                                                     
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    table_id = db.Column(db.Integer, db.ForeignKey("table.table_id"))                                                  
    order_time = db.Column(db.DateTime, default = datetime.now(), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    order_items = db.relationship(
        'OrderItem',
        cascade="all, delete-orphan",
        backref='order'
    )

    def __init__(self, table_id, order_time, total_cost):
        self.table_id = table_id
        self.order_time = order_time
        self.total_cost = total_cost

#Customer Schema
class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_first_name = db.Column(db.String(50), nullable=False)                  
    cust_last_name = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(10), unique=True, nullable=False)                               
    email = db.Column(db.String(60), unique=True, nullable=False)                                
    pref_table = db.Column(db.Integer, db.ForeignKey("table.table_id")) 
    date_created = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    date_reserved = db.Column(db.DateTime, default = datetime.now(), nullable=False)             

    def __init__(self, cust_first_name, cust_last_name, phone_no, email, pref_table):
        self.cust_first_name = cust_first_name
        self.cust_last_name = cust_last_name
        self.phone_no = phone_no
        self.email = email
        self.pref_table = pref_table

#Table Schema
class Table(db.Model):
    table_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)                                  
    capacity = db.Column(db.Integer, nullable=False)                                 
    loc = db.Column(db.String(20))
    
    def __init__(self, table_id, capacity, loc):
        self.table_id = table_id
        self.capacity = capacity
        self.loc = loc


#Payment Schema
class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)        
    amount = db.Column(db.Float, nullable=False)                                            
    payment_method = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default = datetime.today(), nullable=False)

    def __init__(self, order_id, amount, payment_method):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method

#MenuCategory Schema
class MenuCat(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)                                  

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'<MenuCat {self.name}>'

#MenuItem Schema
class MenuItem(db.Model): 
    menu_item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey("menu_cat.category_id"), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)                              
    price = db.Column(db.Float, nullable=False)                                               

    def __init__(self, category_id, name, price):
        self.category_id = category_id
        self.name = name
        self.price = price
        
#OrderItem Schema
class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)
    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_item.menu_item_id"), nullable=False)                         
    quantity = db.Column(db.Integer, nullable=False)
    special_instructions = db.Column(db.String(100))

    menu_item = db.relationship('MenuItem', backref='order_items')                     

    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_item.menu_item_id"), nullable=False)                         
    def __init__(self, order_id, menu_item_id, quantity, special_instructions):
        self.order_id = order_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.special_instructions = special_instructions